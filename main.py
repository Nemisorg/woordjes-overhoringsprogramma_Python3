from os import system, name

import os

from time import sleep

import pathlib

def clear():  
    if name == 'nt': 
        _ = system('cls') 
 
    else: 
        _ = system('clear')

def touch(filename):
    filename.extend([".","w","d","l"])
    i = 0
    for value in filename:
        if value == " ":
            filename[i] = "_"
        i = i + 1
    filename = "".join(filename)
    
    if name == 'nt':
        _ = system('type nul > ' + filename) 
 
    else: 
        _ = system('touch ' + filename)

def ls(cd,cdabsolute):
    cdloop = pathlib.Path(cd)
    if 'paths_ls' not in globals():
        global paths_ls
        paths_ls = {cdabsolute: []}
    else:
        paths_ls[cdabsolute] = []

    for cf in cdloop.iterdir():
        paths_ls[cdabsolute].append(str(cf))

def rm(filedirname):
    if name == 'nt':
        _ = system('del /F /Q ' + filedirname)
        print("del " + filedirname)
 
    else: 
        _ = system('rm -rf ' + filedirname)
        print("del " + filedirname)

def loading():
    laadstr = "Loading"
    for number in range(0,8):
        clear()
        print(laadstr)
        laadstr = laadstr + "."
        if laadstr == "Loading....":
            laadstr = "Loading"
        sleep(0.25)
    sleep(0.5)

def maak():
    clear()
    filename = list(input("Welke bestandsnaam moet de nieuwe woordenlijst krijgen?: "))
    touch(filename)
    print("'/save' om de lijst op te slaan en te stoppen \n'/stop' om te stoppen")
    filename = "".join(filename)
    with open(filename, "w") as currentwdl:
        while True:
            woord = input("Voer een woord in: ")
            if woord == "/save":
                delete = False
                break
            elif woord == "/stop":
                delete = True
                break
            currentwdl.write(woord + "\n")
            ans = input("Voer de betekenis / vertaling van " + woord + " in: ")
            if ans == "/save":
                delete = False
                break
            elif ans == "/stop":
                delete = True
                break
            currentwdl.write(ans + "\n")
    if delete == True:
        rm(filename)
    menu()
    
def verander():
    clear()
    print("Verander")

def add():
    clear()
    print("Add")

def overhoor():
    clear()
    print("Overhoor")

def menu():
    clear()
    actie = input("Wat wilt u doen?:\nMaak een nieuwe woordenlijst (M)\nVerander een bestaande woordenlijst (V)\nVoeg woorden toe aan een bestaande woordenlijst (A)\nOverhoor een woordenlijst (O)\nStop het programma (S)\n\n")
    actie = actie.title()
    if actie == "M":
        maak()
    elif actie == "V":
        verander()
    elif actie == "A":
        add()
    elif actie == "O":
        overhoor()
    elif actie == "S":
        exit()
    else:
        clear()
        menu()

    

def main():
    loading()
    menu()

main()