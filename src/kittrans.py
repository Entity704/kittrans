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
import kittrans_exception
import providers
import string_utils

KITTY_CONFIG_DIR = pathlib.Path(kitty.constants.config_dir)
BASE_DIR = KITTY_CONFIG_DIR / 'kittrans'
CONFIG_FILE = BASE_DIR / 'configs' / 'config.json'

def load_config() -> dict[str, typing.Any]:
    config = {}
    try:
        with open(CONFIG_FILE, encoding='utf-8') as file:
            config = json.load(file)
    except FileNotFoundError:
        kittrans_exception.raise_error(
            FileNotFoundError,
            f'Config file not found!\nPlease create one at `{CONFIG_FILE}`.'
        )
    except json.decoder.JSONDecodeError as error:
        kittrans_exception.raise_error(
            SyntaxError,
            'Failed to decode config file!\nPlease use a valid JSON format.',
            error,
            False
        )

    if not config.get('target'):
        kittrans_exception.raise_error(
            KeyError,
            'You must specify a target language by adding an entry with the\nkey "target" and a value in BCP 47 language tag format.'
        )

    return config

def load_provider(config: dict[str, typing.Any]) -> providers.Provider:
    provider_name = config.get('provider', 'providers.microsoft')

    try:
        module = importlib.import_module(provider_name)
    except ModuleNotFoundError:
        kittrans_exception.raise_error(ModuleNotFoundError, f'Provider module `{provider_name}` not found!')
    except Exception as error:
        kittrans_exception.raise_error(ImportError, 'Provider module appears internal error!', error)

    provider = getattr(module, 'Provider')

    options = config.get('options', {}) | config.get(f'{provider_name}.options', {})

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
        self.source = 'auto'
        self.target = 'undefined'

        self.error = None
        self.show_traceback = False

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
        except Exception as error:
            self.error = error

    def initialize(self):
        self.cmd.set_cursor_visible(False)
        self.draw()

    def draw(self):
        self.cmd.clear_screen()

        if not self.error:
            indent_size = 2 if self.screen_size.cols > 3 else 0
            max_width = max(1, min(80, self.screen_size.cols - indent_size - 1))

            text = '\r\n'.join(string_utils.wrap_text(self.text, max_width, indent_size))
            translation = '\r\n'.join(string_utils.wrap_text(self.translation, max_width, indent_size))

            self.print(f'{ansies.BOLD}Origin text {ansies.RESET}({self.source}):\n')
            self.print(f'{ansies.YELLOW}{text}{ansies.RESET}\n')

            self.print(f'{ansies.BOLD}Translation {ansies.RESET}({self.target}):\n')
            self.print(f'{ansies.CYAN}{translation}{ansies.RESET}\n')
        else:
            if isinstance(self.error, kittrans_exception.KittransError):
                self.print(f'{ansies.RED}[×] ', end='')
            else:
                self.print(f'{ansies.RED}[×] {type(self.error).__name__}: ', end='')

            self.print('\r\n'.join(string_utils.wrap_text(str(self.error), self.screen_size.cols - 1)))
            self.print()

            if self.show_traceback:
                self.print('Traceback:')
                self.print(
                    ''.join(
                        traceback.format_list(traceback.extract_tb(self.error.__traceback__))
                    ).replace('\n', '\r\n')
                )

            self.print(
                f'{ansies.DIM}{ansies.YELLOW}Press [m] to {'hide' if self.show_traceback else 'show'} traceback\r\n'
            )

            self.print(ansies.RESET, end='')

        self.print(f'{ansies.ITALIC}{ansies.DIM}Press [Enter], [Esc] or [Q] to quit{ansies.RESET}')

    def on_key(self, key_event):
        if key_event.key in ('ENTER', 'ESCAPE', 'q'):
            self.quit_loop(0)
        elif key_event.key == 'm' and self.error:
            self.show_traceback = not self.show_traceback
            self.draw()

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
