import time


def wait(t):
    """
    :param time: 要等待的时间
    """
    time.sleep(int(t))


def close_and_open(driver):
    """
    :inner_param driver:  Web驱动
    """

    driver.execute_script('window.open()')
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])


def new_browser():
    """
    :inner_param driver:  Web驱动
    """
    pass


keyword = {'wait': wait,
           'new_page': close_and_open,
           'new_browser': new_browser}


