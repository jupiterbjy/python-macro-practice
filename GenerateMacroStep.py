import time
import sys


class MacroStep:
    def __init__(self, index, imagename, priordelay, option):
        self.Index = index
        self.imgName = imagename
        self.pDelay = priordelay
        self.Option = option


def TStr():
    now = time.gmtime(time.time())
    string_a = [now.tm_year, now.tm_mon, now.tm_mday]
    string_b = [now.tm_hour, now.tm_min, now.tm_sec]
    string_c = string_a + string_b
    out = '{}.{}.{} {}:{}:{}'.format(*string_c)

    # TimeString. Did this mess to reduce horizontal length!
    # Asterisk almost looks like pointer, wow.
    # Actually just unpacking string, how boring.

    return out


def FileAvailable(name):
    global new_file
    global macro_s_point

    macro_s_point = 0
    new_file = False

    while True:
        try:
            with open(name, 'r', encoding='utf-8') as f:
                lines = f.readlines()

        except FileNotFoundError:
            with open(name, 'w', encoding='utf-8') as f:

                print('file not found, creating template.')

                # <Today's Grammar Class>
                # Created in 3 hours / Created on the 13th of July
                # Created at 2013-07-13 14:35 / Created on 2013-07-13

                f.write('@1 Created at  : {}\n'.format(TStr()))
                f.write('@2 Last Access : {}\n'.format(TStr()))
                f.write('# Macro Data Starts\n')

            new_file = True

        else:
            try:
                lines[2]

            except IndexError:
                print('File contains barely nothing!')
                print('Check if you chose correct file, or remove it!')
                print('Script shutdown in 10 seconds.')

                time.sleep(10)
                sys.exit()

            else:
                if ('@1' in lines[0]) and ('@2' in lines[1]):

                    # if file contains those, consider it normal

                    print('file Loaded:', name)
                    print(lines[0], lines[1], sep='')

                    lines[1] = '@2 Last Access : %s' % TStr()

                    with open(name, 'w', encoding='utf-8') as f2:
                        for line in lines:
                            f2.write("%s\n" % line)

                    return lines

                else:
                    print('No creation Date or Last access date is found')
                    print('Performing basic file integrity check', end='')
                    symbol = ['.', '..', '...']

                    global file_integrity

                    file_integrity = False

                    num_lines = sum(1 for _ in f)

                    for i in range(num_lines):
                        print(symbol[i % 3])

                        if '#' in lines[i]:
                            macro_s_point = i
                            file_integrity = True
                            break

                    if file_integrity:
                        return lines

                    else:
                        NameError('File integrity damaged!')
                        print('Script shutdown in 10 seconds.')
                        time.sleep(10)
                        sys.exit()


'''
def GenerateFile():
    
    f_lines = FileAvailable(input())
    
    while True:
        print("Entry for @", macro_s_point, sep='')
        temp = [input()]
        
        f_lines[macro_s_point] = 
'''
