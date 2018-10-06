#import libraries...
from os import system, name, getcwd, stat
import os, fnmatch
from time import sleep
from pathlib import Path
from re import match
from shutil import copy2


#variabelen declareren...
paths_ls = {}
home = os.path.expanduser("~")


#systeemfuncties...
def clear():  
    if name == 'nt':  
        _ = system('cls') 
    else: 
        _ = system('clear')

def ls(cd,cdabsolute):
    paths_ls[cdabsolute] = []
    cdloop = Path(cd)
    
    for cf in cdloop.iterdir():
        paths_ls[cdabsolute].append(str(cf))

def rm(filedirname):
    if name == 'nt':
        _ = system('del /F /Q ' + filedirname)
    else: 
        _ = system('rm -rf ' + filedirname)


#subfuncties voor specifieke taken van het programma...
def characterfix(filename):
    filename.replace(" ", "_")

    while bool(match("^\w.+$",filename)) == False:
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
            
            print(filename)
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

def find(pattern, path):
    result = {}
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern) and root != getcwd():
                result[os.path.join(root, name)] = name
    return result

def is_number(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


#hoofdfuncties...
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
    
    clear()
    
    print("'/save' om de lijst op te slaan en te stoppen \n'/stop' om te stoppen")
    writetofile = {}
    while True:
        woord = ""
        while woord == "" or "=" in woord:
            woord = input("Voer een woord in: ")
        if woord == "/save":
            delete = False
            break
        elif woord == "/stop":
            delete = True
            break

        ans = ""
        while ans == "" or "=" in ans:
            ans = input("Voer de betekenis / vertaling van " + woord + " in: ")
        if ans == "/save":
            delete = False
            break
        elif ans == "/stop":
            delete = True
            break
        writetofile[woord] = ans

    if delete == False:
        with open(filename, "w") as currentwdl:
            for woord,ans in writetofile.items():
                currentwdl.write(woord + "=" + ans + "\n")
        
        if stat(filename).st_size == 0:
            rm(filename)

def verander():
    while True:
        ls(".",getcwd())
        cancel = 0
        for filedirs in paths_ls[getcwd()]:
            if filedirs.endswith(".wdl"):
                cancel = cancel + 1
    
        if cancel == 0:
            clear()
            
            print("Geen bestanden om te veranderen...")
            sleep(1)
            
            return

        clear()
        
        cancel = False
        verander = ""
        while verander not in paths_ls[getcwd()]:
            ls(".",getcwd())
            for filedirs in paths_ls[getcwd()]:
                if filedirs.endswith(".wdl"):
                    print(filedirs[:-4])
            
            verander = input("Welk bestand had u gewenst te veranderen? '/cancel' om te annuleren: ")
            if verander == "/cancel":
                return

            verander = characterfix(verander)
            if verander == "/cancel":
                return
            verander = verander + ".wdl"
            
            clear()

        while True:
            clear()

            linenumber = 0
            currentline = ""
            all_lines = {}
            currentwdl = open(verander)
            for currentline in currentwdl:
                linenumber = linenumber + 1

                print(str(linenumber) + " " + currentline , end = '')
                all_lines[linenumber] = currentline
            
            changeline = input("\n\nWelke lijn moet veranderd worden? '/cancel' om te stoppen:... ")
            if changeline == "/cancel":
                currentwdl.close()

                break
            
            nummercorrect = is_number(changeline)
            if nummercorrect == True:
                changeline = int(changeline)
                if changeline > 0 and changeline <= linenumber:
                    print("'/stop' om de bewerking te negeren")
                    
                    woord = ""
                    while woord == "" or "=" in woord:
                        woord = input("Voer een woord in: ")

                    if woord != "/stop":
                        ans = ""
                        while ans == "" or "=" in ans:
                            ans = input("Voer de betekenis / vertaling van " + woord + " in: ")
                        ans = ans + "\n"

                    

                    if woord != "/stop" and ans != "/stop":
                        all_lines[changeline] = woord + "=" + ans
                        currentwdl.close()
                        
                        currentwdl = open(verander, "w")
                        for line, value in all_lines.items():
                            currentwdl.write(value)

            currentwdl.close()

def add():
    while True:
        ls(".",getcwd())
        cancel = 0
        for filedirs in paths_ls[getcwd()]:
            if filedirs.endswith(".wdl"):
                cancel = cancel + 1
    
        if cancel == 0:
            clear()
            
            print("Geen bestanden om te aan toe te voegen...")
            sleep(1)
            
            return

        clear()
        
        cancel = False
        toevoegen = ""
        while toevoegen not in paths_ls[getcwd()]:
            ls(".",getcwd())
            for filedirs in paths_ls[getcwd()]:
                if filedirs.endswith(".wdl"):
                    print(filedirs[:-4])
            
            toevoegen = input("Welk bestand had u gewenst aan toe te voegen? '/cancel' om te annuleren: ")
            if toevoegen == "/cancel":
                return

            toevoegen = characterfix(toevoegen)
            if toevoegen == "/cancel":
                return
            toevoegen = toevoegen + ".wdl"
            
            clear()

        copy2(toevoegen,toevoegen + "cache")

        while True:
            clear()

            linenumber = 0
            currentline = ""
            all_lines = {}
            currentwdl = open(toevoegen)
            for currentline in currentwdl:
                linenumber = linenumber + 1

                print(str(linenumber) + " " + currentline , end = '')
                all_lines[linenumber] = currentline
            currentwdl.close()

            print("\n\n'/save' om de lijst op te slaan en te stoppen \n'/stop' om te stoppen")
            woord = ""
            while woord == "" or "=" in woord:
                woord = input("Voer een woord in: ")
            if woord == "/save":
                rm(toevoegen + "cache")
                break
            elif woord == "/stop":
                rm(toevoegen)
                copy2(toevoegen + "cache", toevoegen)
                rm(toevoegen + "cache")
                break

            ans = ""
            while ans == "" or "=" in ans:
                ans = input("Voer de betekenis / vertaling van " + woord + " in: ")
            if ans == "/save":
                rm(toevoegen + "cache")
                break
            elif ans == "/stop":
                rm(toevoegen)
                copy2(toevoegen + "cache", toevoegen)
                rm(toevoegen + "cache")
                break
            ans = ans + "\n"
            
            all_lines["laatste"] = woord + "=" + ans
                
            currentwdl = open(toevoegen, "w")
            for line, value in all_lines.items():
                currentwdl.write(value)
            currentwdl.close()

def importwdl():
    filesforimport = find('*.wdl', home)
    if len(filesforimport) == 0:
        print("Er zijn geen bestanden gevonden om te importeren...")
        sleep(1)
        return
    for fullpath, filename in filesforimport.items():
        print(filename)
    confirmimport = "-"
    while confirmimport not in ["Y", "N", ""]:
        confirmimport = input("Weet u zeker dat u " + str(len(filesforimport)) + " bestanden wilt importeren? (Y, n)... ")
        confirmimport = confirmimport.title()
    if confirmimport == "Y" or confirmimport == "":
        for fullpath, filename in filesforimport.items():
            filename = confirmoverwrite(filename)
            if filename == "/cancel":
                break
            copy2(fullpath, filename)
            rm(fullpath)

def verwijder():
    cancel = 0
    while True:
        ls(".",getcwd())
        for filedirs in paths_ls[getcwd()]:
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
        while delete not in paths_ls[getcwd()]:
            ls(".",getcwd())
            for filedirs in paths_ls[getcwd()]:
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


#main...
def menu():
    actie = ""
    
    while actie != "S":
        clear()

        actie = input("Wat wilt u doen?:\nMaak een nieuwe woordenlijst (M)\nVerander een bestaande woordenlijst (V)\nVoeg woorden toe aan een bestaande woordenlijst (A)\nOverhoor een woordenlijst (O)\nImport woordenlijsten (I)\nVerwijder een woordenlijst (R)\nStop het programma (S)\n\n")
        actie = actie.title()
        
        clear()
        
        if actie == "M":
            maak()
        elif actie == "V":
            verander()
        elif actie == "A":
            add()
        #elif actie == "O":
        #    overhoor()
        elif actie == "I":
            importwdl()
        elif actie == "R":
            verwijder()


#start...
menu()