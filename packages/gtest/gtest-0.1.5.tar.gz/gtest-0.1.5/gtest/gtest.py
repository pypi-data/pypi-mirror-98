# -*- coding: UTF-8 -*-
from gtest.model.options import Options
from gtest.model.suite_file_tree import SuiteFileTree
from gtest.model.suite_tree import SuiteTree
from gtest.runner.base_runner import runner_factory
from gtest.utils.opt_parser import OptionParser
from gtest.utils.output import Output
from gtest.utils.logger import logger
from gtest.exceptions import BaseException
from gtest.utils.file import log_traceback
import sys


class GTest(object):
    version = '0.1.5'

    def __init__(self, path, options):
        self.opt = Options(path, options, self.version)
        self.path = self.opt.run_path
        self.output = Output(self.opt)

    def run(self):
        """实际的测试启动入口函数"""
        try:
            file_tree = SuiteFileTree(self.path, self.opt)  # 先解析目录文件结构
            suite_tree = SuiteTree(file_tree, self.opt)  # 再生成数据树
            runner = runner_factory(self.opt.run_mode, suite_tree, self.opt)  # 执行用例
            '''miss: show result'''
        except Exception as e:
            if isinstance(e, BaseException):
                logger.debug("正常退出")
            else:
                import traceback
                exception_info = str(e)
                logger.debug('异常退出，原因: {}'.format(exception_info))
                traceback_info = traceback.format_exc()
                log_traceback(exception_info, traceback_info)
                if self.opt.track_error:
                    traceback.print_exc()


def run(args):
    """程序式入口"""
    path, options = OptionParser().parse(args)
    GTest(path, options).run()


def run_from_cli():
    """从命令行启动"""
    run(sys.argv[1:])

