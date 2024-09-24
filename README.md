# CodingOIer's Luogu Article Sync Helper

用于从本地把文章的更新推送到洛谷。

编写于不到一小时，有问题正常。

## 如何使用

下载二进制文件后，有如下命令。

**在当前目录放置一个 `.config`，内容是你的洛谷 Cookie，格式如下。**

```plain
754324
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- `luogu -init` 初始化目录，默认工作目录为当前目录，可使用 `-path` 指定工作目录。
- `luogu -add example.md -remote xxxxxx` 添加文件链接，`xxxxxx` 必须是手动创建一个新文章的 id。
- `luogu -remove example.md` 删除链接。
- `luogu -sync` 推送更新。

你也可以下载源码后使用 `python3 main.py` 加参数，效果相同。

## 本地开发

自己装依赖，不想写了。