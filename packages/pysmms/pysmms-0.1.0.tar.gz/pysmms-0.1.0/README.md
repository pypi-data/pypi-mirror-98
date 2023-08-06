# PYSMMS

基于 sm.ms 图床的命令行工具，sm.ms 文档见[此链接](https://doc.sm.ms/)。

借鉴 [n0vad3v/smv2](https://github.com/n0vad3v/smv2)，在其基础上添加了上传成功后自动拷贝图片链接到剪贴板，多账号随机上传等功能。

# 安装

```bash
pip install pysmms
```

# 使用

## 查看帮助

```bash
➜  ~ pysmms help
pysmms {arg}

   profile          查看用户资料（需要配置 Authorization）
   ip_history       基于 IP 的临时上传历史记录
   history          获取用户上传记录（需要配置 Authorization）
   /path/to/picture 上传图片（需要配置 Authorization）

上传图片不需要配置 Authorization，但不保证图片的使用时效。
配置 Authorization 需要在用户根目录创建 .pysmms 文件，文件写入以下内容：

    [sm.ms]
    auth=['wKSlYH******z8eb8qSr']

注意：auth 以列表存放，支持多个 auth 随机上传。
```

## 上传图片

```bash
pysmms /path/to/picture
```

上传图片不强制需要 Authorization，但无 Authorization 的图片不保证时效。

例如：

![上传图片](https://i.loli.net/2020/02/24/lIBou7j5NetLfT1.png)

## 查看用户资料

```bash
pysmms profile
```

![用户资料](https://i.loli.net/2020/02/24/DwTYEchCsbmW4Iu.png)

## 查询临时上传历史

```bash
pysmms ip_history
```

此历史记录基于 IP，不需要配置 Authorization。

## 查询用户上传历史记录

```bash
pysmms history
```

此历史记录需要配置 Authorization，只可查询最近五条数据。

**[具体开发介绍查看此链接](https://lijianxun.top/274.html)**