from flask_bcrypt import Bcrypt

import json

def strcut(s):
    return s[0:80]

# def labelshow():
#     L = []
#     label_detail = Label.query.filter().all()
#     for i in label_detail:
#         m = "<a>{}</a>".format(i.tag)
#         L.append(m)
#     print(L)
#     return " ".join(L)

bcrypt = Bcrypt()

