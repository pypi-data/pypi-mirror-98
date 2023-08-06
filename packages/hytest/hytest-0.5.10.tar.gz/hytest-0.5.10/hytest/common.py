from .utils.signal import signal


# 存储 全局共享 数据
GSTORE = {}

def INFO(info):
    """
    在日志和测试报告中打印 重要信息，
    使得 运行报告更加清晰

    参数：
    info :   信息描述
    """
    signal.info(f'{info}')

def STEP(stepNo:int,desc:str):
    """
    在日志和测试报告中打印出 测试步骤说明，
    使得 运行报告更加清晰

    参数：
    stepNo : 指定 是第几步
    desc :   步骤描述
    """
    signal.step(stepNo,desc)


def CHECK_POINT(desc:str, condition):
    """
    检查点

    参数：
    desc :   检查点文字描述
    condition ： 检查点 表达式
    """

    if condition:
        signal.checkpoint_pass(desc)
    else:
        signal.checkpoint_fail(desc)
        raise AssertionError()
