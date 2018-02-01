import string
import collections
#checks if files exist. If they do, try to open them
try:
    plain = open("input1.txt", "r")
    key = open("key1.txt", "r")
    output = open("output1.txt", "r")
except IOError:
    print('Could not find a file')
    exit()
#makes sure files are readable
try:
    pt = plain.read()
    kt = key.read()
except IOError:
    print('Could not read a file')
    exit()


for c in string.punctuation:
    pt = pt.replace(c, "")
    pt = pt.replace(" ", "")
print(pt)

#building vigenere square. Pulled from https://stackoverflow.com/questions/19882621/for-kasiski-test-how-to-implement-26x26-table-in-python

def vigsquare(printable=False):
    '''
    Returns a string like a vigenere square,
    printable joins each row with a newline so it's literally square
    printable=False (defaul) joins without newlines for easier
    searching by row and column index
    '''
    alpha = string.ascii_uppercase
    rotater = collections.deque(alpha)
    vigsquare_list = []
    for i in range(26):
        vigsquare_list.append(''.join(rotater))
        rotater.rotate(-1)
    if printable:
        return '\n'.join(vigsquare_list)
    else:
        return ''.join(vigsquare_list)
def vigenere(row, column):
    '''
    Return a character from a vigenere square by
    row and column letter.
    vigenere('L', 'G') returns 'R'
    '''
    alpha = string.ascii_uppercase
    rowindex = alpha.find(row)
    columnindex = alpha.find(column)
    return vigsquare()[rowindex*26 + columnindex]

print(vigsquare(printable=True))
print(vigenere('L', 'G'))



