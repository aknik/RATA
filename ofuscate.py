# http://stackoverflow.com/questions/7488995/python-efficient-obfuscation-of-string

# For Python 3 - strings are Unicode, print is a function

def obfuscate(byt):
    # Use same function in both directions.  Input and output are bytes
    # objects.
    mask = b'keyword'
    lmask = len(mask)
    return bytes(c ^ mask[i % lmask] for i, c in enumerate(byt))

def test(s):
    data = obfuscate(s.encode())
    print(len(s), len(data), data)
    newdata = obfuscate(data).decode()
    print(newdata == s)


simple_string = 'Just plain ASCII'
unicode_string = ('sensei = \N{HIRAGANA LETTER SE}\N{HIRAGANA LETTER N}'
                  '\N{HIRAGANA LETTER SE}\N{HIRAGANA LETTER I}')

test(simple_string)
test(unicode_string)
Python 2 version:

# For Python 2

mask = 'keyword'
nmask = [ord(c) for c in mask]
lmask = len(mask)

def obfuscate(s):
    # Use same function in both directions.  Input and output are
    # Python 2 strings, ASCII only.
    return ''.join([chr(ord(c) ^ nmask[i % lmask])
                    for i, c in enumerate(s)])

def test(s):
    data = obfuscate(s.encode('utf-8'))
    print len(s), len(data), repr(data)
    newdata = obfuscate(data).decode('utf-8')
    print newdata == s


simple_string = u'Just plain ASCII'
unicode_string = (u'sensei = \N{HIRAGANA LETTER SE}\N{HIRAGANA LETTER N}'
                  '\N{HIRAGANA LETTER SE}\N{HIRAGANA LETTER I}')

test(simple_string)
test(unicode_string)

##############################################################################################################
How about the old ROT13 trick?

>>> x = 'some string'
>>> y = x.encode('rot13')
>>> y
'fbzr fgevat'
>>> y.decode('rot13')
u'some string'
For a unicode string:

>>> x = u'國碼'
>>> print x
國碼
>>> y = x.encode('unicode-escape').encode('rot13')
>>> print y
\h570o\h78op
>>> print y.decode('rot13').decode('unicode-escape')
國碼
