# -*- coding: UTF-8 -*-
from gtest.runner.base_runner import BaseRunner
from gtest.keyword_.common import *
from gtest.utils.logger import logger
import time


class DefaultRunner(BaseRunner):
    def __init__(self, suite_tree, option):
        BaseRunner.__init__(self, suite_tree, option)

    def run_case(self, case, _result):
        logger.info('执行用例: {}'.format(case.name))
        start_time = round(time.time(), 2)
        self.run_setup(case.name, case.setup, '用例')
        logger.add_prefix()
        result = list()
        try:
            result = [self.run_step(step) for step in case.step]
        except Exception as e:
            result.append(False)
            raise e
        finally:
            logger.sub_prefix()
            self.refresh_dyn()
            if False not in result:
                _result['result'] = True
                self.pass_count += 1
                logger.debug('用例执行成功: {}, 用时: {}'.format(case.name, self._count_time(start_time)))
            else:
                _result['result'] = False
                logger.debug('用例执行失败: {}, 用时: {}'.format(case.name, self._count_time(start_time)))
            self.run_teardown(case.name, case.teardown, '用例(Case)')
            '''清除浏览器环境，保证在当前窗口中下一个suite执行时有一个新页面和干净的cookies'''
            close_and_open(self.driver)
