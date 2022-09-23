import pyfiglet
import zipfile
from pathlib import Path
import time
import itertools

print(pyfiglet.figlet_format("ZipForcer"))
print("------The ZIP Password BruteForcer------")
print("[1] Enter")
print("[0] Exit\n")
option=input("[?] Enter your choice: ")
print()

if option=='0':
    print("GOOD BYE!")
    quit()
elif option=='1':
    file_path = input("Enter ZIP File PATH: ")
    if not zipfile.is_zipfile(file_path):
        print("\nzip file path you entered is incorrect.")
        print("Check it and try again.")
        quit()
    
    word_list = input ("Enter Wordlist(.txt File) PATH: ")
    print()
    pth=Path(word_list)
    if not (word_list.endswith(".txt") and pth.exists()) :
        print("word list path you entered is incorrect.")
        print("Check it and try again.")
        quit()
    
    init_time= time.time()

    with open(word_list) as file:
        words=file.read()
    file.close()

    final_list=[]
    wordlist=words.split()
    for i in range(1, len(wordlist)+1):
        perms=itertools.combinations(wordlist, i)
        for j in list(perms):
            final_list.append("".join(j))
    
    final_set=set(final_list)
    i=0
    for word in final_set:
        i+=1
        try:
            with zipfile.ZipFile(file_path) as f:
                f.extractall(pwd=bytes(word, 'utf-8'))
            final_time=time.time()
            tot_time=final_time-init_time
            print("----P4SSW0RD CR4CK3D----")
            print("Password: "+word+"\n")
            print("The time taken to crack the password: "+str(tot_time))
            print("Attempt no.: "+str(i))
            print("Speed: "+str(i/tot_time)+" passwords/sec")
            quit()
        except Exception as e:
            pass
    print("Password not found :( ")

else:
    print("Invalid Response !")
