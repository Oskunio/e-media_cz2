import rsa_algorithm
import shared

def encryptPNG(filename1, filename2, n, e, blockSize):

    handler = open(filename1, 'rb')
    hexFile = handler.read().hex()

    # find header
    posInText = hexFile.find("49444154")

    if posInText != -1:
        # data length (hex)
        length = hexFile[(posInText - 8):posInText]
        # data length (dec)
        chunkLengthDec = int(length, 16)
        # data length bytes -> chars
        realLength = 2 * chunkLengthDec
        # get data part from IDAT
        idatHex = hexFile[(posInText+8):(posInText + 8 + realLength)]
        newIDAT = ''

        i = 0

        while i < realLength:
            # jesli dodanie wielkosci bloku wyszlo by poza zakres
            if (i+blockSize) > realLength:
                block = idatHex[i:i+(realLength-i)]
            else:
                # jesli nie wychodzi poza zakres
                block = idatHex[i:i+blockSize]

            i = i + blockSize
            encryptedBlock = encryptBlock(block, n, e)
            newIDAT += encryptedBlock

        # sklejanie nowego pliku
        newFile = shared.MakeNewIDAT(hexFile,newIDAT,posInText,realLength)
        shared.HexStringToPNG(filename2, newFile)


def encryptBlock(block, n, e):
    # rzutowanie na int
    blockInt = int(block, 16)
    encryptedBlock = rsa_algorithm.encrypt(blockInt, n, e)
    # zamiana na hex string bez '0x' z przodu
    hexBlock = format(encryptedBlock, 'x')

    # wyrownanie blokow do dlugosci 512
    while len(hexBlock) % 512 != 0:
        hexBlock = '0' + hexBlock
    return hexBlock


def decryptPNG(filename1, filename2, n, d):
    handler = open(filename1, 'rb')
    hexFile = handler.read().hex()
    # find header
    posInText = hexFile.find("49444154")

    if posInText != -1:
        # data length (hex)
        length = hexFile[(posInText - 8):posInText]
        # data length (dec)
        chunkLengthDec = int(length, 16)
        # data length bytes -> chars
        realLength = 2 * chunkLengthDec
        # get data part from IDAT
        idatHex = hexFile[(posInText + 8):(posInText + 8 + realLength)]
        newIDAT = ''
        i = 0

        # wczytywanie blokow o wielkosci 512
        while i < realLength:
            block = idatHex[i:i + 512]
            i = i + 512
            decryptedBlock = decryptBlock(block, n, d)
            newIDAT += decryptedBlock

        # sklejanie nowego pliku
        newFile = shared.MakeNewIDAT(hexFile, newIDAT, posInText, realLength)
        shared.HexStringToPNG(filename2, newFile)


def decryptBlock(block, n, d):
    blockInt = int(block, 16)
    encryptedBlock = rsa_algorithm.decrypt(blockInt, n, d)
    # zamiana na hex string bez '0x' z przodu
    hexBlock = format(encryptedBlock, 'x')

    #wyrownanie dlugosci do parzystej liczby
    while len(hexBlock) % 2 != 0:
        hexBlock = '0' + hexBlock

    return hexBlock
