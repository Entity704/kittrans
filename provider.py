from typing import Protocol

class ProviderProtocol(Protocol):
    def __init__(self, options: list[str] = []):
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
