from random import randint

v = 0.1

key = 846404207240646278124898970924
sbox = (
    (4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3),
    (14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9),
    (5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11),
    (7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3),
    (6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2),
    (4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14),
    (13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12),
    (1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12),
)

fro = ['00', '11', '22', '33', '44', '55', '66', '77', '88', '99', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii',
       'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz', ' 1', ' 2',
       ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9']
to_ = ['!', '@', '#', '$', '%', '^', '|', '*', '(', ')', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '~', '"', ':', ';', '_', '<', '>', '.',
       ',']

__all__ = ['mcgo', 'soc', 'zcod']


def conv(num, to_base=10, from_base=10):
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    alph = "0123456789abcdefghijklmnopqrstuvwxyz"
    if n < to_base:
        return alph[n]
    else:
        return conv(n // to_base, to_base) + alph[n % to_base]


class mcgo(object):
    """
    based on gost 28147-89
    """

    defkey = key
    defsbox = sbox
    v = 0.1

    def __init__(self, key: int = key, sbox=sbox):
        from .gost import GostCrypt
        self.c = GostCrypt(key, sbox)
        self.key = key
        self.sbox = sbox

    def encrypt(self, text):
        re = str(conv(self.c.encrypt(len(text)), 36, 10)) + '&'

        if len(text) % 2 != 0:
            text += '_'

        for i in range(0, len(text), 2):
            b = list(text[i:i + 2])
            re += conv(self.c.encrypt(int(str(ord(b[0])) + 'f' + str(ord(b[1])), 16)), 36, 10) + ' '
        return re[:-1]

    def decrypt(self, code):
        code = code.split('&')
        le = self.c.decrypt(int(conv(code[0], 10, 36)))

        re = ''
        for b in code[1].split(' '):
            b = conv(self.c.decrypt(int(conv(b, 10, 36))), 16, 10).split('f')
            re += chr(int(b[0])) + chr(int(b[1]))
        return re[0:le]

    def encode(self, text, charset='utf-8'):
        return self.encrypt(text).encode(charset)

    def decode(self, code, charset='utf-8'):
        return self.decrypt(code.decode(charset))

    def encrypt_t(self, text):
        from tqdm import tqdm
        if len(text) % 2 != 0:
            text += 'x' * (2 - len(text) % 2)

        re = f'{conv(self.c.encrypt(len(text)), 36, 10)}!'
        for i in tqdm(range(0, len(text), 2)):
            b = list(text[i:i + 2])
            re += conv(self.c.encrypt(int(f'{ord(b[0])}f{ord(b[1])}', 16)), 36, 10) + ' '
        return re[:-1]

    def decrypt_t(self, code):
        from tqdm import tqdm
        code = code.split('!')
        le = self.c.decrypt(int(conv(code[0], 10, 36)))

        re = ''
        for b in tqdm(code[1].split(' ')):
            b = conv(self.c.decrypt(int(conv(b, 10, 36))), 16, 10).split('f')
            re += chr(int(b[0])) + chr(int(b[1]))
        return re[0:(le - 1)]


class zcod(object):
    deffro = fro
    defto_ = to_
    v = 0.1

    def __init__(self, co=mcgo(), fro=fro, to_=to_, charset='utf-8'):
        assert len(to_) == len(fro)
        self.fro = fro
        self.to_ = to_
        self.co = co
        self.charset = charset

    def comp(self, text):
        for i in range(0, len(self.fro)):
            text = text.replace(self.fro[i], self.to_[i])
        return text

    def decomp(self, text):
        for i in range(len(self.to_) - 1, -1, -1):
            text = text.replace(self.to_[i], self.fro[i])
        return text

    def rencode(self, text):
        return self.comp(text).encode(self.charset)

    def rdecode(self, code):
        return self.decomp(code.decode(self.charset))

    # # zcod + mcgo

    def encrypt(self, text):
        return self.comp(self.co.encrypt(text))

    def decrypt(self, code):
        return self.co.decode(self.decomp(code))

    def encode(self, text):
        return self.rencode(self.co.encrypt(text))

    def decode(self, code):
        return self.co.decrypt(self.rdecode(code))


class soc(object):
    v = 0.1

    def __init__(self):
        pass

    def gen_sbox(self, st=False):
        from numpy.random import permutation
        from itertools import repeat
        if not st:
            return [permutation(l) for l in repeat(range(16), 8)]
        elif st == 2:
            return str([permutation(l) for l in repeat(range(16), 8)]).replace(' ', '').replace('array([', '\n    [').replace('])', ']').replace(']]', ']\n]')
        else:  # 4 json
            return str([permutation(l) for l in repeat(range(16), 8)]).replace('array([', '[').replace('])', ']').replace(' ', '')

    def gen_key(self, minl: int = 32, maxl: int = 64):
        assert 1 <= minl < maxl <= 256 and maxl >= 1
        return randint(int('1' + '0' * (minl - 1)), int('1' + '0' * (maxl - 1)))

    def gen_day_key(self):
        from time import gmtime
        abs(int(str(gmtime().tm_year)[2:]) - gmtime().tm_yday) * mcgo.defkey

    def get_local_day_key(self, up=False, dir: str = './', klen=128):
        from time import gmtime
        k = abs(int(str(gmtime().tm_year)[2:]) - gmtime().tm_yday) * mcgo.defkey

        def make():
            with open(dir + 'dk.k', 'w') as f:
                k = self.gen_key(klen - 1, klen)
                f.write(f'{gmtime().tm_year}.{gmtime().tm_yday}\n{k}')
            return k

        def read():
            with open(dir + 'dk.k', 'r') as f:
                return f.read()

        if up:
            return make()
        else:
            try:
                b = read()
                if b.split('\n')[0] != f'{gmtime().tm_year}.{gmtime().tm_yday}':
                    make()
                    return int(read().split('\n')[1])
                else:
                    return int(b.split('\n')[1])
            except:
                make()
