# zapisuje hexadecymalny string do pliku
def HexStringToPNG(filename, newFile):
    data = bytes.fromhex(newFile)
    with open(filename, 'wb') as file:
        file.write(data)
    file.close()

# tworzy nowy IDAT


def MakeNewIDAT(hexOldFile, newIdatData, posInText, realLength):

    newIdatLength = int(len(newIdatData) / 2)

    # formatowanie do hex stringa
    newIdatLengthHex = format(newIdatLength, 'x')

    # dlugosc kawalka przechowujacego dlugosc idat musi miec dlugosc rowna 8
    while len(newIdatLengthHex) % 8 != 0:
        newIdatLengthHex = '0' + newIdatLengthHex

    # zawartosc pliku przed IDAT + nowa dlugosc + naglowek IDAT + nowe dane + reszta pliku
    newFile = hexOldFile[0:(posInText - 8)] + newIdatLengthHex + hexOldFile[posInText:(
        posInText + 8)] + newIdatData + hexOldFile[(posInText + 8 + realLength):]

    return newFile
