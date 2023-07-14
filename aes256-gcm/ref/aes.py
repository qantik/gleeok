""" Column-major AES-128 implementation. """

__sbox = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

__rcon = [
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39
]

from utils import *

def substitute(x):
    """ Apply S-box on a single byte. """
    return __sbox[x]

def subbytes(x):
    """ Compute the SubBytes layer on a state matrix. """
    for i in range(16):
        x[i] = substitute(x[i])

def shiftrows(x):
    """ Compute the SubBytes layer on a state matrix. """
    c0 = [ x[0],  x[5],  x[10], x[15] ]  
    c1 = [ x[4],  x[9],  x[14], x[3]  ]  
    c2 = [ x[8],  x[13], x[2],  x[7]  ]  
    c3 = [ x[12], x[1],  x[6],  x[11] ]
    x[0:4], x[4:8], x[8:12], x[12:16] = c0, c1, c2, c3

def mixcolumns(x):
    """ Compute the MixColumns layer on a state matrix. """
    xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

    for i in range(4):
        t = x[4*i+0] ^ x[4*i+1] ^ x[4*i+2] ^ x[4*i+3]
        u = x[4*i+0]
        x[4*i+0] ^= t ^ xtime(x[4*i+0] ^ x[4*i+1])
        x[4*i+1] ^= t ^ xtime(x[4*i+1] ^ x[4*i+2])
        x[4*i+2] ^= t ^ xtime(x[4*i+2] ^ x[4*i+3])
        x[4*i+3] ^= t ^ xtime(x[4*i+3] ^ u)

def addroundkey(x, rk):
    """ Compute the AddRoundKey layer on a state matrix. """
    for i in range(16):
        x[i] = x[i] ^ rk[i]

def roundfunction(x, rk, last=False):
    subbytes(x)
    shiftrows(x)
    if not last:
        mixcolumns(x)
    addroundkey(x, rk)

def keyschedule128(k):
    rkeys = [ k[:] ]
    
    for i in range(0, 10):
        t = [ 
            __sbox[rkeys[i][13]] ^ __rcon[i+1], __sbox[rkeys[i][14]],
            __sbox[rkeys[i][15]], __sbox[rkeys[i][12]]
        ]

        c0 = [
            rkeys[i][0] ^ t[0], rkeys[i][1] ^ t[1],
            rkeys[i][2] ^ t[2], rkeys[i][3] ^ t[3]
        ]  
        c1 = [
            rkeys[i][4] ^ c0[0], rkeys[i][5] ^ c0[1],
            rkeys[i][6] ^ c0[2], rkeys[i][7] ^ c0[3]
        ]  
        c2 = [
            rkeys[i][8]  ^ c1[0], rkeys[i][9]  ^ c1[1],
            rkeys[i][10] ^ c1[2], rkeys[i][11] ^ c1[3]
        ]  
        c3 = [
            rkeys[i][12] ^ c2[0], rkeys[i][13] ^ c2[1],
            rkeys[i][14] ^ c2[2], rkeys[i][15] ^ c2[3]
        ]
        rkeys.append(c0 + c1 + c2 + c3)
    return rkeys

def keyschedule256(k):
    rkeys = [ k[0:16], k[16:32] ]
    
    for i in range(0, 14):
        if i % 2 == 0:
            t = [ 
                __sbox[rkeys[i+1][13]] ^ __rcon[i//2+1], __sbox[rkeys[i+1][14]],
                __sbox[rkeys[i+1][15]], __sbox[rkeys[i+1][12]]
            ]
        else:
            t = [ 
                __sbox[rkeys[i+1][12]], __sbox[rkeys[i+1][13]],
                __sbox[rkeys[i+1][14]], __sbox[rkeys[i+1][15]]
            ]

        c0 = [
            rkeys[i][0] ^ t[0], rkeys[i][1] ^ t[1],
            rkeys[i][2] ^ t[2], rkeys[i][3] ^ t[3]
        ]  
        c1 = [
            rkeys[i][4] ^ c0[0], rkeys[i][5] ^ c0[1],
            rkeys[i][6] ^ c0[2], rkeys[i][7] ^ c0[3]
        ]  
        c2 = [
            rkeys[i][8]  ^ c1[0], rkeys[i][9]  ^ c1[1],
            rkeys[i][10] ^ c1[2], rkeys[i][11] ^ c1[3]
        ]  
        c3 = [
            rkeys[i][12] ^ c2[0], rkeys[i][13] ^ c2[1],
            rkeys[i][14] ^ c2[2], rkeys[i][15] ^ c2[3]
        ]
        rkeys.append(c0 + c1 + c2 + c3)
    return rkeys

def aes128(x, k):
    """
    >>> x = int2bytes(0x00112233445566778899AABBCCDDEEFF, 128)
    >>> k = int2bytes(0x000102030405060708090A0B0C0D0E0F, 128)
    >>> _ = aes128(x, k)
    >>> bytes2hex(x)
    '69C4E0D86A7B0430D8CDB78070B4C55A'
    """
    rkeys = keyschedule128(k)

    addroundkey(x, rkeys[0])
    for i in range(1, 11):
        roundfunction(x, rkeys[i], i==10)

def aes256(x, k):
    """
    >>> x = int2bytes(0x00112233445566778899AABBCCDDEEFF, 128)
    >>> k = int2bytes(0x000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F, 256)
    >>> _ = aes256(x, k)
    >>> bytes2hex(x)
    '8EA2B7CA516745BFEAFC49904B496089'
    """
    rkeys = keyschedule256(k)

    addroundkey(x, rkeys[0])
    #print(0, bytes2hex(rkeys[0]))
    for i in range(1, 15):
        #print(i, bytes2hex(rkeys[i]))
        roundfunction(x, rkeys[i], i==14)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
