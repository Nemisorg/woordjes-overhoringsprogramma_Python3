from os import system, name
import os
from time import sleep
import pathlib

paths_ls = {}
wdl_list = [".","w","d","l"]

def clear():  
    if name == 'nt':  
        _ = system('cls') 
    else: 
        _ = system('clear')

def characterfix(filename):
    i = 0
    for value in filename:
        if value == " ":
            filename[i] = "_"
        elif value == "<" or value == ">" or value == ":" or value == '"' or value == "/" or value == "\\" or value == "|" or value == "?" or value == "*":
            filename[i] = ""
        i += 1
    filename = "".join(filename)

    return filename

def confirmoverwrite(filename):
    if os.path.isfile(filename) == True:
        overwrite = 0
        while overwrite not in ["A", "O"]:
                overwrite = input("Het bestand dat u wilt maken bestaat al, \nwilt u het overschrijven (O) of een andere bestandsnaam kiezen (A)?: ")
                overwrite = overwrite.title()
        while overwrite == "A" and os.path.isfile(filename) == True:
            filename = list(input("Welke bestandsnaam moet de nieuwe woordenlijst krijgen?: "))
            filename.extend([".","w","d","l"])
            filename = "".join(filename)

    return filename

def ls(cd,cdabsolute):
    cdloop = pathlib.Path(cd)
    paths_ls[cdabsolute] = []

    for cf in cdloop.iterdir():
        paths_ls[cdabsolute].append(str(cf))

def rm(filedirname):
    if name == 'nt':
        _ = system('del /F /Q ' + filedirname)
    else: 
        _ = system('rm -rf ' + filedirname)

def cp(oldpath,newpath):
    if name == 'nt':
        _ = system('copy /Y ' + oldpath + " " + newpath)
    else: 
        _ = system('cp -r ' + oldpath + " " + newpath)

def maak():
    filename = list(input("Welke bestandsnaam moet de nieuwe woordenlijst krijgen? '/cancel' om te annuleren: "))
    while len(filename) == 0:
        clear()
        filename = list(input("Welke bestandsnaam moet de nieuwe woordenlijst krijgen? '/cancel' om te annuleren: "))
    filename.extend([".","w","d","l"])

    if "".join(filename) == "/cancel.wdl":
        return 0
    
    filename = characterfix(filename)
    filename = confirmoverwrite(filename)

    cp(filename, filename + "cache")
    clear()
    
    print("'/save' om de lijst op te slaan en te stoppen \n'/stop' om te stoppen")
    # open file
    # woord = input("Voer een woord in: ")
    # while woord != "stop"
    #   doe je ding
    #   woord = input("Voer een woord in: ")
    with open(filename, "w") as currentwdl:
        while True:
            woord = input("Voer een woord in: ")
            if woord == "/save":
                delete = False
                break
            elif woord == "/stop":
                delete = True
                break

            ans = input("Voer de betekenis / vertaling van " + woord + " in: ")
            if ans == "/save":
                delete = False
                break
            elif ans == "/stop":
                delete = True
                break
            currentwdl.write(woord + "=" + ans + "\n")

    if delete == True:
        rm(filename)
        cp(filename + "cache", filename)
        rm(filename + "cache")
    else:
        rm(filename + "cache")
        if os.stat(filename).st_size == 0:
            rm(filename)

def verwijder():
    cancel = 0
    while cancel != True:
        ls(".",os.getcwd())
        for filedirs in paths_ls[os.getcwd()]:
            if filedirs.endswith(".wdl"):
                cancel = cancel + 1
    
        if cancel == 0:
            clear()
            print("Geen bestanden om te verwijderen...")
            sleep(1)
            return 0

        cancel = False
        delete = ""
        while delete not in paths_ls[os.getcwd()]:
            ls(".",os.getcwd())
            for filedirs in paths_ls[os.getcwd()]:
                if filedirs.endswith(".wdl"):
                    print(filedirs[:-4])
            delete = input("Welk bestand had u gewenst te verwijderen? '/cancel' om te annuleren: ")
            delete = delete + ".wdl"
            clear()
            if delete == "/cancel.wdl":
                return 0

        rm(delete)
        print("Bestand succesvol verwijderd...")
        sleep(1)


def menu():
    actie = ""
    while actie != "S":
        clear()
        actie = input("Wat wilt u doen?:\nMaak een nieuwe woordenlijst (M)\nVerander een bestaande woordenlijst (V)\nVoeg woorden toe aan een bestaande woordenlijst (A)\nOverhoor een woordenlijst (O)\nVerwijder een woordenlijst (R)\nStop het programma (S)\n\n")
        actie = actie.title()
        clear()
        # while actie != "S":
        #   doe iets
        #   actie = input("")
        if actie == "M":
            maak()
        #elif actie == "V":
        #    verander()
        #elif actie == "A":
        #    voeg_toe()
        #elif actie == "O":
        #    overhoor()
        elif actie == "R":
            verwijder()

menu()