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

KITTRANS_VERSION_MAJOR = 0
KITTRANS_VERSION_MINOR = 1
KITTRANS_VERSION_PATCH = 0
KITTRANS_VERSION_SUFFIX = ''

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

        self.pager = string_utils.Pager('')

    def initialize(self):
        self.cmd.set_cursor_visible(False)
        self.draw()

    def draw(self):
        self.cmd.clear_screen()

        if not self.error:
            self.print(
                f' {ansies.BOLD}Kittrans{ansies.RESET}'
                + f' v{KITTRANS_VERSION_MAJOR}.{KITTRANS_VERSION_MINOR}.{KITTRANS_VERSION_PATCH}'
                + f'{'-' + KITTRANS_VERSION_SUFFIX if KITTRANS_VERSION_SUFFIX else ''}'
            )
            self.print('=' * 96)
            self.print()

            indent_size = 4 if self.screen_size.cols > 4 + 1 else 0
            max_width = max(1, min(96 - indent_size * 2, self.screen_size.cols - indent_size - 1))
            self.pager.max_rows = max(1, self.screen_size.rows - 10)

            text = '\n'.join(string_utils.wrap_text(self.text, max_width, indent_size))
            translation = '\n'.join(string_utils.wrap_text(self.translation, max_width, indent_size))

            content = f'  {ansies.BOLD}Origin text {ansies.RESET}({self.source}):\n\n'
            content += f'{ansies.YELLOW}{text}{ansies.RESET}\n\n\n'
            content += f'  {ansies.BOLD}Translation {ansies.RESET}({self.target}):\n\n'
            content += f'{ansies.CYAN}{translation}{ansies.RESET}'
            self.pager.content = content
            self.pager.clip_row()

            self.print('\r\n'.join(self.pager.get_view()) + ansies.RESET)

            lines_left = self.pager.rows() - self.pager.max_rows - self.pager.row

            if lines_left > 0:
                self.print(
                    ansies.BOLD
                    + f'... {lines_left} line{'s' if lines_left > 1 else ''} left'
                    + ansies.RESET,
                    end='\r\n\n'
                )
            else:
                self.print(end='\r\n\n')

            if content.count('\n') + 1 > self.pager.max_rows:
                self.print(
                    f'At line {
                        string_utils.pad(
                            str(self.pager.row + 1),
                            len(str(self.pager.rows() - self.pager.max_rows + 1)),
                            '0',
                            ansies.DIM,
                            ansies.RESET
                        )
                    }, '
                    + f'{
                        string_utils.pad(
                            str(round(self.pager.progress() * 100)),
                            3,
                            '0',
                            ansies.DIM,
                            ansies.RESET
                        )
                    }%'
                    + ' | '
                    + f'{ansies.YELLOW}Origin text{ansies.RESET}, {ansies.CYAN}Translation{ansies.RESET}'
                )

                self.print(
                    ansies.DIM
                    + f'{ansies.BOLD}[PageUp]{ansies.RESET}{ansies.DIM}: scroll up'
                    + f' | {ansies.BOLD}[PageDown]{ansies.RESET}{ansies.DIM}: scroll down'
                    + f' | {ansies.BOLD}[↑]{ansies.RESET}{ansies.DIM}: scroll up one line'
                    + f' | {ansies.BOLD}[↓]{ansies.RESET}{ansies.DIM}: scroll down one line'
                    + ansies.RESET,
                    end='\r\n\n'
                )
            else:
                self.print(end='\r\n\n\n')
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
                f'{ansies.DIM}{ansies.YELLOW}Press '
                + f'{ansies.BOLD}[m]{ansies.UNSET_BOLD_AND_DIM}{ansies.DIM}'
                + f' to {'hide' if self.show_traceback else 'show'} traceback',
                end='\r\n\n'
            )

            self.print(ansies.RESET, end='')

        self.print(
            f'{ansies.ITALIC}{ansies.DIM}Press '
            + f'{ansies.RESET}{ansies.BOLD}{ansies.DIM}[Enter]{ansies.RESET}{ansies.ITALIC}{ansies.DIM}'
            + f', {ansies.RESET}{ansies.BOLD}{ansies.DIM}[Esc]{ansies.RESET}{ansies.ITALIC}{ansies.DIM}'
            + f' or {ansies.RESET}{ansies.BOLD}{ansies.DIM}[Q]{ansies.RESET}{ansies.ITALIC}{ansies.DIM}'
            + f' to quit{ansies.RESET}'
        )

    def on_key(self, key_event):
        if key_event.key in ('ENTER', 'ESCAPE', 'q') and key_event.type == kitty.key_encoding.EventType.RELEASE:
            self.quit_loop(0)
            return

        if not self.error:
            if key_event.type not in (kitty.key_encoding.EventType.PRESS, kitty.key_encoding.EventType.REPEAT):
                return

            if key_event.key == 'PAGE_UP': self.pager.page_up()
            elif key_event.key == 'PAGE_DOWN': self.pager.page_down()
            elif key_event.key == 'UP': self.pager.page_up(1)
            elif key_event.key == 'DOWN': self.pager.page_down(1)

            self.draw()
        else:
            if key_event.key == 'm':
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
