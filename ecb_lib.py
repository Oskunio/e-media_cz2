import binascii
import shared
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


class ECB_LIB():
    def __init__(self, oryginalFile, encryptedFile, decryptedFile, n, e, d, blockSize=None):
        self.oryginalFile = oryginalFile
        self.encryptedFile = encryptedFile
        self.decryptedFile = decryptedFile
        self.generateKey(n, e, d)
        (self.keyPair, self.publicKey) = self.generateKey(n, e, d)
        if blockSize is None:
            blockSize = 64
        self.blockSize = blockSize

    def generateKey(self, n, e, d):
        keyPair = RSA.construct((n, e, d))
        publicKey = keyPair.publickey()
        return keyPair, publicKey

    def encryptPNG(self):
        handler = open(self.oryginalFile, 'rb')
        hexFile = handler.read().hex()
        posInText = shared.findPngHeader(hexFile)

        if posInText != -1:
            realLength = shared.getDataRealLength(hexFile, posInText)
            # get data part from IDAT
            idatHex = hexFile[(posInText + 8):(posInText + 8 + realLength)]
            newIDAT = ''
            i = 0

            while i < realLength:
                # jesli dodanie wielkosci bloku wyszlo by poza zakres
                if (i + self.blockSize) > realLength:
                    block = idatHex[i:i + (realLength - i)]
                else:
                    # jesli nie wychodzi poza zakres
                    block = idatHex[i:i + self.blockSize]

                i += self.blockSize
                encryptedBlock = self.encryptBlock(block)
                newIDAT += encryptedBlock

            newFile = shared.MakeNewIDAT(
                hexFile, newIDAT, posInText, realLength)
            shared.HexStringToPNG(self.encryptedFile, newFile)

    def encryptBlock(self, block):
        # rzutowanie stringu na bity
        msg = bytes(block, 'ascii')
        encryptor = PKCS1_OAEP.new(self.publicKey)

        encryptedBlock = encryptor.encrypt(msg)

        # rzutowanie znakow na hex
        hexBlock = binascii.hexlify(encryptedBlock)
        # rzutowanie hex bitow na hex stringi
        hexBlock = str(hexBlock, 'utf-8')
        # wyrownanie dlugosci do 512
        while len(hexBlock) % 512 != 0:
            hexBlock = '0' + hexBlock

        return hexBlock

    def decryptPNG(self):
        handler = open(self.encryptedFile, 'rb')
        hexFile = handler.read().hex()
        posInText = shared.findPngHeader(hexFile)

        if posInText != -1:
            realLength = shared.getDataRealLength(hexFile, posInText)
            # get data part from IDAT
            idatHex = hexFile[(posInText + 8):(posInText + 8 + realLength)]
            newIDAT = ''
            i = 0

            # wczytywanie blokow
            while i < realLength:
                block = idatHex[i:i + 512]
                i += 512
                decryptedBlock = self.decryptBlock(block)
                newIDAT += decryptedBlock

            # sklejanie pliku
            newFile = shared.MakeNewIDAT(
                hexFile, newIDAT, posInText, realLength)
            # zapisywanie pliku
            shared.HexStringToPNG(self.decryptedFile, newFile)

    def decryptBlock(self, block):
        decryptor = PKCS1_OAEP.new(self.keyPair)
        blockBytes = str.encode(block)
        blockBytes = binascii.unhexlify(blockBytes)
        hexBlock = decryptor.decrypt(blockBytes)
        hexBlock = str(hexBlock, 'utf-8')

        # wyrownanie dlugosci do parzystej liczby
        while len(hexBlock) % 2 != 0:
            hexBlock = '0' + hexBlock

        return hexBlock
