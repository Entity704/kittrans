import json
import importlib, pathlib, os, sys, select

import kitty, kittens

import ansies, text_wrapper
import providers

BASE_DIR = pathlib.Path(
    os.path.expanduser('~/.config/kitty/kittrans/')).resolve()
CONFIG_FILE = BASE_DIR / 'config.json'

def load_config():
    with open(CONFIG_FILE, encoding='utf-8') as f:
        return json.load(f)

def load_provider(config):
    provider_name = config.get('provider', 'providers.microsoft')

    module = importlib.import_module(provider_name)
    provider = getattr(module, 'Provider')

    return provider(config.get('options', {}))

def read_stdin(timeout=0.5):
    fd = sys.stdin.fileno()

    ready, _, _ = select.select([fd], [], [], timeout)

    if not ready:
        return ''

    return os.read(fd, 16 * 1024 * 1024).decode('utf-8')

class Handler(kittens.tui.handler.Handler):
    def __init__(self, text: str):
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
                source=config.get('source', 'auto'),
                target=self.target,
            )
        except Exception as err:
            self.error = f'Error: {err}'

    def initialize(self):
        self.cmd.set_cursor_visible(False)
        self.draw()

    def draw(self):
        if not self.error:
            text = text_wrapper.wrap_text(self.text, 80, 1)
            translation = text_wrapper.wrap_text(self.translation, 80, 1)

            self.print(f'{ansies.ITALIC}Origin text {ansies.RESET}({self.source}):\n')
            for line in text:
                self.print(line)
            self.print('\n')

            self.print(f'{ansies.ITALIC}Translation {ansies.RESET}({self.target}):\n{ansies.BOLD}')
            for line in translation:
                self.print(line)
            self.print(f'{ansies.RESET}\n')
        else:
            self.print(f'{ansies.RED}[×] {self.error}{ansies.RESET}\n')

        self.print(f'{ansies.DIM}Press [Enter], [Esc] or [Q]...{ansies.RESET}')

    def on_key(self, key_event):
        if key_event.key in ('ENTER', 'ESCAPE', 'q'):
            self.quit_loop(0)

    def on_resize(self, new_size):
        self.draw()

def main(args: list[str]) -> str:
    text = read_stdin()

    if not text.strip():
        return ''

    handler = Handler(text)
    kittens.tui.loop.Loop().loop(handler)

    return ''

@kittens.tui.handler.result_handler(type_of_input='selection')
def handle_result(
    args: list[str],
    answer: str,
    target_window_id: int,
    boss: kitty.boss.Boss
) -> None:
    pass
