#A simple python script to generate password - strong or weak
import random
import sys

def generate_weak_pwd(plen):
    """A function which generates weak password to the users"""
    s = "abcdefghijklmnopqrstuvwxyz"
    pwd = "".join(random.sample(s,plen ))
    return pwd

def generate_strong_pwd(plen):
    """A function which generates strong password to the users"""
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    pwd = "".join(random.sample(s,plen ))
    return pwd

def main():
    print("Welcome from password generator! ")
    flag = input("Please Choose Weak or Strong Password to generate\nWeak-W and Strong-S: ")
    passlen = int(input("Please type the desired password length : "))

    if flag == 'W':
        res = generate_weak_pwd(passlen)
        print(res)
    elif flag == 'S':
        res = generate_strong_pwd(passlen)
        print(res)    

if __name__ == '__main__':
    main()
    sys.exit(0)