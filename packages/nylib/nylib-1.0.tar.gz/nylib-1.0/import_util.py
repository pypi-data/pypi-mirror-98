import sys, os

curPath = os.path.abspath(os.path.dirname(__file__))
# 加载上几级
for i in range(2):
    curPath = os.path.split(curPath)[0]
    sys.path.append(curPath)

from loguru import logger
from pylib import *
from mylib import *

from string import Template
import json
