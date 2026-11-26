# Kittrans

[ **English** | [**简体中文**](docs/zh-Hans/README.md) ]

A simple translator for [Kitty](https://sw.kovidgoyal.net/kitty/) terminal emulator.

[![Release](https://img.shields.io/github/v/release/Entity704/kittrans?style=flat-square&logo=github&logoColor=979DA4&label=Release&labelColor=24292E&color=blue)](https://github.com/Entity704/kittrans/releases/latest)
![WIP](https://img.shields.io/badge/Status-Work%20in%20Progress-orange?style=flat-square&labelColor=24292E)


## Setting up

1. Copy the scripts to your Kitty's config directory (probably `~/.config/kitty/kittrans`)
2. Add `map alt+shift+t kitten kittrans/src/kittrans.py @selection` to your config file (eg. `kitty.conf`)
3. Create `config.json` in `configs` directory and [configure it](#configure)

And then, you can select a string of text and press <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd> to translate it.


## Configure

The config file uses JSON format.

Options:

- `"provider"`: the provider module path
- `"source"`: source language, using [BCP 47](https://www.rfc-editor.org/info/rfc5646/) language tag in Language-Script-Region format. `"auto"` for automatically detect
- `"target"`: target language, using BCP 47 language tag in Language-Script-Region format
- `"options"`: extra options for all providers (values can be overwritten by the value of the same key in `"{provider}.options"`)
- `"{provider}.options"`: extra options for specified providers (eg. API keys, endpoint URI)


## Provider Modules

See [Provider Modules](docs/provider-modules.md).
