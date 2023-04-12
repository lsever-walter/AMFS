import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from simple_pid import PID
from jax import RealTimePlotApplet


PID_Generator = PID()
PID_Generator.test()
