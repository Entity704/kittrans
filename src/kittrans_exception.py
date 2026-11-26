import traceback
import typing

class KittransError(Exception):
    pass

def raise_error(
    error_type: type[Exception],
    message: str,
    origin: BaseException | None = None,
    show_origin_tb: bool = True
) -> typing.NoReturn:
    error_message = f'(Kittrans) {error_type.__name__}:' + ('\n' + message).replace('\n', '\n  ')

    if origin:
        error_message += f'\n\nOrigin error ({type(origin).__name__}):\n  {str(origin)}'

        if show_origin_tb and origin.__traceback__:
            error_message += '\n\nOrigin error traceback:\n'
            error_message += ''.join(traceback.format_list(traceback.extract_tb(origin.__traceback__)))

    raise KittransError(error_message) from origin
