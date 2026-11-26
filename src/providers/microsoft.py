import json
import typing
import urllib.error
import urllib.parse
import urllib.request

import kittrans_exception

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
        source_lang = source if source != 'auto' else ''

        params = {
            'from': source_lang,
            'to': target,
            'isEnterpriseClient': 'false'
        }
        query = urllib.parse.urlencode(params)

        request = urllib.request.Request(
            f'https://edge.microsoft.com/translate/translatetext?{query}',
            data=json.dumps([text]).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as error:
            kittrans_exception.raise_error(
                urllib.error.HTTPError,
                f'Provider returns HTTP {error.code} ({error.reason}).'
            )
        except TimeoutError as error:
            kittrans_exception.raise_error(
                TimeoutError,
                'Request timed out.'
            )
        except ConnectionError as error:
            kittrans_exception.raise_error(
                ConnectionError,
                f'Failed to connect to provider: {str(error)}.'
            )

        if source == 'auto':
            source_lang = f'[auto]{result[0]['detectedLanguage']['language']}, {round(result[0]['detectedLanguage']['score'] * 100)}%'

        return result[0]['translations'][0]['text'], source_lang
