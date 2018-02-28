from flask_bcrypt import Bcrypt

def strcut(s):
    return s[0:80]

bcrypt = Bcrypt()
