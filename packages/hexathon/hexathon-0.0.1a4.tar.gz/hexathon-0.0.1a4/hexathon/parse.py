import re


__re_valid = '^[0-9a-fA-F]+$'
def valid(hx):
    if len(hx) == 0 or len(hx) % 2 != 0:
        raise ValueError('invalid hex')
    if not re.match(__re_valid, hx):
        raise ValueError('invalid hex')
    return hx


def even(hx):
    if len(hx) % 2 != 0:
        hx = '0' + hx
    return valid(hx)


def uniform(hx):
    return even(hx).lower()


def strip_0x(hx):
    if len(hx) < 2:
        raise ValueError('invalid hex')
    if hx[:2] == '0x':
        hx = hx[2:]
    return even(hx)


def add_0x(hx):
    if len(hx) == 0:
        raise ValueError('invalid hex')
    if hx[:2] == '0x':
        hx = hx[2:]
    return '0x' + even(hx)


def unpad(hx):
    hx = strip_0x(hx)
    i = 0
    for i in range(len(hx)):
        if hx[i] != '0':
            break
    hx = hx[i:]
    return even(hx)


def pad(hx, byte_length):
    hx = strip_0x(hx)
    hx = hx.rjust(byte_length * 2, '0')
    return hx
