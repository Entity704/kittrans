import json
import os
import typing
import urllib.request

DEFAULT_INSTRUCTION = '''\
You are a translator. Your only job is to translate the **Text to be translated** provided by the user into the specified target language.

## Rules:

- Faithful to the original text, without adding or omitting information, retaining the original tone and format
- "Context" is only used for understanding and disambiguation, and must not be translated or output
- If "Source language" is "auto", you need to guess the source language yourself

## Output format:

You must output valid **JSON** only, and:

- Do not use Markdown
- Do not wrap JSON in code fences
- Do not include explanations, comments, or text outside the JSON object

Parameters include:

- `"translation"`: the translated text
- `"guessed_language"` (optional): the guessed source language, only used when "Source language" is "auto", using **BCP 47** language tag

## Example (Does not include code block markers):

Input:

```text
Source language: auto
Target language: en-US

Context:
<context>
我上午和朋友一起出去玩了，今天天气真不错。
</context>

Text to be translated:
<source_text>
今天天气真不错。
</soutce_text>
```

Output:

```json
{
  "translation": "The weather is nice today.",
  "guessed_language": "zh-Hans"
}
```\
'''

DEFAULT_PROMPT = '''\
Source language: {source}
Target language: {target}

Context:
<context>
{context}
</context>

Text to be translated:
<source_text>
{source_text}
</soutce_text>\
'''

class Provider:
    def __init__(self, options: dict[str, typing.Any] = {}):
        self.options = options

        self.endpoint = options.get('endpoint', 'https://api.openai.com/v1/responses')
        self.model = options.get('model', '')
        self.env_key = options.get('env_key', None)

        self.api_key = None
        if self.env_key:
            self.api_key = os.getenv(self.env_key)

        self.headers = options.get('headers', {})
        self.reasoning = options.get('reasoning', 'none')
        self.instruction = options.get('instruction', DEFAULT_INSTRUCTION)
        self.prompt = options.get('prompt', DEFAULT_PROMPT)
        self.temperature = options.get('temperature', 0.0)

    def translate(
        self,
        text: str,
        target: str,
        source: str = 'auto',
        context: str = ''
    ) -> tuple[str, str]:
        headers = {}
        headers['Content-Type'] = 'application/json'
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        for key, value in self.headers:
            headers[key] = value

        data = {
            'model': self.model,
            'input': self.prompt.format(source=source, target=target, source_text=text, context=context),
            'instructions': self.instruction,
            'reasoning': {
                'effort': self.reasoning
            },
            'temperature': self.temperature,
            'stream': False
        }

        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(request, timeout=120) as response:
            response_data = json.loads(response.read().decode('utf-8'))

        result = json.loads(response_data['output'][0]['content'][0]['text'])

        source_lang = source
        if source == 'auto':
            source_lang = f'[auto]{result['guessed_language']}'

        return result['translation'], source_lang
