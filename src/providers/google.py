import json
import typing
import urllib.parse
import urllib.request

GOOGLE_TRANSLATE_PA_API_KEY = 'AIzaSyDLEeFI5OtFBwYBIoK_jj5m32rZK5CkCXA'

class Provider:
    def __init__(self, options: dict[str, typing.Any] = {}):
        self.options = options

    def translate(
        self,
        text: str,
        target: str,
        source: str = 'auto',
        context: str = ''
    ) -> tuple[str, str]:
        params = {
            'params.client': 'gtx',
            'query.source_language': source,
            'query.target_language': target,
            'query.text': text,
            'key': GOOGLE_TRANSLATE_PA_API_KEY,
            'data_types': 'TRANSLATION'
        }
        query = urllib.parse.urlencode(params)

        request = urllib.request.Request(
            f'https://translate-pa.googleapis.com/v1/translate?{query}',
            method='GET'
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))

        source_lang = source
        if source == 'auto':
            source_lang = f'[auto]{result['detectedLanguages']['srclangs'][0]}, {round(result['detectedLanguages']['srclangsConfidences'][0] * 100, 2)}%'

        return result['translation'], source_lang
