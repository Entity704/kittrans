def wrap_text(
    text: str,
    clip_width: int,
    indent: int = 0
) -> list[str]:
    lines = text.split('\n')

    indent_str = ' ' * indent

    row = 0
    while row < len(lines):
        line = lines[row]

        if len(line) > clip_width:
            lines.insert(row + 1, line[clip_width:])
            lines[row] = line[:clip_width] + '⏎'

        lines[row] = indent_str + lines[row]
        row += 1

    return lines
