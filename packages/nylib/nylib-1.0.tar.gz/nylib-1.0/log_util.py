# encoding:utf8
import logging
import sys
from loguru import logger as log

# 创建名为'spam_application'的记录器
logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)

log.add('./python.log')
loginfo = log.info

# 控制台输出

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)

# 创建级别为DEBUG的日志处理器
fh = logging.FileHandler('./python.log')
fh.setLevel(logging.INFO)

# 创建级别为ERROR的控制台日志处理器
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# 创建格式器，加到日志处理器中
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(sh)
logger.addHandler(fh)
logger.addHandler(ch)


def getLogger(name, file):
    logger.name = name
    logger.addHandler(logging.FileHandler(file))
    return logger
