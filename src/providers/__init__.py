import typing

class Provider(typing.Protocol):
    def __init__(self, options: dict[str, typing.Any] = {}):
        ...

    def translate(
        self,
        text: str,
        target: str,
        source: str = 'auto',
        context: str = ''
    ) -> tuple[str, str]:
        '''
        Translate text

        Args:
            text (str): Original text
            target (str): Target language
            source (str): Source language
            context (str): Context

        Returns:
            tuple[str, str]: Translated text and detected source language
        '''

        ...
