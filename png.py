import rsa_algorithm
import time


def HexStringToPNG(filename, newFile):
    data = bytes.fromhex(newFile)
    with open(filename, 'wb') as file:
        file.write(data)
    file.close()


def encryptPNG(filename1, filename2, n, e, blockSize):
    handler = open(filename1, 'rb')
    hexFile = handler.read().hex()
    posInText = hexFile.find("49444154")

    if posInText != -1:
        length = hexFile[(posInText - 8):posInText]
        chunkLengthDec = int(length, 16)
        realLength = 2 * chunkLengthDec
        idatHex = hexFile[(posInText+8):(posInText + 8 + realLength)]
        newIDAT = ''
        i = 0
        print('orginal lenght')
        print(realLength)

        while i < realLength:
            # jesli dodanie wielkosci bloku wyszlo by poza zakres
            if (i+blockSize) > realLength:
                block = idatHex[i:i+(realLength-i)]
            else:
                # jesli nie wychodzi poza zakres
                block = idatHex[i:i+blockSize]

            i = i + blockSize
            encryptedBlock = encryptBlock(block, n, e, blockSize)
            newIDAT += encryptedBlock

        newIdatLength = int(len(newIDAT) / 2)
        print('encrypted lenght')
        print(2*newIdatLength)
        #formatowanie do hex stringa
        newIdatLengthHex = format(newIdatLength, 'x')

        # dlugosc kawalka przechowujacego dlugosc idat musi miec dlugosc rowna 8
        while len(newIdatLengthHex) % 8 != 0:
            newIdatLengthHex = '0' + newIdatLengthHex
        # zawartosc pliku przed IDAT + nowa dlugosc + naglowek IDAT + nowe dane + reszta pliku
        newFile = hexFile[0:(posInText-8)] + newIdatLengthHex + hexFile[posInText:(
            posInText+8)] + newIDAT + hexFile[(posInText + 8 + realLength):]

        HexStringToPNG(filename2, newFile)


def encryptBlock(block, n, e, blockSize):
    # rzutowanie na int
    blockInt = int(block, 16)
    dlugosc = len(str(blockInt))

    if dlugosc > 617:
        print('Przekroczono dlugosc klucza:', dlugosc)

    start = time.time()
    encryptedBlock = rsa_algorithm.encrypt(blockInt, n, e)
    end = time.time()
    #print('encrypt time:', str(end - start))
    #zamiana na hex string bez '0x' z przodu
    hexBlock = format(encryptedBlock, 'x')
    leng = len(hexBlock)
    # wyrownanie blokow do dlugosci 512
    while len(hexBlock) % 512 != 0:
        hexBlock = '0' + hexBlock
    return hexBlock


def decryptPNG(filename1, filename2, n, d, blockSize):
    handler = open(filename1, 'rb')
    hexFile = handler.read().hex()
    posInText = hexFile.find("49444154")

    if posInText != -1:
        length = hexFile[(posInText - 8):posInText]
        chunkLengthDec = int(length, 16)
        realLength = 2 * chunkLengthDec
        idatHex = hexFile[(posInText + 8):(posInText + 8 + realLength)]
        newIDAT = ''
        i = 0
        print('new idat length')
        print(realLength)
        # wczytywanie blokow o wielkosci 512
        while i < realLength:
            block = idatHex[i:i + 512]
            i = i + 512
            decryptedBlock = decryptBlock(block, n, d,blockSize)
            newIDAT += decryptedBlock

        newIdatLength = int(len(newIDAT) / 2)
        print('decrypted length')
        print(2*newIdatLength)
        newIdatLengthHex = format(newIdatLength, 'x')
        while len(newIdatLengthHex) % 8 != 0:
            newIdatLengthHex = '0' + newIdatLengthHex
        newFile = hexFile[0:(posInText - 8)] + newIdatLengthHex + hexFile[posInText:(
            posInText + 8)] + newIDAT + hexFile[(posInText + 8 + realLength):]

        HexStringToPNG(filename2, newFile)


def decryptBlock(block, n, d, blockSize):
    blockInt = int(block, 16)
    encryptedBlock = rsa_algorithm.decrypt(blockInt, n, d)
    hexBlock = format(encryptedBlock, 'x')
    length = len(hexBlock)
    #wyrownanie do pierwotnej dlugosci
    while len(hexBlock) % 2 != 0:
        hexBlock = '0' + hexBlock
    return hexBlock
