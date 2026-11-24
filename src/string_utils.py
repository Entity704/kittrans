import unicodedata

SPECIAL_WIDTH_MAP = {
    '“': 'H',
    '”': 'H',
    '‘': 'H',
    '’': 'H'
}

def is_full_width(char: str) -> bool:
    if char in SPECIAL_WIDTH_MAP and SPECIAL_WIDTH_MAP[char] == 'H':
        return False
    return unicodedata.east_asian_width(char) in ('F', 'W')

def char_width_of(char: str) -> int:
    return 2 if is_full_width(char) else 1

def text_width(text: str) -> int:
    return sum(char_width_of(char) for char in text)

def wrap_text(
    text: str,
    clip_width: int,
    indent: int = 0
) -> list[str]:
    text = text.replace('\t', ' ' * 4)
    lines = text.split('\n')

    indent_str = ' ' * indent

    row = 0
    while row < len(lines):
        line = lines[row].rstrip()

        width = 0
        for index, char in enumerate(line):
            char_width = char_width_of(char)

            if width + char_width > clip_width:
                if index > 0:
                    curr_line = line[:index]
                    next_line = line[index:]

                    curr_line_width = text_width(curr_line)
                    padding = clip_width - curr_line_width

                    lines[row] = curr_line + ' ' * padding + '⏎'
                    lines.insert(row + 1, next_line)
                break

            width += char_width

        lines[row] = indent_str + lines[row]
        row += 1

    return lines
