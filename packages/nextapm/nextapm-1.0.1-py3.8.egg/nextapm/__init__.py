from nextapm.lib.util import validateConfig
from nextapm.lib.instrument.wrapper import start

name = "nextapm"

version = "1.0.1"

if validateConfig():
  start()

  
