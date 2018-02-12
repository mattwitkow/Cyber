import collections
import string
import numpy as np
#checks if files exist. If they do, try to open them
try:
    plain = open("input.txt", "r")
    key = open("key.txt", "r")
    output = open("output.txt", "w")
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


#pt = pt.translate(string.punctuation)
print(pt)
exclude = set(string.punctuation)
pt = ''.join(ch for ch in pt if ch not in exclude)
pt = pt.replace('\n', '').replace('\r', '')
output.write("preprocessing" + '\n')
output.write(pt + '\n')
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
output.write("Poly Sub" + '\n')
# i val also helps with the padding step
for c in pt:
    if i == 16:
        i = 0;
    poly += vigenere(c, kt[i])
    output.write(vigenere(c, kt[i]))
    i += 1
output.write('\n')
output.write("Padding" + '\n')
output.write(poly)
# padding for 4x4 blocks
while i < 16:
    poly += "A"
    output.write("A")
    i += 1

# start shifting
blockNum = poly.__len__() / 16
i = 0       # total text indexing
j = 0       # inside block indexing
shiftedText = ""
output.write('\n')
output.write("Shifting" + '\n')
temp = blockNum
while temp > 0:
    displayCol = ""
    row1 = poly[0 + i: i + 4]
    shiftedText += row1
    displayCol += row1 + '\n'
    row2 = poly[4 + i:4 + i + 4]
    row2 = row2[1:]+row2[:1]

    shiftedText += row2
    displayCol += row2 + '\n'
    row3 = poly[8 + i:8 + i + 4]
    row3 = row3[2:]+row3[:2]

    shiftedText += row3
    displayCol += row3 + '\n'
    row4 = poly[12 + i: 12 + i + 4]
    row4 = row4[3:]+row4[:3]

    displayCol += row4 + '\n'
    shiftedText += row4
    output.write(displayCol)
    temp -= 1
    i += 16
    output.write('\n')

unformatted = ''
output.write('\n')
output.write('Parity' + '\n')

def parityOf(int_type):
    parity = 0
    while (int_type):
        parity = ~parity
        int_type = int_type & (int_type - 1)
    return(parity)



def checkParity(string_bits):
    counter = 0
    for c in string_bits:
        if c == "1":
            counter += 1
    return (counter % 2) == 0

hexstring = ""
binstring = ""
for c in shiftedText:
    unformatted = (bin(ord(c)))
    unformatted = unformatted[2:].zfill(8)
    if not checkParity(unformatted):
        #print("odd")
        unformatted = "1" + unformatted[1:]
    binstring += unformatted
    hexstring += "{0:0>2X}".format(int(unformatted, 2))

hex2bin_map = {
   "0":"0000",
   "1":"0001",
   "2":"0010",
   "3":"0011",
   "4":"0100",
   "5":"0101",
   "6":"0110",
   "7":"0111",
   "8":"1000",
   "9":"1001",
   "A":"1010",
   "B":"1011",
   "C":"1100",
   "D":"1101",
   "E":"1110",
   "F":"1111",
}

#hex block num
#takes in hex string like EE and converts it to byte type
def hexToByte(hexstring):
    binasstring = hex2bin_map[hexstring[0:1]] + hex2bin_map[hexstring[1:2]]
    #print(binasstring)
    return int(binasstring, 2)
    #return '{0:08b}'.format(int(binasstring, 2))

def rgfMul(byteNum, multBy):
    if multBy != 2 and multBy != 3:
        return
    sigGreater = False
    if byteNum >= 128:
        sigGreater = True
    
    mask = 2 ** 8 - 1
    doubled = (byteNum << 1) & mask

    #check if msb is 0
    #print(bin(doubled))
    #print(doubled)
    
    if multBy == 2 and not sigGreater:
        return doubled
    if multBy == 2:
        return doubled ^ int('00011011',2)
    if multBy == 3 and not sigGreater:
        return doubled ^ byteNum
    else:
        return (doubled ^ byteNum) ^ int('00011011',2)
#print('rgf below')
#print(rgfMul(hexToByte(hexstring[0:2]),2))
#print(rgfMul(175, 3))
#print(hexstring[0:2])
#print(hexToByte(hexstring[0:2]))


temp = blockNum
text = ""
i = 0
def fillRow(mtrix, rownum, text):
    i = 0 # for the columns of the matrix
    j = 0 # for actual text
    while i < 4:
        mtrix[rownum, i] = text[j:j+2]
        j += 2
        i += 1
mixedoutput = ''
while temp > 0:
    matrix = np.zeros(shape=(4, 4), dtype=object)

    displayCol = ""
    row1 = hexstring[0 + i: i + 8] + '\n'
    fillRow(matrix, 0, row1)#check this later to see how \n is handled
    text += row1

    displayCol += row1
    row2 = hexstring[8 + i:8 + i + 8]  + '\n'
    fillRow(matrix, 1, row2)
    #row2 = row2[1:]+row2[:1]

    text += row2
    displayCol += row2
    row3 = hexstring[16 + i:16 + i + 8] + '\n'
    fillRow(matrix, 2, row3)
    #row3 = row3[2:]+row3[:2]

    text += row3
    displayCol += row3
    row4 = hexstring[24 + i: 24 + i + 8] + '\n'
    fillRow(matrix, 3, row4)
    #row4 = row4[3:]+row4[:3]

    displayCol += row4
    text += row4
    output.write(displayCol + "\n")
    temp -= 1
    i += 32
    text += '\n'

    #now that the matrix is filled with string hex values, begin mix columns
    mixedmatrix = np.zeros(shape=(4, 4), dtype=object)
    #do col 0
    counter = 0
    while counter < 4:
        mixedmatrix[0, counter] = rgfMul(hexToByte(matrix[0, counter]), 2) ^ rgfMul(hexToByte(matrix[1, counter]), 3) ^\
                                  hexToByte(matrix[2, counter]) ^ hexToByte(matrix[3, counter])
        counter += 1
    #col1
    counter = 0
    while counter < 4:
        mixedmatrix[1, counter] = hexToByte(matrix[0,counter]) ^ rgfMul(hexToByte(matrix[1,counter]),2) ^ \
                                  rgfMul(hexToByte(matrix[2,counter]),3) ^ hexToByte(matrix[3,counter])
        counter+=1
    #col2
    counter = 0
    while counter < 4:
        mixedmatrix[2, counter] = hexToByte(matrix[0,counter]) ^ hexToByte(matrix[1,counter]) ^\
                                  rgfMul(hexToByte(matrix[2, counter]), 2) ^ rgfMul(hexToByte(matrix[3,counter]),3)
        counter += 1
    counter = 0
    while counter < 4:
        mixedmatrix[3, counter] = rgfMul(hexToByte(matrix[0, counter]), 3) ^ hexToByte(matrix[1,counter])^\
                                  hexToByte(matrix[2, counter]) ^ rgfMul(hexToByte(matrix[3, counter]), 2)
        counter += 1
    counter = 0
    np.set_printoptions(formatter={'object': hex})
    print(mixedmatrix)
    outer = 0
    inner = 0

    for outer in range(4):
        for inner in range(4):
            mixedoutput += hex(mixedmatrix[outer][inner])[2:] + ' '
            if inner == 3:
                mixedoutput += '\n'
            inner += 1
        if outer == 3:
            mixedoutput += '\n'
        outer += 1
output.write("mixed output" + '\n')
print(mixedoutput)
output.write(mixedoutput)


