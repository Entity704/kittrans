# Kittrans

[ **English** | [**简体中文**](README_zh-Hans.md) ]

A simple translator for Kitty terminal emulator.

## Setting up

1. Copy the scripts to `~/.config/kitty/kittrans`
2. Add `map alt+shift+t kitten kittrans/kittrans.py @selection` to your config file (eg. `kitty.conf`)
3. Create `config.json` in kittrans directory and [configure it](#configure)

And then, you can select a string of text and press <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd> to translate it.

## Configure

The config file uses JSON format.

Options:

- `"provider"`: the provider module path
- `"source"`: source language, `"auto"` for automatically detect
- `"target"`: target language
- `"{provider}.options"`: extra options for providers (eg. API keys, endpoint URI)
