import base64
import hashlib
import json
import os
import sys
import time

import pyperclip
import requests

from .utils import gh_conf, gh_table


class GitPic(object):
    __doc__ = "Github 图床，使用 jsDelivr CDN 加速。"

    @staticmethod
    def format_upload(item):
        """
        格式化 upload 接口返回的数据
        """

        items = [
            ["文件", item["filename"]],
            ["图片地址", item["url"]]
        ]
        try:
            pyperclip.copy(item["url"])
        except pyperclip.PyperclipException:
            print(
                "您的系统不支持复制粘贴！")
        finally:
            return gh_table(items)

    def upload(self, img_path):
        with open(img_path, "rb") as f:
            base64_data = base64.b64encode(f.read())
            img_data = base64_data.decode("utf8")

        data = gh_conf()
        if not data:
            sys.exit("请检查 github 配置！")

        content = "{}.{}".format(img_data, time.time()).encode("utf8")
        _name = hashlib.md5(content).hexdigest()[:8]
        suffix = os.path.splitext(img_path)[1]
        file_name = _name + suffix

        url = "https://api.github.com/repos/{user}/{repo}/contents/{file_name}?access_token={token}"
        url = url.format(
            user=data["user"],
            repo=data["repo"],
            file_name=file_name,
            token=data["token"]
        )

        html = requests.put(url, data=json.dumps({
            "message": "Upload by pysmms.",
            "branch": "master",
            "content": img_data
        })).json()

        if html.get("content", None):
            url = "https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/{filename}".format(
                user=data["user"],
                repo=data["repo"],
                branch=data["branch"],
                filename=file_name)
            return self.format_upload({"filename": file_name, "url": url})
        elif html.get("message", None):
            items = [
                ["Error Message", html["message"]],
                ["Documentation Url", html["documentation_url"]]
            ]
            gh_table(items)
        else:
            sys.exit("Error!")
