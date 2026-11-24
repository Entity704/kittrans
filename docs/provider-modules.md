# Kittrans | Provider Modules

[ **English** | [**简体中文**](zh-Hans/provider-modules.md) ]


## Customize your own providers

See [provider template](../src/providers/__init__.py).


## Built-in Modules

### Microsoft

`providers.microsoft`

Microsoft's free translate API.


### Responses API

`providers.responses_api`

Uses OpenAI Responses API to call language models to translate.

#### Options

| Key             | Type   | Default value                                          | Description                                          |
|:----------------|:-------|:-------------------------------------------------------|:-----------------------------------------------------|
| `"endpoint"`    | String | `"https://api.openai.com/v1/responses"`                | API endpoint URI.                                    |
| `"model"`       | String | `""`                                                   | Model ID.                                            |
| `"env_key"`     | String | `null`                                                 | Environment variable name which contains an API key. |
| `"headers"`     | Object | `{}`                                                   | Extra headers to send to the endpoint.               |
| `"reasoning"`   | String | `"none"`                                               | Reasoning effort.                                    |
| `"instruction"` | String | *See [source code](../src/providers/responses_api.py)* | System prompt for the model.                         |
| `"prompt"`      | String | *See [source code](../src/providers/responses_api.py)* | User prompt for the model.                           |
| `"temperature"` | Number | `0.0`                                                  | Sampling temperature.                                |
