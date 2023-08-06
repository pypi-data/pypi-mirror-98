class ReadUserError(Exception):
    pass
class LogoffUserError(Exception):
    pass

from os import remove

def save(name,username):
    with open(name+".user","w") as fn1:
        fn1.write(username)
def read(name):
    try:
        with open(name+".user","r") as fn2:
            return fn2.read()
    except FileNotFoundError:
        raise ReadUserError(name+" user is not found!")
def logoff(name):
    try:
        remove(name+".user")
    except FileNotFoundError:
        raise LogoffUserError(name+" user is not found!")

def setmain():
    try:
        user = read("User1")
        print(user,"欢迎！")
        yesno = input("你想注销吗（Y/N）：")
        if yesno == "Y" or yesno == "y":
            logoff("User1")
    except ReadUserError:
        a = input("请输入用户名：")
        save("User1",a)


if __name__ == "__main__":
    setmain()