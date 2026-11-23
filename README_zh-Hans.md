# Kittrans

[ [**English**](README.md) | **简体中文** | [**使简易化的中国人**](README_zh-Huh.md) ]

为 Kitty 终端模拟器编写的简易翻译器。

## 安装

1. 将脚本复制到 `~/.config/kitty/kittrans`
2. 添加 `map alt+shift+t kitten kittrans/kittrans.py` 到你的配置文件（如 `kitty.conf`）
3. 在 kittrans 目录添加 `config.json` 并[配置](#配置)

然后，你就可以选择一串文本并点击 <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd> 去翻译它了。

## 配置

配置文件使用 JSON 格式。

配置项:

- `"provider"`：翻译提供者模块路径
- `"source"`：源语言，使用 `"auto"` 以自动检测
- `"target"`：目标语言
- `"options"`：给特定提供者的额外配置（如 API 密钥、接口 URI）
