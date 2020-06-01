import time
from Crypto.Cipher import PKCS1_OAEP
import binascii

def HexStringToPNG(filename, newFile):
    data = bytes.fromhex(newFile)
    with open(filename, 'wb') as file:
        file.write(data)
    file.close()


def encryptPNG(filename1, filename2, publicKey, blockSize):

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
            if (i + blockSize) > realLength:
                block = idatHex[i:i + (realLength - i)]
            else:
                # jesli nie wychodzi poza zakres
                block = idatHex[i:i + blockSize]

            i = i + blockSize
            encryptedBlock = encryptBlock(block, publicKey, blockSize)
            newIDAT += encryptedBlock
        # powrot do dlugosci bitowej
        newIdatLength = int(len(newIDAT) / 2)
        print('encrypted lenght')
        print(2*newIdatLength)
        newIdatLengthHex = format(newIdatLength, 'x')
        while len(newIdatLengthHex) % 8 != 0:
            newIdatLengthHex = '0' + newIdatLengthHex
        newFile = hexFile[0:(posInText-8)] + newIdatLengthHex + hexFile[posInText:(
            posInText+8)] + newIDAT + hexFile[(posInText + 8 + realLength):]
        HexStringToPNG(filename2, newFile)


def encryptBlock(block, publicKey, blockSize):
    # rzutowanie stringu na bity
    msg = bytes(block, 'ascii')
    encryptor = PKCS1_OAEP.new(publicKey)

    start = time.time()
    encryptedBlock = encryptor.encrypt(msg)
    end = time.time()
    #print('encrypt time:', str(end - start))
    # rzutowanie znakow na hex
    hexBlock = binascii.hexlify(encryptedBlock)
    # rzutowanie hex bitow na hex stringi
    hexBlock = str(hexBlock, 'utf-8')
    length = len(hexBlock)
    while len(hexBlock) % 512 != 0:
        hexBlock = '0' + hexBlock
    return hexBlock


def decryptPNG(filename1, filename2, keyPair, blockSize):
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

        while i < realLength:
            block = idatHex[i:i + 512]
            i = i + 512
            decryptedBlock = decryptBlock(block,keyPair,blockSize)
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


def decryptBlock(block, keyPair, blockSize):
    decryptor = PKCS1_OAEP.new(keyPair)

    blockBytes = str.encode(block)
    blockBytes = binascii.unhexlify(blockBytes)
    hexBlock = decryptor.decrypt(blockBytes)
   # hexBlock = binascii.hexlify(hexBlock)
    hexBlock = str(hexBlock, 'utf-8')
    length = len(hexBlock)
    while len(hexBlock) % 2 != 0:
        hexBlock = '0' + hexBlock
    return hexBlock
