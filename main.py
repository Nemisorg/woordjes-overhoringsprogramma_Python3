from os import system, name

from time import sleep

def clear():  
    if name == 'nt': 
        _ = system('cls') 
 
    else: 
        _ = system('clear')

def touch(filename):
    if("." in filename):
        i = 0
        for value in filename:
            if (value == "."):
                filename_lastdot = i
            i = i + 1
        if (filename_lastdot == 0):
            filename.extend([".","w","d","l"])
        filename = "".join(filename)
    else:
        filename.extend([".","w","d","l"])
        filename = "".join(filename)
    
    if name == 'nt':
        _ = system('type nul > ' + filename) 
 
    else: 
        _ = system('touch' + filename)

def loading():
    laadstr = "Loading"
    for number in range(0,8):
        clear()
        print(laadstr)
        laadstr = laadstr + "."
        if (laadstr == "Loading...."):
            laadstr = "Loading"
        sleep(0.5)
    sleep(1)

def maak():
    clear()
    filename = list(input("Welke bestandsnaam moet de nieuwe woordenlijst krijgen?\n"))
    touch(filename)
    
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
    #loading()
    menu()

main()