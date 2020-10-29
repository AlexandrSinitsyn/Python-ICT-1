import fun


def encrypt_caesar(plaintext, shift=3):
    ciphertext = ""

    for i in plaintext:
        symbol = ord(i) + shift

        symbol = fun.fun(i, symbol)

        ciphertext += chr(symbol)

    return ciphertext


def decrypt_caesar(plaintext, shift=3):
    ciphertext = ""

    for i in plaintext:
        symbol = ord(i) - shift

        symbol = fun.fun(i, symbol)

        ciphertext += chr(symbol)

    return ciphertext
