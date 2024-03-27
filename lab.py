from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choice

latin_low = ascii_lowercase
latin_up = ascii_uppercase
digits = digits
kirill_up = ''.join(chr(i) for i in range(ord('А'), ord('Я') + 1))
kirill_low = ''.join(chr(i) for i in range(ord('а'), ord('я') + 1))
special = punctuation

choose = {
          kirill_low: True,
          kirill_up: False,
          latin_low: False,
          latin_up: True,
          digits: True,
          special: False
          }

password = ""
length = 10
value = ''
for i, j in choose.items():
    if j:
        value += i



while len(password) != length:
    password += choice(value)
print(password)

