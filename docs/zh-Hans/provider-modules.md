# Kittrans | 模块

[ [**English**](../provider-modules.md) | **简体中文** ]


## 自定义你自己的提供者

参见 [提供者模块模板](../../src/providers/__init__.py)。


## 内置模块

### Google

`providers.google`

谷歌翻译 API。

#### 配置项

| 键          | 类型 | 默认值 | 描述           |
|:------------|:-----|:-------|:---------------|
| `"timeout"` | 整数 | `30`   | 请求超时秒数。 |


### Microsoft

`providers.microsoft`

微软的免费翻译 API。

#### 配置项

| 键          | 类型 | 默认值 | 描述           |
|:------------|:-----|:-------|:---------------|
| `"timeout"` | 整数 | `30`   | 请求超时秒数。 |


### Responses API

`providers.responses_api`

使用 OpenAI Responses API 调用语言模型来翻译。

#### 配置项

| 键              | 类型           | 默认值                                              | 描述                                 |
|:----------------|:---------------|:----------------------------------------------------|:-------------------------------------|
| `"endpoint"`    | 字符串         | `"https://api.openai.com/v1/responses"`             | API 端点 URI。                       |
| `"model"`       | 字符串 \| 空值 | `null`                                              | 模型 ID。                            |
| `"env_key"`     | 字符串 \| 空值 | `null`                                              | 包含 API 密钥的环境变量。            |
| `"context"`     | 布尔值         | `true`                                              | 是否将屏幕内容作为上下文发送给模型。 |
| `"headers"`     | 对象           | `{}`                                                | 包含在请求中的额外请求头。           |
| `"reasoning"`   | 字符串         | `"none"`                                            | 推理努力。                           |
| `"instruction"` | 字符串 \| 空值 | *见 [源代码](../../src/providers/responses_api.py)* | 给模型的系统提示词。                 |
| `"prompt"`      | 字符串 \| 空值 | *见 [源代码](../../src/providers/responses_api.py)* | 给模型的用户提示词。                 |
| `"temperature"` | 浮点数         | `0.0`                                               | 采样温度。                           |
| `"timeout"`     | 整数           | `120`                                               | 请求超时秒数。                       |
