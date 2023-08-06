import os, sys

curPath = os.path.abspath(os.path.dirname(__file__))
parentPath = os.path.split(curPath)[0]
sys.path.append(parentPath)
