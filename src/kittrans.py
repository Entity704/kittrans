import os
import select
import sys

import kittens.tui.handler
import kittens.tui.loop
import kitty.boss
import kitty.utils

import handlers

def read_stdin(timeout: float = 0.5) -> str:
    fd = sys.stdin.fileno()

    ready, _, _ = select.select([fd], [], [], timeout)
    if not ready:
        return ''

    screen_size = kitty.utils.screen_size_function()()
    data = os.read(fd, max(4096, screen_size.cols * screen_size.rows * 4)).decode('utf-8')

    return data

def main(args: list[str]) -> str:
    text = text = args[1] if len(args) > 1 else ''
    context = read_stdin().strip('\n')

    if not text.strip() or text == '@selection':
        return ''

    handler = handlers.TranslationHandler(text, context)
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
