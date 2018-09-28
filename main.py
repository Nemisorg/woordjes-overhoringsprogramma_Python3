from os import system, name
import os
from time import sleep
import pathlib
import re

paths_ls = {}
cached_lists = {}

def clear():  
    if name == 'nt':  
        _ = system('cls') 
    else: 
        _ = system('clear')

def characterfix(filename):
    filename.replace(" ", "_")

    while bool(re.match("^\w.+$",filename)) == False:
        clear()
        
        filename = input("'" + filename + "' is geen correcte bestandsnaam. Voer een andere bestandsnaam in, '/cancel' om te annuleren: ")
        
        if filename == "/cancel":
            return filename
    
    return filename

def confirmoverwrite(filename):
    if os.path.isfile(filename) == True:
        overwrite = ""
        while overwrite not in ["A", "O"]:
            clear()
            
            overwrite = input("Het bestand dat u wilt maken bestaat al, \nwilt u het overschrijven (O) of een andere bestandsnaam kiezen (A)? '/cancel' om te annuleren: ")
            
            if overwrite == "/cancel":
                return overwrite
            
            overwrite = overwrite.title()

        while overwrite == "A" and os.path.isfile(filename) == True:
            clear()

            filename = input("Welke bestandsnaam moet de nieuwe woordenlijst krijgen? '/cancel' om te annuleren: ")
            
            if filename == "/cancel":
                return filename
            
            filename = characterfix(filename)
            filename = filename + ".wdl"

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
    filename = input("Welke bestandsnaam moet de nieuwe woordenlijst krijgen? '/cancel' om te annuleren: ")
    if filename == "/cancel":
        return
    
    filename = characterfix(filename)
    if filename == "/cancel":
        return
    
    filename = filename + ".wdl"
    filename = confirmoverwrite(filename)
    if filename == "/cancel":
        return

    cp(filename, filename + "cache")
    
    clear()
    
    cached_lists[filename] = {}
    print("'/save' om de lijst op te slaan en te stoppen \n'/stop' om te stoppen")
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
        cached_lists[filename][woord] = ans

    with open(filename, "w") as currentwdl:
        for woord,ans in cached_lists[filename].items():
            currentwdl.write(woord + "=" + ans)
    '''
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
        '''

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
            return

        clear()
        cancel = False
        delete = ""
        while delete not in paths_ls[os.getcwd()]:
            ls(".",os.getcwd())
            for filedirs in paths_ls[os.getcwd()]:
                if filedirs.endswith(".wdl"):
                    print(filedirs[:-4])
            delete = input("Welk bestand had u gewenst te verwijderen? '/cancel' om te annuleren: ")

            if delete == "/cancel":
                return

            delete = characterfix(delete)

            if delete == "/cancel":
                return

            delete = delete + ".wdl"
            clear()

        confirmdelete = "-"
        while confirmdelete not in ["Y","N",""]:
            confirmdelete = input("Weet u zeker dat u het bestand '" + delete[:-4] + "' wilt verwijderen? (y,N): ")
            confirmdelete = confirmdelete.title()
            clear()
        if confirmdelete == "Y":
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