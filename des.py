import string
import collections
#checks if files exist. If they do, try to open them
try:
    plain = open("input1.txt", "r")
    key = open("key1.txt", "r")
    output = open("output1.txt", "w")
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

# building vigenere square. Pulled from https://stackoverflow.com/questions/19882621/for-kasiski-test-how-to-implement-26x26-table-in-python

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
# print(vigenere('L', 'G'))
# mnext step-run vigenere(plaintext, key) character by character until the end of the plain text.
# Repeat the key when needed(every 16 chars)
i = 0

poly = ''
output.write("Poly Sub")
# i val also helps with the padding step
for c in pt:
    if i == 16:
        i = 0;
    poly += vigenere(c, kt[i])
    output.write(vigenere(c, kt[i]))
    i += 1

# padding for 4x4 blocks
while i < 16:
    poly += "A"
    output.write("Padding")
    output.write("A")
    i += 1

# start shifting
blockNum = poly.__len__() / 16
i = 0       # total text indexing
j = 0       # inside block indexing
#while blockNum > 0:
#    row1 = poly[0 + i: i + 4]
#    row2 = poly[4 + i:4 + i + 4]
 #   row3 = poly[8 + i:8 + i + 4]
  #  row4 = poly[12 + i: 12 + i + 4]
    #print(row1, row2, row3, row4)
   # blockNum -= 1
    #i += 16

while blockNum > 0:
    row1 = poly[0 + i: i + 4]
    row2 = poly[4 + i:4 + i + 4]
    row2 = row2[1:]+row2[:1]
    poly[4 + i: 4 + i + 4] = row2       #FIX THIS. STRINGS ARE IMMUTABLE
    row3 = poly[8 + i:8 + i + 4]
    row3 = row3[2:]+row3[:2]
    poly[8 + i: 8 + i + 4] = row3
    row4 = poly[12 + i: 12 + i + 4]
    row4 = row4[3:]+row4[:3]
    poly[12 + i: 12 + i + 4] = row4
    # print(row1, a, b, c)
    #print(row1)
    #print(row2)
    #print(row3)
    #print(row4 + '\n')
    blockNum -= 1
    i += 16

print("HERE")
print(poly)







