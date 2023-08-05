from random import randint as rint
from random import choice
from codelib.base import base64decode as b_dec
from codelib.base import base64encode as b_enc
from codelib.rot import *

def dec(string, password = "foo bar moooo", rotate=50,  layer = 0, rfs=6):
    try:
        string = b_dec(rot47IterBackword(string, rfs))
    except:
        pass
    tmp = ""
    tmp_key = 0
    try:
        if(layer >=  0):
            for x in bytearray(password.encode()):
                tmp_key += x
            for i in string[18:-25]:
                tmp += chr(ord(i) - (rotate + tmp_key))
            return dec(tmp, password, rotate, layer-1, rfs)
        return b_dec(string)
    except KeyboardInterrupt:
        return "Mlikycow :: interrupt :: form keyboard"
    except:
        return "".join([chr(rint(40, 10000)) for x in range(rint(1000, 3000))])
