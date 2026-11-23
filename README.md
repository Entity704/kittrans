# Kittrans

[ **English** | [**使简易化的中国人**](README_zh-Hans.md) ]

A simple translator for Kitty terminal emulator.

## Setting up

1. Copy the scripts to `~/.config/kitty/kittrans`
2. Add `map alt+shift+t kittrans/kittrans.py` to your config file (eg. `kitty.conf`)
3. Create `config.json` in kittrans directory and [configure it](#configure)

And then, you can select a string of text and press `alt+shift+t` to translate it.

## Configure

The config file uses JSON format.

Options:

- `"provider"`: the provider module path
- `"source"`: source language, `"auto"` for automatically detect
- `"target"`: target language
- `"options"`: extra options for providers (eg. API keys, endpoint URI)
