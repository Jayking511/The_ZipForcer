import pyfiglet
import zipfile
from pathlib import Path
import time
from itertools import permutations
import threading
import sys
import queue

print(pyfiglet.figlet_format("ZipForcer"))
print("------The ZIP Password BruteForcer------")
print("[1] Enter")
print("[0] Exit\n")
choice=input("[?] Enter your choice: ")
print()

def checkzipfilepath(file_path):
    if not zipfile.is_zipfile(file_path):
        print("\nzip file path you entered is incorrect.")
        print("Check it and try again.")
        sys.exit()
    else:
        pass

def checkwordlist(word_list):
    pth=Path(word_list)
    if not (word_list.endswith(".txt") and pth.exists()) :
        print("word list path you entered is incorrect.")
        print("Check it and try again.")
        sys.exit()
    else:
        pass

def permutation(word_list):
    wordlist=[]
    with open(word_list) as file:
        data=file.read()
    for i in data.split():
        wordlist.append(i)
    finallist=wordlist[:]
    
    perm=permutations(wordlist, 2)
    for i in perm:
        finallist.append("@".join(i))
    finalset=set(finallist)
    return finalset

def password(file_path, word, i, init_time, myqueue):
    try:
        with zipfile.ZipFile(file_path) as f:
            f.extractall(pwd=bytes(word, 'utf-8'))
        final_time=time.time()
        tot_time=final_time-init_time
        print(f"----P4SSW0RD CR4CK3D----\nPassword: {word}\n\nThe time taken to crack the password: {tot_time}\nAttempt no.: {i}\nSpeed: {i/tot_time}passwords/sec\n")
        myqueue.put("Exit")
    except Exception as e:
        pass


if choice=='0':
    print("GOOD BYE!")
    sys.exit()
elif choice=='1':
    file_path = input("Enter ZIP File PATH: ")
    checkzipfilepath(file_path)
    
    word_list = input ("Enter Wordlist(.txt File) PATH: ")
    print()
    checkwordlist(word_list)
    
    init_time= time.time()
    finalset=permutation(word_list)

    myqueue=queue.Queue()
    threads=[]
    cnt=0
    for word in finalset:
        cnt+=1
        t=threading.Thread(target=password, args=[file_path, word, cnt, init_time, myqueue])
        try:
            if myqueue.get_nowait()=="Exit":
                sys.exit()
        except queue.Empty:
            pass
        t.daemon=True
        t.start()
        threads.append(t)
    for i in threads:
        i.join()
    print("Password not found :( ")
else:
    print("Invalid Response !")
