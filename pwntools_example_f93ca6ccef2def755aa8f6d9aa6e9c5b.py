from pwn import * # pip install pwntools
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes
import base64
import codecs


r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def btlong(a):
    hex_a = a

    a_byte = []
    n = 2
    for i in str(hex_a)[2:]:
        a_byte.append(str(hex_a)[n:n + 2])
        n = n + 2
    print(a_byte)
    ascii_byte = []
    a_byte = list(filter(None, a_byte))
    for i in range(len(a_byte)):

        ascii_byte.append(int(a_byte[i], base=16))
    word = ''

    for i in ascii_byte:
        word = word + chr(i)
    return word


def jsn_send(a):
    to_send = {
        "decoded": "changeme"
    }

    to_send["decoded"] = a

    json_send(to_send)




received = json_recv()


#print("Received type: ")
#print(received["type"])
#print("Received encoded value: ")
#print(received["encoded"])
for i in range(0,100):

    print("Received type: ")
    print(received["type"])
    print("Received encoded value: ")
    print(received["encoded"])

    if received["type"] == "base64": #DONE
        decoded = str(base64.b64decode(received["encoded"]))[2:-1]
        jsn_send(decoded)

    elif received["type"] == "hex": # DONE
        decode_hex = codecs.getdecoder("hex_codec")
        decoded = str(decode_hex(received["encoded"])[0])[2:-1]
        jsn_send(decoded)
    elif received["type"] == "rot13": #DONE
        decoded = codecs.decode(received["encoded"], "rot13")
        jsn_send(decoded)

    elif received["type"] == "bigint":
        decoded  = btlong(received["encoded"])
        jsn_send(decoded)


    else:
        #received["type"] == "utf-8": #DONE

        decoded1 = [chr(b) for b in received["encoded"]]
        decoded = "".join(decoded1)
        jsn_send(decoded)

    received = json_recv()














