import random

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456!£$%^&*(`)"

def gen_password(password_len, password_count):
        password = "" 
        for x in range(0,password_count):
            for x in range(0,password_len):
                password_char = random.choice(chars)
                password+=password_char
            password = f"\n\n{password}\n\n"
        return password
