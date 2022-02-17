from threading import Thread
from typing import Callable, Dict
from rich.console import Console

from SDK.process import Process
from SDK.utils.time import sleep

class ModuleStore:

  def __init__(self, **kwargs):
      for key in kwargs:
        self.__setattr__(key, kwargs[key])

class ModuleConfig:

  def __init__(self, sleep_time: int, **kwargs):
    self.sleep_time = sleep_time

    for key in kwargs:
      self.__setattr__(key, kwargs[key])

class Module:

  def __init__(self, config: ModuleConfig, store: ModuleStore, fn: Callable):
    self.config = config
    self.store = store
    self.fn = fn
    self.active = False

__modules: Dict[str, Module] = {}

def register_module(function: Callable, name: str, config: ModuleConfig = ModuleConfig(1), store = ModuleStore()):

  # Infinite loop wrapper
  def wrapper(csgo: Process):
    try:
      while sleep(config.sleep_time):
        if module.active and csgo.window_active():
          function(csgo)
    except:
      Console().print_exception()

  # Create and register module
  module = Module(config, store, wrapper)
  if not name in __modules:
    __modules[name] = module  
  else:
    raise Exception(f'Module with name {name} already registered')

  # raise error if dev try to call and registered module directly
  def error():
    raise Exception('You should not be calling this function')

  return error

def get_modules():
  return __modules

def start_modules(csgo: Process):
  modules = get_modules()
  for name in modules:
    module = modules[name]
    Thread(target=module.fn, args=(csgo,), daemon=True).start()
