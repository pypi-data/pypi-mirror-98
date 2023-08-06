import collections
import enum
import logging
from typing import Dict, List, NamedTuple, Optional, Tuple, Union

from tapa.verilog import xilinx as rtl
from tapa.verilog import ast

from .instance import Instance, Port

_logger = logging.getLogger().getChild(__name__)


class MMapConnection(NamedTuple):
  id_width: int
  args: Tuple[Instance.Arg, ...]


class Task:
  """Describes a TAPA task.

  Attributes:
    level: Task.Level, upper or lower.
    name: str, name of the task, function name as defined in the source code.
    code: str, HLS C++ code of this task.
    tasks: A dict mapping child task names to json instance description objects.
    fifos: A dict mapping child fifo names to json FIFO description objects.
    ports: A dict mapping port names to Port objects for the current task.
    module: rtl.Module, should be attached after RTL code is generated.

  Properties:
    is_upper: bool, True if this task is an upper-level task.
    is_lower: bool, True if this task is an lower-level task.

  Properties unique to upper tasks:
    instances: A tuple of Instance objects, children instances of this task.
    args: A dict mapping arg names to lists of Arg objects that belong to the
        children instances of this task.
    mmaps: A dict mapping mmap arg names to MMapConnection objects.
  """

  class Level(enum.Enum):
    LOWER = 0
    UPPER = 1

  def __init__(self, **kwargs):
    level: Union[Task.Level, str] = kwargs.pop('level')
    if isinstance(level, str):
      if level == 'lower':
        level = Task.Level.LOWER
      elif level == 'upper':
        level = Task.Level.UPPER
    if not isinstance(level, Task.Level):
      raise TypeError('unexpected `level`: ' + level)
    self.level = level
    self.name: str = kwargs.pop('name')
    self.code: str = kwargs.pop('code')
    self.tasks = collections.OrderedDict()
    self.fifos = collections.OrderedDict()
    if self.is_upper:
      self.tasks = collections.OrderedDict(
          sorted((item for item in kwargs.pop('tasks').items()),
                 key=lambda x: x[0]))
      self.fifos = collections.OrderedDict(
          sorted((item for item in kwargs.pop('fifos').items()),
                 key=lambda x: x[0]))
      self.ports = {i.name: i for i in map(Port, kwargs.pop('ports'))}
    self.module = rtl.Module('')
    self._instances: Optional[Tuple[Instance, ...]] = None
    self._args: Optional[Dict[str, List[Instance.Arg]]] = None
    self._mmaps: Optional[Dict[str, MMapConnection]] = None

  @property
  def is_upper(self) -> bool:
    return self.level == Task.Level.UPPER

  @property
  def is_lower(self) -> bool:
    return self.level == Task.Level.LOWER

  @property
  def instances(self) -> Tuple[Instance, ...]:
    if self._instances is not None:
      return self._instances
    raise ValueError(f'children of task {self.name} not populated')

  @instances.setter
  def instances(self, instances: Tuple[Instance, ...]) -> None:
    self._instances = instances
    self._args = collections.defaultdict(list)

    mmaps: Dict[str, List[Instance.Arg]] = collections.defaultdict(list)
    for instance in instances:
      for arg in instance.args:
        self._args[arg.name].append(arg)
        if arg.cat in {Instance.Arg.Cat.MMAP, Instance.Arg.Cat.ASYNC_MMAP}:
          mmaps[arg.name].append(arg)

    self._mmaps = {}
    for arg_name, args in mmaps.items():
      # width of the ID port is the sum of the widest slave port plus bits
      # required to multiplex the slaves
      id_width = max(
          arg.instance.task.get_id_width(arg.port) or 0 for arg in args)
      id_width += (len(args) - 1).bit_length()
      self._mmaps[arg_name] = MMapConnection(id_width, args=tuple(args))
      if len(args) > 1:
        for arg in args:
          arg.shared = True
        _logger.debug(
            "mmap argument '%s' is shared by %d ports",
            arg_name,
            len(args),
        )

  @property
  def args(self) -> Dict[str, List[Instance.Arg]]:
    if self._args is not None:
      return self._args
    raise ValueError(f'children of task {self.name} not populated')

  @property
  def mmaps(self) -> Dict[str, MMapConnection]:
    if self._mmaps is not None:
      return self._mmaps
    raise ValueError(f'children of task {self.name} not populated')

  def get_id_width(self, port: str) -> Optional[int]:
    if port in self.mmaps:
      return self.mmaps[port].id_width or None
    return None

  _DIR2CAT = {'produced_by': 'ostream', 'consumed_by': 'istream'}

  def get_fifo_port(
      self,
      fifo_name: str,
      direction: str,
  ) -> Tuple[str, int, str]:
    """Get port information to which a given FIFO is connected."""
    if direction not in self._DIR2CAT:
      raise ValueError(f'invalid direction: {direction}')
    if direction not in self.fifos[fifo_name]:
      raise ValueError(f'{fifo_name} is not {direction} any task')
    task_name, task_idx = self.fifos[fifo_name][direction]
    for port, arg in self.tasks[task_name][task_idx]['args'].items():
      if arg['cat'] == self._DIR2CAT[direction] and arg['arg'] == fifo_name:
        return task_name, task_idx, port
    raise ValueError(f'task {self.name} has inconsistent metadata')

  def add_m_axi(
      self,
      width_table: Dict[str, int],
      tcl_files: Dict[str, str],
  ) -> None:
    for arg_name, (m_axi_id_width, args) in self.mmaps.items():
      # add m_axi ports to the arg list
      self.module.add_m_axi(
          name=arg_name,
          data_width=width_table[arg_name],
          id_width=m_axi_id_width or None,
      )
      if len(args) == 1:
        continue

      # add AXI interconnect if necessary
      assert len(args) <= 16, f'too many ports connected to {arg_name}'
      assert m_axi_id_width is not None

      s_axi_id_width = max(
          arg.instance.task.get_id_width(arg.port) or 0 for arg in args)

      portargs = [
          ast.make_port_arg(port='INTERCONNECT_ACLK', arg=rtl.HANDSHAKE_CLK),
          ast.make_port_arg(
              port='INTERCONNECT_ARESETN',
              arg=rtl.HANDSHAKE_RST_N,
          ),
          ast.make_port_arg(port='M00_AXI_ACLK', arg=rtl.HANDSHAKE_CLK),
          ast.make_port_arg(port='M00_AXI_ARESET_OUT_N', arg=''),
      ]

      for axi_chan, axi_ports in rtl.M_AXI_PORTS.items():
        for axi_port, direction in axi_ports:
          m_axi_arg = f'{rtl.M_AXI_PREFIX}{arg_name}_{axi_chan}{axi_port}'

          if axi_port == 'ID' and direction == 'input':
            m_axi_arg = (f"{{{s_axi_id_width + 4 - m_axi_id_width}'d0, "
                         f"{m_axi_arg}}}")
          portargs.append(
              ast.make_port_arg(
                  port=f'M00_AXI_{axi_chan}{axi_port}',
                  arg=m_axi_arg,
              ))

      for idx, arg in enumerate(args):
        portargs += (
            ast.make_port_arg(port=f'S{idx:02d}_AXI_ACLK',
                              arg=rtl.HANDSHAKE_CLK),
            ast.make_port_arg(port=f'S{idx:02d}_AXI_ARESET_OUT_N', arg=''),
        )

        wires = []
        for axi_chan, axi_ports in rtl.M_AXI_PORTS.items():
          for axi_port, _ in axi_ports:
            wire_name = (f'{rtl.M_AXI_PREFIX}{arg.mmap_name}_'
                         f'{axi_chan}{axi_port}')
            wires.append(
                ast.Wire(name=wire_name,
                         width=rtl.get_m_axi_port_width(
                             port=axi_port,
                             data_width=width_table[arg_name],
                             id_width=arg.instance.task.get_id_width(arg.port),
                         )))
            portargs.append(
                ast.make_port_arg(
                    port=f'S{idx:02d}_AXI_{axi_chan}{axi_port}',
                    arg=wire_name,
                ))
        self.module.add_signals(wires)

      data_width = max(width_table[arg_name], 32)
      assert data_width in {32, 64, 128, 256, 512, 1024}
      module_name = (f'axi_interconnect_{data_width}b_'
                     f'{s_axi_id_width}t_x{len(args)}')
      s_axi_data_width = ' \\\n  '.join(
          f'CONFIG.S{idx:02d}_AXI_DATA_WIDTH {data_width}'
          for idx in range(len(args)))
      s_axi_read_acceptance = ' \\\n  '.join(
          f'CONFIG.S{idx:02d}_AXI_READ_ACCEPTANCE 16'
          for idx in range(len(args)))
      s_axi_write_acceptance = ' \\\n  '.join(
          f'CONFIG.S{idx:02d}_AXI_WRITE_ACCEPTANCE 16'
          for idx in range(len(args)))
      tcl_files.setdefault(
          module_name, f'''\
create_ip \\
  -name axi_interconnect \\
  -vendor xilinx.com \\
  -library ip \\
  -version 1.7 \\
  -module_name {module_name}
set_property -dict [list \\
  CONFIG.AXI_ADDR_WIDTH 64 \\
  CONFIG.NUM_SLAVE_PORTS {len(args)} \\
  CONFIG.THREAD_ID_WIDTH {s_axi_id_width} \\
  CONFIG.INTERCONNECT_DATA_WIDTH {data_width} \\
  CONFIG.M00_AXI_DATA_WIDTH {data_width} \\
  {s_axi_data_width} \\
  CONFIG.M00_AXI_READ_ISSUING 16 \\
  {s_axi_read_acceptance} \\
  CONFIG.M00_AXI_WRITE_ISSUING 16 \\
  {s_axi_write_acceptance} \\
  ] [get_ips {module_name}]
set_property generate_synth_checkpoint false [get_files {module_name}.xci]
generate_target {{synthesis simulation}} [get_files {module_name}.xci]
''')
      self.module.add_instance(
          module_name=module_name,
          instance_name=f'{module_name}__{arg_name}',
          ports=portargs,
      )
