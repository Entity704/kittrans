import json
import urllib.request

class Provider:
    def __init__(self, options: list[str] = []):
        pass

    def translate(
        self,
        text: str,
        target: str,
        source: str = 'auto',
        context: str = ''
    ) -> tuple[str, str]:
        source_lang = source if source != 'auto' else ''

        request = urllib.request.Request(
            f'https://edge.microsoft.com/translate/translatetext?from={source_lang}&to={target}&isEnterpriseClient=false',
            data=json.dumps([text]).encode('utf-8'),
            headers={
                'Content-Type': 'application/json'
            },
            method='POST'
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))

        if source == 'auto':
            source_lang = f'[auto]{result[0]['detectedLanguage']['language']}, {round(result[0]['detectedLanguage']['score'] * 100)}%'

        return result[0]['translations'][0]['text'], source_lang
