import copy
import importlib
import json
import pathlib
import types
import typing

import kitty.constants

import kittrans_exception
import providers

KITTY_CONFIG_DIR = pathlib.Path(kitty.constants.config_dir)
BASE_DIR = KITTY_CONFIG_DIR / 'kittrans'
CONFIG_FILE = BASE_DIR / 'configs' / 'config.json'

DEFAULT_CONFIGURATION = {
    ('options' , dict): {},
    ('provider', str ): 'providers.microsoft',
    ('source'  , str ): 'auto',
    ('target'  , str ): None,

    ('providers.google.options', dict): {
        ('timeout', int): 30
    },

    ('providers.microsoft.options', dict): {
        ('timeout', int): 30
    },

    ('providers.responses_api.options', dict): {
        ('context'    , bool      ): True,
        ('endpoint'   , str       ): 'https://api.openai.com/v1/responses',
        ('env_key'    , str | None): None,
        ('headers'    , dict      ): {},
        ('instruction', str | None): None,
        ('model'      , str | None): None,
        ('reasoning'  , str       ): 'none',
        ('prompt'     , str | None): None,
        ('temperature', float     ): 0.0,
        ('timeout'    , int       ): 120,
    }
}

def is_none_allowed(expected_type) -> bool:
    if expected_type is type(None):
        return True
    elif isinstance(expected_type, types.UnionType):
        return type(None) in typing.get_args(expected_type)
    else:
        return False

def matches_type(value, expected_type) -> bool:
    if value is None:
        return is_none_allowed(expected_type)
    elif isinstance(expected_type, types.UnionType):
        return matches_type(value, typing.get_args(expected_type)[0])
    elif expected_type is int:
        return isinstance(value, int) and not isinstance(value, bool)
    else:
        return isinstance(value, expected_type)

def apply_defaults(
    config: dict[str, typing.Any],
    defaults: dict[tuple[str, type], typing.Any]
) -> dict[str, typing.Any]:
    for (key, expected_type), default_value in defaults.items():
        if key not in config:
            if default_value is None and not is_none_allowed(expected_type):
                kittrans_exception.raise_error(
                    KeyError,
                    f'Missing required field "{key}".'
                )

            if isinstance(default_value, dict):
                config[key] = apply_defaults({}, default_value)
            else:
                config[key] = copy.deepcopy(default_value)

            continue

        value = config[key]

        if not matches_type(value, expected_type):
            kittrans_exception.raise_error(
                ValueError,
                f'The value of "{key}" should not be {type(value).__name__}.'
            )

        if isinstance(default_value, dict):
            apply_defaults(value, default_value)

    return config

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

    return apply_defaults(config, DEFAULT_CONFIGURATION)

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
