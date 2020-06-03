import rsa_algorithm
import shared
import random
from decimal import *


class CBC():
    def __init__(self, filename1, filename2, filename3, n, e, d, keySize=1024, blockSize=256):
        self.filename1 = filename1
        self.filename2 = filename2
        self.filename3 = filename3
        self.n = n
        self.e = e
        self.d = d
        self.keySize = keySize
        self.blockSize = blockSize
        # TODO: Change it to random generated vector blockSize length
        self.initVector = 39148909606116584139217578911852226208392673723327461817764665387041932301469953656455111581286860433415168217272091210760342718513088835887519717692257045463290303961993457634410738193751786818051267367706820540072424942077293174158076608881311555234075334997743548395808580050646064651757605451868472088201
        self.prevVector = None

    def changeStringToHex(self, str):
        return int(str, base=16)

    def xorTwoHex(self, a, b):
        return a ^ b

    def encryptPNG(self):
        handler = open(self.filename1, 'rb')
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
                if (i+self.blockSize) > realLength:
                    block = idatHex[i:i+(realLength-i)]
                else:
                    # jesli nie wychodzi poza zakres
                    block = idatHex[i:i+self.blockSize]

                i = i + self.blockSize
                encryptedBlock = self.encryptBlock(block)
                newIDAT += encryptedBlock

            # reser previous Vector used in encryptBlock to None for decryption
            self.prevVector = None

            # sklejanie nowego pliku
            newFile = shared.MakeNewIDAT(
                hexFile, newIDAT, posInText, realLength)
            shared.HexStringToPNG(self.filename2, newFile)

    def encryptBlock(self, block):
        # rzutowanie na int
        blockInt = self.changeStringToHex(block)
        blockInt = self.xorTwoHex(blockInt, self.initVector) if self.prevVector == None else self.xorTwoHex(
            blockInt, self.prevVector)

        encryptedBlock = rsa_algorithm.encrypt(blockInt, self.n, self.e)
        self.prevVector = encryptedBlock
        # zamiana na hex string bez '0x' z przodu
        hexBlock = format(encryptedBlock, 'x')

        # wyrownanie blokow do dlugosci 512
        while len(hexBlock) % 512 != 0:
            hexBlock = '0' + hexBlock
        return hexBlock

    def decryptPNG(self):
        handler = open(self.filename2, 'rb')
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
                decryptedBlock = self.decryptBlock(block)
                newIDAT += decryptedBlock

            # sklejanie nowego pliku
            newFile = shared.MakeNewIDAT(
                hexFile, newIDAT, posInText, realLength)
            shared.HexStringToPNG(self.filename3, newFile)

    def decryptBlock(self, block):
        blockInt = self.changeStringToHex(block)

        decryptedBlock = rsa_algorithm.decrypt(blockInt, self.n, self.d)
        decryptedBlock = self.xorTwoHex(decryptedBlock, self.initVector) if self.prevVector == None else self.xorTwoHex(
            decryptedBlock, self.prevVector)

        self.prevVector = blockInt

        # zamiana na hex string bez '0x' z przodu
        hexBlock = format(decryptedBlock, 'x')

        # wyrownanie dlugosci do parzystej liczby
        while len(hexBlock) % 2 != 0:
            hexBlock = '0' + hexBlock

        return hexBlock
