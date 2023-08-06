import hashlib, binascii, os
import secrets
import string

password_result = []

class simple:
    def __init__(self, length: int, characters: str) -> None:
        self.length = length
        self.characters = characters

    def generate(self, iterations):
        password_result.clear()
        for p in range(iterations):
            password: str = ''
            for c in range(self.length):
                password += secrets.choice(self.characters)
            password_result.append(password)
        return password_result

    def result(self, num: int) -> None:
        return password_result[num]

class complex(simple):
    def __init__(self, length, string_method, numbers=True, special_chars=False):
        characters = ''

        methods: dict = {
            "upper": string.ascii_uppercase,
            "lower": string.ascii_lowercase,
            "both": string.ascii_letters,
        }

        characters += methods[string_method]

        if numbers:
            characters += string.digit
        if special_chars:
            characters += string.punctuation

        super().__init__(length=length, characters=characters)

def hash(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),salt, 100000)

    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_hash(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]

    pwdhash = hashlib.pbkdf2_hmac('sha512',provided_password.encode('utf-8'),salt.encode('ascii'),100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

# Test scenarios

if __name__ == "__main__":
    var = simple(20, 'abcdefghijklmnopqrstuvwxyz0123467589')
    print(var.generate(3))

    print(var.result(1))

    stored_password = hash(var.result(1))
    print(stored_password)

    p = input('Password: ')
    if verify_hash(stored_password, p) == True:
        print('The password is correct')
