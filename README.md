# Kittrans

[ **English** | [**简体中文**](docs/zh-Hans/README.md) ]

A simple translator for Kitty terminal emulator.


## Setting up

1. Copy the scripts to your Kitty's config directory (probably `~/.config/kitty/kittrans`)
2. Add `map alt+shift+t kitten kittrans/src/kittrans.py @selection` to your config file (eg. `kitty.conf`)
3. Create `config.json` in `configs` directory and [configure it](#configure)

And then, you can select a string of text and press <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd> to translate it.


## Configure

The config file uses JSON format.

Options:

- `"provider"`: the provider module path
- `"source"`: source language, `"auto"` for automatically detect
- `"target"`: target language
- `"{provider}.options"`: extra options for providers (eg. API keys, endpoint URI)


## Provider Modules

See [Provider Modules](docs/provider-modules.md).
