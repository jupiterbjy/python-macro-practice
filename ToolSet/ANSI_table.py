from ToolSet import MemberLoader


def Check_CMD():
    from psutil import Process
    import os
    if 'exe' in Process(os.getpid()).parent().name():
        return True
    else:
        return False

    
def Clear_Screen(Run = []):

    ''''Uses kwarg list's global-like property to store state'''
    import os
    
    if not Run:
        Run.append(Check_CMD())
    
    if Run[0]:
        os.system('cls')
    else:
        os.system('clear')

    
def Check_ANSI(output=True):
    if Check_CMD():
        
        if output:
            print("ANSI incompetible, Importing Colorama.init")
            
        from colorama import init
        init()
        
    else:
        if output:
            print("Running on ANSI compatable Terminal.")

    
class ANSI_C():
    
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
        "RED" : '\033[91m',
        "GRN" : '\033[92m',
        "BLU" : '\033[94m',
        "YEL" : '\033[93m',
        "PUR" : '\033[94m',
        "CYA" : '\033[96m',
        "END" : '\033[0m',
        "BOLD" : '\033[1m',
        "HEADER" : '\033[95m',
        "UNDERLINE" : '\033[4m',
    }
    
def C_list(idx):
    return ANSI_C.table[list(ANSI_C.table.keys())[idx]]
    
def Colorize(txt, color):
    s = str(txt)
    return ANSI_C.table[color] + s + ANSI_C.table["END"]
        
    
    
__all__ = MemberLoader.ListFunction(__name__, prefix_mode= True)
__all__.append('ANSI_C')
