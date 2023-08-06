from os import remove
from glob import *

def all_user(dirs=".\\"):
    if dirs[-1] == "/" or dirs[-1] == "\\":
        all = glob(dirs+"*.user")
    else:
        all = glob(dirs+"\\"+"*/user")
    return all
def delete_all(dirs=".\\"):
    lis = all_user(dirs)
    for i in lis:
        remove(i)
if __name__ == "__main__":
    a = all_user()
    for i in a:
        print(i)
    yesno = input("是否删除所有用户？(Y/N)")
    if yesno == "Y" or yesno == "y":
        delete_all()