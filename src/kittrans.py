import importlib
import json
import os
import pathlib
import select
import sys
import traceback
import typing

import kittens.tui.handler
import kittens.tui.loop
import kitty.boss
import kitty.constants
import kitty.utils

import ansies
import providers
import string_utils

KITTY_CONFIG_DIR = pathlib.Path(kitty.constants.config_dir)
BASE_DIR = KITTY_CONFIG_DIR / 'kittrans'
CONFIG_FILE = BASE_DIR / 'configs' / 'config.json'

def load_config() -> dict[str, typing.Any]:
    with open(CONFIG_FILE, encoding='utf-8') as f:
        return json.load(f)

def load_provider(config: dict[str, typing.Any]) -> providers.Provider:
    provider_name = config.get('provider', 'providers.microsoft')

    module = importlib.import_module(provider_name)
    provider = getattr(module, 'Provider')

    options = config.get(f'{provider_name}.options', config.get('options', {}))

    return provider(options)

def read_stdin(timeout: float = 0.5) -> str:
    fd = sys.stdin.fileno()

    ready, _, _ = select.select([fd], [], [], timeout)
    if not ready:
        return ''

    screen_size = kitty.utils.screen_size_function()()
    data = os.read(fd, max(4096, screen_size.cols * screen_size.rows * 4)).decode('utf-8')

    return data

class Handler(kittens.tui.handler.Handler):
    def __init__(self, text: str, context: str = ''):
        super().__init__()
        self.text = text

        self.translation = ''
        self.source = 'unknown'
        self.target = 'undefined'
        self.error = ''

        try:
            config = load_config()

            self.target = config.get('target', 'zh-Hans')

            provider = load_provider(config)

            self.translation, self.source = provider.translate(
                text=text,
                target=self.target,
                source=config.get('source', 'auto'),
                context=context
            )
        except Exception as err:
            self.error = f'Error: {err}\n{traceback.format_exc()}'

    def initialize(self):
        self.cmd.set_cursor_visible(False)
        self.draw()

    def draw(self):
        self.cmd.clear_screen()

        if not self.error:
            indent_size = 2 if self.screen_size.cols > 3 else 0
            max_width = max(1, min(80, self.screen_size.cols - indent_size - 1))

            text = string_utils.wrap_text(self.text, max_width, indent_size)
            translation = string_utils.wrap_text(self.translation, max_width, indent_size)

            self.print(f'{ansies.BOLD}Origin text {ansies.RESET}({self.source}):\n{ansies.YELLOW}')
            for line in text:
                self.print(line)
            self.print(f'{ansies.RESET}\n')

            self.print(f'{ansies.BOLD}Translation {ansies.RESET}({self.target}):\n{ansies.CYAN}')
            for line in translation:
                self.print(line)
            self.print(f'{ansies.RESET}\n')
        else:
            self.print(f'{ansies.RED}[×] ', end='')
            for line in string_utils.wrap_text(self.error, self.screen_size.cols - 1):
                self.print(line)
            self.print(ansies.RESET)

        self.print(f' {ansies.ITALIC}{ansies.DIM}Press [Enter], [Esc] or [Q]...{ansies.RESET}')

    def on_key(self, key_event):
        if key_event.key in ('ENTER', 'ESCAPE', 'q'):
            self.quit_loop(0)

    def on_resize(self, new_size):
        self.draw()

def main(args: list[str]) -> str:
    text = text = args[1] if len(args) > 1 else ''
    context = read_stdin().strip('\n')

    if not text.strip() or text == '@selection':
        return ''

    handler = Handler(text, context)
    kittens.tui.loop.Loop().loop(handler)

    return ''

@kittens.tui.handler.result_handler(type_of_input='text')
def handle_result(
    args: list[str],
    answer: str,
    target_window_id: int,
    boss: kitty.boss.Boss
) -> None:
    pass
