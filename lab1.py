import matplotlib.pyplot as plt
import re
import requests
from random import randrange
from math import log, sqrt


alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
monofr = [0.064, 0.013, 0.046, 0.013, 0.000, 0.027, 0.042, 0.005, 0.007, 0.020, 0.055, 0.044, 0.01, 0.009, 0.033, 0.027, 0.029, 0.068, 0.086, 0.025, 0.043, 0.037, 0.045, 0.027, 0.003, 0.011, 0.01, 0.011, 0.005, 0.004, 0.016, 0.008, 0.019]


def build_histogram(text):
    monofrequencies = [0] * 33
    for char in text:
        if re.match('[а-щьюяіїєґ]', char.lower()):
            x = alphabet.index(char.lower())
            monofrequencies[x] += 1
    for i in range(33):
        monofrequencies[i] = monofrequencies[i] / len([char.lower() for char in text if re.match('[а-щьюяіїєґҐ]', char.lower())])
    plt.bar([char.lower() for char in alphabet if re.match('[а-щьюяіїєґ]', char)], monofrequencies, width=1)
    plt.show()
    return monofrequencies


def vigenere_encrypt(text, key):
    ciphertext = ''
    text = [char.lower() for char in text if re.match('[а-щьюяіїєґ]', char.lower())]
    for i in range(len(text)):
        p = alphabet.index(text[i])
        k = alphabet.index(key[i % len(key)])
        c = (p + k) % 33
        ciphertext += alphabet[c]
    return ciphertext


def vigenere_decrypt(text, key):
    plaintext = ''
    text = [char.lower() for char in text if re.match('[а-щьюяіїєґ]', char.lower())]
    for i in range(len(text)):
        p = alphabet.index(text[i])
        k = alphabet.index(key[i % len(key)])
        c = (p - k) % 33
        plaintext += alphabet[c]
    return plaintext


def index_of_coincidence(text):
    counts = [0]*33
    for char in text:
        counts[alphabet.index(char)] += 1
    numer = 0
    total = 0
    for i in range(33):
        numer += counts[i]*(counts[i]-1)
        total += counts[i]
    return 33*numer / (total*(total-1))


def find_period_slices(text):
    text = [char.lower() for char in text if re.match('[а-щьюяіїєґ]', char.lower())]
    ioc_list = []
    found_period = 0
    for period in range(5, 21):
        slices = [''] * period
        for i in range(len(text)):
            slices[i % period] += text[i]
        sum = 0
        for i in range(period):
            sum += index_of_coincidence(slices[i])
        ioc = sum / period
        ioc_list.append(ioc)
        if ioc > 1.6 and found_period == 0:
            found_period = period
    plt.bar(range(5, 21), ioc_list)
    plt.show()
    return found_period, slices


# def cosangle(x, y):
#     numerator = 0
#     lengthx2 = 0
#     lengthy2 = 0
#     for i in range(len(x)):
#         numerator += x[i]*y[i]
#         lengthx2 += x[i] * x[i]
#         lengthy2 += y[i] * y[i]
#     return numerator / sqrt(lengthx2 * lengthy2)


def hack_vigenere(text, period, slices, monofrequencies):
    frequencies = []
    for i in range(period):
        frequencies.append([0] * 33)
        for j in range(len(slices[i])):
            frequencies[i][alphabet.index(slices[i][j])] += 1
        for j in range(33):
            frequencies[i][j] = frequencies[i][j] / len(slices[i])
    key = ['а'] * period
    for i in range(period):
        min_chi = 1000
        chi_list = []
        for j in range(33):
            chi = 0
            testtable = frequencies[i][j:] + frequencies[i][:j]
            for k in range(len(testtable)):
                chi += (testtable[k]-monofrequencies[k])**2/(monofrequencies[k]+0.00001)
            chi_list.append(chi)
            if chi < min_chi:
                min_chi = chi
        key[i] = alphabet[chi_list.index(min_chi)]

    # for i in range(period):
    #     for j in range(33):
    #         testtable = frequencies[i][j:] + frequencies[i][:j]
    #         if cosangle(monofrequencies, testtable) > 0.9:
    #             key[i] = alphabet[j]
    # plaintext = vigenere_decrypt(text, key)
    return key


if __name__ == '__main__':
    url = "https://raw.githubusercontent.com/leshasaloest/cryptoanalysislabs/main/plaintext"
    text = requests.get(url).text
    key = "стілець" #слова-ключі, що гарантовно працюють : шифрування весна вакцинація війна вподобайка любов жуйка тепловізор чашка
    ct = vigenere_encrypt(text, key)
    build_histogram(text)
    period, slices = find_period_slices(ct)
    print(vigenere_decrypt(ct, key))
    print(hack_vigenere(ct, period, slices, monofr))

