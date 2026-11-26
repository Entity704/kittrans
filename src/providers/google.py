import json
import re
import typing
import urllib.error
import urllib.parse
import urllib.request

import kittrans_exception

GOOGLE_TRANSLATE_PA_API_KEY = 'AIzaSyDLEeFI5OtFBwYBIoK_jj5m32rZK5CkCXA'

def convert_lc(lsr_tag):
    if lsr_tag == 'auto': return 'auto'

    match = re.search(r'(([a-z]{2})-([a-z]{4})-([a-z]{2}))', lsr_tag, re.IGNORECASE)
    if match:
        return f'{match.group(2).lower()}-{match.group(4).upper()}'
    else:
        kittrans_exception.raise_error(
            ValueError,
            f'Invalid language tag: "{lsr_tag}".'
        )

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
        source = convert_lc(source)
        target = convert_lc(target)

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

        try:
            with urllib.request.urlopen(request, timeout=self.options.get('timeout', 30)) as response:
                result = json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as error:
            kittrans_exception.raise_error(
                urllib.error.HTTPError,
                f'Provider returns HTTP {error.code} ({error.reason}).'
            )
        except TimeoutError:
            kittrans_exception.raise_error(
                TimeoutError,
                'Request timed out.'
            )
        except ConnectionError as error:
            kittrans_exception.raise_error(
                ConnectionError,
                f'Failed to connect to provider: {str(error)}.'
            )

        source_lang = source
        if source == 'auto':
            source_lang = f'[auto]{result['detectedLanguages']['srclangs'][0]}, {round(result['detectedLanguages']['srclangsConfidences'][0] * 100, 2)}%'

        return result['translation'], source_lang
