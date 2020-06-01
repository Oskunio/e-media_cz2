from Crypto.Cipher import PKCS1_OAEP
import binascii
import shared

def encryptPNG(filename1, filename2, publicKey, blockSize):

    handler = open(filename1, 'rb')
    hexFile = handler.read().hex()
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


        while i < realLength:
            # jesli dodanie wielkosci bloku wyszlo by poza zakres
            if (i + blockSize) > realLength:
                block = idatHex[i:i + (realLength - i)]
            else:
                # jesli nie wychodzi poza zakres
                block = idatHex[i:i + blockSize]

            i = i + blockSize
            encryptedBlock = encryptBlock(block, publicKey)
            newIDAT += encryptedBlock

        newFile = shared.MakeNewIDAT(hexFile, newIDAT, posInText, realLength)
        shared.HexStringToPNG(filename2, newFile)


def encryptBlock(block, publicKey):
    # rzutowanie stringu na bity
    msg = bytes(block, 'ascii')
    encryptor = PKCS1_OAEP.new(publicKey)

    encryptedBlock = encryptor.encrypt(msg)

    # rzutowanie znakow na hex
    hexBlock = binascii.hexlify(encryptedBlock)
    # rzutowanie hex bitow na hex stringi
    hexBlock = str(hexBlock, 'utf-8')
    # wyrownanie dlugosci do 512
    while len(hexBlock) % 512 != 0:
        hexBlock = '0' + hexBlock

    return hexBlock


def decryptPNG(filename1, filename2, keyPair):
    handler = open(filename1, 'rb')
    hexFile = handler.read().hex()
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

        # wczytywanie blokow
        while i < realLength:
            block = idatHex[i:i + 512]
            i = i + 512
            decryptedBlock = decryptBlock(block, keyPair)
            newIDAT += decryptedBlock

        # sklejanie pliku
        newFile = shared.MakeNewIDAT(hexFile, newIDAT, posInText, realLength)
        # zapisywanie pliku
        shared.HexStringToPNG(filename2, newFile)


def decryptBlock(block, keyPair):
    decryptor = PKCS1_OAEP.new(keyPair)
    blockBytes = str.encode(block)
    blockBytes = binascii.unhexlify(blockBytes)
    hexBlock = decryptor.decrypt(blockBytes)
    hexBlock = str(hexBlock, 'utf-8')

    # wyrownanie dlugosci do parzystej liczby
    while len(hexBlock) % 2 != 0:
        hexBlock = '0' + hexBlock

    return hexBlock
