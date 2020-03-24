from Toolset import MemberLoader


def rgbToHex(r=0, g=0, b=0):
    arr = [r, g, b]
    out = []
    for i in arr:
        if i < 16:
            out.append('0' + str(hex(i))[2:])
        else:
            out.append(str(hex(i))[2:])
    return '#' + ''.join(out)


def QtColorize(text, color=(0, 0, 0), size=None, weight=None):
    start = '<span style=\" '
    font = f'font-size:{size}pt; '
    font_weight = f'font-weight:{weight}; '
    color = f'color:{rgbToHex(*color)}; '
    end = '\" >'
    txt = str(text)
    span_complete = '</span>'

    out = [start, font, font_weight, color, end, txt, span_complete]

    if size is None:
        out.remove(font)

    if weight is None:
        out.remove(font_weight)

    return ''.join(out)


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
