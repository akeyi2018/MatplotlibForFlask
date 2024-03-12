import secrets
import string
from werkzeug.security import generate_password_hash, check_password_hash

def get_random_password_string(length):
    pass_chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(pass_chars) for x in range(length))
    return password

def crt_pass(passwd):
    res = generate_password_hash(password=passwd,salt_length=8)
    print(res)
    print(len(res))
    passwd = 'testtest1'
    cres = check_password_hash(res, passwd)
    print(cres)

def get_random_user_name(length):
    pass_chars = string.digits
    password = ''.join(secrets.choice(pass_chars) for x in range(length))
    return 'USR' + password

def get_gender(gender):
    res = {'1':'男性','2':'女性'}
    return res[gender]

# print(get_random_password_string(80))

crt_pass('testtest1')

print(get_random_user_name(16))
