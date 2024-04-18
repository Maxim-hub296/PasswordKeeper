from string import ascii_lowercase, ascii_uppercase, digits, punctuation

kirill_up = ''.join(chr(i) for i in range(ord('А'), ord('Я') + 1))
kirill_low = ''.join(chr(i) for i in range(ord('а'), ord('я') + 1))

choose = {
            "kirill_low": [False, kirill_low],
            "kirill_up": [False, kirill_up],
            "latin_low": [True, ascii_lowercase],
            "latin_up": [False, ascii_uppercase],
            "digits": [True, digits],
            "special": [False, punctuation]
        }