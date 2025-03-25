"""
Author: Wyatt1026
Project Address: https://github.com/Wyatt1026/BilibiliDailyUp
"""
from config import config
from core.bilibili import Bilibili
import os

if __name__ == '__main__':
    # 检查是否使用环境变量
    if config.USE_ENVIRONMENT_VARIABLE:
        # 获取环境变量中的 COOKIES
        cookies = os.environ.get('COOKIES')
        if cookies:
            # 分割 COOKIES 字符串为列表
            ck_list = cookies.split(",")
        else:
            print("未设置 COOKIES 这个环境变量，任务终止")
            ck_list = []
    else:
        # 从配置文件中获取 COOKIE 列表
        ck_list = config.COOKIE_LIST

    # 遍历 COOKIE 列表，执行任务
    for ck in ck_list:
        bilibili = Bilibili(ck)
        bilibili.do_job()
