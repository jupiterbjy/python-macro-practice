from Toolset import MemberLoader

COLORIZE_ENABLE = False


def rgbToHex(r=0, g=0, b=0):
    arr = [r, g, b]
    out = [str(hex(i))[2:] for i in arr]
    return '#' + ''.join(out)


def QtColorize(text, color=(0, 0, 0), size=None, weight=None):
    if COLORIZE_ENABLE:
        start = '<span style=\" '
        font = f'font-size:{size}pt; ' if size else ''
        font_weight = f'font-weight:{weight}; ' if size else ''
        color = f'color:{rgbToHex(*color)}; '
        end = '\" >'
        txt = str(text)
        span_complete = '</span>'

        out = [start, font, font_weight, color, end, txt, span_complete]

        return ''.join(out)

    return text


class ANSI_C:
    
    RED = '\033[91m'
    GRN = '\033[92m'
    BLU = '\033[94m'
    YEL = '\033[93m'
    PUR = '\033[94m'
    CYA = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'
    HEADER = '\033[95m'
    UNDERLINE = '\033[4m'
    
    table = {
        "RED": '\033[91m',
        "GREEN": '\033[92m',
        "BLUE": '\033[94m',
        "YELLOW": '\033[93m',
        "PURPLE": '\033[94m',
        "CYAN": '\033[96m',
        "END": '\033[0m',
        "BOLD": '\033[1m',
        "HEADER": '\033[95m',
        "UNDERLINE": '\033[4m',
    }


def C_list(idx):
    return ANSI_C.table[list(ANSI_C.table.keys())[idx]]


def TerminalColorize(txt, color):
    s = str(txt)
    return ANSI_C.table[color] + s + ANSI_C.table["END"]
        

__all__ = MemberLoader.ListFunction(__name__, prefix_mode=True)
