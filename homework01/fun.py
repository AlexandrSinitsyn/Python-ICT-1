def fun(prevChar, newChar):
    if not (ord('z') >= ord(prevChar) >= ord('a') or ord('Z') >= ord(prevChar) >= ord('A')):
        return ord(prevChar)

    res = ''

    if newChar > ord('z'):
        res = ord('a') - 1 + (newChar - ord('z'))
    elif ord('z') >= newChar >= ord('a'):
        res = newChar
    elif ord('z') >= ord(prevChar) >= ord('a') > newChar > ord('Z'):
        res = ord('z') + 1 - (ord('a') - newChar)
    elif ord('a') > newChar > ord('Z') >= ord(prevChar) >= ord('A'):
        res = ord('A') - 1 + (newChar - ord('Z'))
    elif ord('Z') >= newChar >= ord('A'):
        res = newChar
    else:  # if ord('A') > symbol:
        res = ord('Z') + 1 - (ord('A') - newChar)

    return res