import configparser
import os
import re

from terminaltables import DoubleTable

base_url = "https://sm.ms/api/v2/"
profile_url = base_url + "profile"
history_url = base_url + "history"
upload_history_url = base_url + "upload_history"
upload_url = base_url + "upload"


def gh_conf():
    """
    读取 ~/.pysmms 文件中 GitHub 配置。

    """

    config = configparser.ConfigParser()
    _config = config.read(os.path.expanduser("~") + "/.pysmms")
    if _config:
        return {
            "user": config["github"]["user"],
            "repo": config["github"]["repo"],
            "branch": config["github"]["branch"],
            "token": config["github"]["token"],
        }
    return None


def gh_table(items):
    """
    生成表格
    """

    table_instance = DoubleTable(items, "GitHub - 上传图片")
    table_instance.inner_row_border = True
    return table_instance.table


def auth():
    """
    读取 ~/.pysmms 文件中 smms 配置。

    如果读取失败返回空列表。
    """

    config = configparser.ConfigParser()
    _config = config.read(os.path.expanduser("~") + "/.pysmms")
    if _config:
        return eval(config["sm.ms"]["auth"])
    return []


def table(items, title):
    """
    生成表格
    """

    table_instance = DoubleTable(items, "SM.MS - {}".format(title))
    table_instance.inner_row_border = True
    return table_instance.table


def table_err(items):
    """
    处理异常消息
    """

    if items["code"] == "image_repeated":
        url = re.findall(
            "Image upload repeated limit, this image exists at: (.*)",
            items["message"]
        )[0]
        data = [
            ["Code", items["code"]],
            ["Message", "此图已存在"],
            ["URL", url],
            ["Request Id", items["RequestId"]]
        ]
    else:
        data = [
            ["Code", items["code"]],
            ["Message", items["message"]],
            ["Request Id", items["RequestId"]]
        ]
    return table(items=data, title="异常")
