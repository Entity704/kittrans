# Kittrans

[ [**English**](../../README.md) | **简体中文** ]

为 Kitty 终端模拟器编写的简易翻译器。

![Release](https://img.shields.io/github/v/release/Entity704/kittrans?style=flat-square&logo=github&logoColor=979DA4&label=Release&labelColor=24292E&color=blue&link=https%3A%2F%2Fgithub.com%2FEntity704%2Fkittrans%2Freleases%2Flatest)
![WIP](https://img.shields.io/badge/Status-Work%20in%20Progress-orange?style=flat-square&labelColor=24292E)


## 安装

1. 将项目复制到你的 Kitty 配置目录（可能是 `~/.config/kitty/kittrans`）
2. 添加 `map alt+shift+t kitten kittrans/src/kittrans.py @selection` 到你的配置文件（如 `kitty.conf`）
3. 在 `configs` 目录添加 `config.json` 并[配置](#配置)

然后，你就可以选择一串文本并点击 <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd> 去翻译它了。


## 配置

配置文件使用 JSON 格式。

配置项:

- `"provider"`：翻译提供者模块路径
- `"source"`: 源语言, 使用 [BCP 47](https://www.rfc-editor.org/info/rfc5646/) 语言标签的 Language-Script-Region 格式。`"auto"` 为自动检测
- `"target"`: 目标语言，使用 BCP 47 语言标签的 Language-Script-Region 格式
- `"options"`：给所有提供者模块的额外配置（值能够被 `"{provider}.options"` 中相同键的值覆盖）
- `"{provider}.options"`：给特定提供者的额外配置（如 API 密钥、接口 URI）


## 模块

参见 [模块](provider-modules.md)。
