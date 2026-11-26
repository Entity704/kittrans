import re
import unicodedata

ANSI_SGR_RE = re.compile(r'\033\[[0-9;]*m')

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
    text = text.replace('\r\n', '\n')
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

def pad(
    text: str,
    width: int,
    char: str = '0',
    prefix: str = '',
    suffix: str = ''
) -> str:
    text = str(text)
    padding = char * max(0, width - len(text))
    return f'{prefix}{padding}{suffix}{text}'

class Pager:
    def __init__(self, content: str, max_rows: int = 1, row: int = 0):
        self.content = content.replace('\r\n', '\n')
        self.max_rows = max_rows
        self._row = row

    @property
    def row(self) -> int:
        self.clip_row()
        return self._row

    @row.setter
    def row(self, value):
        self._row = value
        self.clip_row()

    def clip_row(self): self._row = max(0, min(self.rows() - self.max_rows, self._row))
    def page_up(self, rows: int = 15): self.row -= rows
    def page_down(self, rows: int = 15): self.row += rows

    def rows(self) -> int: return self.content.count('\n') + 1
    def progress(self) -> float: return self.row / max(1, self.rows() - self.max_rows)

    def get_view(self) -> list[str]:
        lines = self.content.split('\n')
        lines.extend([''] * self.max_rows)

        view = lines[self.row:self.row + self.max_rows]
        view[0] = ''.join(ANSI_SGR_RE.findall('\n'.join(lines[:self.row]))) + view[0]

        return view
