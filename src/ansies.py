RESET       = '\033[0m'
BOLD        = '\033[1m'
DIM         = '\033[2m'
ITALIC      = '\033[3m'
UNDERLINE   = '\033[4m'
BLINK       = '\033[5m'
RAPID_BLINK = '\033[6m'
INVERSE     = '\033[7m'
HIDDEN      = '\033[8m'
DELETE      = '\033[9m'

UNSET_BOLD_AND_DIM = '\033[22m'
UNSET_ITALIC       = '\033[23m'
UNSET_UNDERLINE    = '\033[24m'
UNSET_BLINK        = '\033[25m'
UNSET_RAPID_BLINK  = '\033[26m'
UNSET_INVERSE      = '\033[27m'
UNSET_HIDDEN       = '\033[28m'
UNSET_DELETE       = '\033[29m'

BLACK   = '\033[30m'
RED     = '\033[31m'
GREEN   = '\033[32m'
YELLOW  = '\033[33m'
BLUE    = '\033[34m'
MAGENTA = '\033[35m'
CYAN    = '\033[36m'
WHITE   = '\033[37m'
DEFAULT = '\033[39m'

BRBLACK   = '\033[90m'
BRRED     = '\033[91m'
BRGREEN   = '\033[92m'
BRYELLOW  = '\033[93m'
BRBLUE    = '\033[94m'
BRMAGENTA = '\033[95m'
BRCYAN    = '\033[96m'
BRWHITE   = '\033[97m'

BLACK_BG   = '\033[40m'
RED_BG     = '\033[41m'
GREEN_BG   = '\033[42m'
YELLOW_BG  = '\033[43m'
BLUE_BG    = '\033[44m'
MAGENTA_BG = '\033[45m'
CYAN_BG    = '\033[46m'
WHITE_BG   = '\033[47m'
DEFAULT_BG = '\033[49m'

BRBLACK_BG   = '\033[100m'
BRRED_BG     = '\033[101m'
BRGREEN_BG   = '\033[102m'
BRYELLOW_BG  = '\033[103m'
BRBLUE_BG    = '\033[104m'
BRMAGENTA_BG = '\033[105m'
BRCYAN_BG    = '\033[106m'
BRWHITE_BG   = '\033[107m'

def color256(index: int) -> str:
    return f'\033[38;5;{index}m'

def color256_bg(index: int) -> str:
    return f'\033[48;5;{index}m'

def rgb(r: int, g: int, b: int) -> str:
    return f'\033[38;2;{r};{g};{b}m'

def rgb_bg(r: int, g: int, b: int) -> str:
    return f'\033[48;2;{r};{g};{b}m'
