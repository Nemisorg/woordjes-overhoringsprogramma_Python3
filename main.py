# Imports
import os, re, pathlib, random, time


# Variables
ACTIONS = {
    "menu_actions": ("M", "V", "T", "O", "I", "R", "S"),
    "existing_file_handling_actions": ("A", "O"),
}

MESSAGES = {
    "ask_menu_action": "Wat wilt u doen?: \n\n\
Maak een nieuwe lijst (M) \n\
Verander een bestaande lijst (V) \n\
Voeg woorden / zinnen toe aan een bestaande lijst (T) \n\
Overhoor een lijst (O) \n\
Import lijsten (I) \n\
Verwijder een lijst (R) \n\
Stop het programma (S) \n\n",

    "ask_filename": "Welke bestandsnaam moet het nieuwe bestand krijgen? ",

    "ask_corrected_filename": "'{}' is geen correcte bestandsnaam. \
Voer een andere bestandsnaam in: ",

    "ask_existing_file_handling": "Het bestand dat u wilt maken bestaat al, \n\
wilt u het overschrijven (O) of een andere bestandsnaam kiezen (A)? ",

    "ask_first_language": "Wat is de eerste taal? ",

    "ask_second_language": "Wat is de tweede taal? ",

    "ask_word_nontranslated": "Voer een woord / zin in in het {}, /S om te stoppen: ",

    "ask_word_translated": "Wat is de vertaling van '{}' in het {}: ",

    "line_to_change": "Welke lijn moet veranderd worden? ",

    "ask_wich_list_file": "Welk bestand wilt u gebruiken voor de gekozen actie? ",

    "ask_language_order": "Hoe wilt u de lijst overhoren? ",

    "wrong": "Fout, het juiste antwoord was '{}'.",

    "keep_it_up": "Ga zo door!",

    "confirm_delete": "Weet u zeker dat u '{}' wilt verwijderen? [Y/n] ",

    "file_delete_exit_0": "Het bestand is succesvol verwijderd. "
}


# System functions
def oscheck(ntcmd, othercmd):
    if os.name == 'nt':
        exec(ntcmd)
    else: 
        exec(othercmd)

def clear():
    oscheck("os.system('cls')", "os.system('clear')")

def ls(cd,cdabsolute):
    paths_ls = []
    cdloop = pathlib.Path(cd)
    
    for cf in cdloop.iterdir():
        paths_ls.append(str(cf))
    return paths_ls

def any_key():
    oscheck("pause", """bash -c 'read -s -n 1 -p "Press any key to continue . . . "'""")

def rm(list_file):
    oscheck("os.system('del /F /Q {}')".format(list_file), "os.system('rm -rf {}')".format(list_file))


# Subfunctions
def ask_menu_action():
    clear()
    menu_action = input(MESSAGES["ask_menu_action"]).title()
    while menu_action not in ACTIONS["menu_actions"]:
        clear()
        menu_action = input(MESSAGES["ask_menu_action"]).title()
    return menu_action

def execute_menu_action(menu_action):
    if menu_action == "S":
        clear()
        return menu_action
    elif menu_action == "M":
        make_list()
    elif menu_action == "V":
        change_list()
    elif menu_action == "T":
        pass
    elif menu_action == "O":
        learn_list()
    elif menu_action == "I":
        pass
    elif menu_action == "R":
        remove_list()
    elif menu_action == "C":
        pass

def ask_filename():
    clear()
    filename = input(MESSAGES["ask_filename"])
    return filename

def check_filename_characters(filename):
    filename.replace(" ", "_")
    while re.match(r"^\w.+$",filename) is None:
        clear()
        filename = input(MESSAGES["ask_corrected_filename"].format(filename[:-4]))
        filename += ".wdl"
    return filename

def ask_nonexisting_filename(filename):
    if os.path.isfile(filename):
        existing_file_handling_action = None
        while existing_file_handling_action not in ACTIONS["existing_file_handling_actions"]:
            clear()
            print(filename[:-4])
            existing_file_handling_action = input(MESSAGES["ask_existing_file_handling"]).title()
        return existing_file_handling_action, filename
    existing_file_handling_action = "O"
    return existing_file_handling_action, filename

def make_filename():
    existing_file_handling_action = "A"
    while existing_file_handling_action == "A":
        clear()
        filename = input(MESSAGES["ask_filename"])
        filename += ".wdl"
        filename = check_filename_characters(filename)
        existing_file_handling_action, filename = ask_nonexisting_filename(filename)
    return filename

def ask_languages(open_file):
    clear()
    first_language = input(MESSAGES["ask_first_language"])
    while "=" in first_language or first_language == "":
        first_language = input(MESSAGES["ask_first_language"])
    second_language = input(MESSAGES["ask_second_language"])
    while "=" in second_language or second_language == "":
        second_language = input(MESSAGES["ask_second_language"])
    open_file.write(first_language + "=" + second_language + "\n")
    return first_language, second_language

def ask_words(open_file, first_language, second_language):
    clear()
    first_word = input(MESSAGES["ask_word_nontranslated"].format(first_language))
    if first_word.title() == "/S":
        return first_word.title()
    elif "=" in first_word or first_word == "":
        return
    clear()
    second_word = input(MESSAGES["ask_word_translated"].format(first_word, second_language))
    if "=" in second_word or second_word == "":
        return
    open_file.write(first_word + "=" + second_word + "\n")

def print_list_files():
    paths_ls = ls(".", os.getcwd())
    for file_dir in paths_ls:
        if file_dir.endswith(".wdl"):
            print(file_dir[:-4])
    return paths_ls
        
def ask_wich_list_file():
    clear()
    paths_ls = print_list_files()
    list_file = input(MESSAGES["ask_wich_list_file"])
    list_file += ".wdl"
    while list_file not in paths_ls:
        clear()
        print_list_files()
        list_file = input(MESSAGES["ask_wich_list_file"])
        list_file += ".wdl"
    return list_file

def import_lines(open_file):
    all_lines = []
    for line in open_file:
        all_lines.append(line.rstrip("\n"))
    first_language, second_language = all_lines[0].split("=")
    second_language = second_language
    del all_lines[0]
    return all_lines, first_language, second_language

def ask_language_order(first_language, second_language):
    order = ""
    while order not in ("1", "2"):
        clear()
        print("1: " + first_language + " naar " + second_language)
        print("2: " + second_language + " naar " + first_language)
        order = input(MESSAGES["ask_language_order"])
    if order == "2":
        language_to_ask = first_language
        reverse_ask = True
    else:
        language_to_ask = second_language
        reverse_ask = False
    return language_to_ask, reverse_ask

def ask_meanings(all_lines, language_to_ask, reverse_ask):
    asked_meanings = []
    while len(asked_meanings) != len(all_lines):
        line = random.randint(0, len(all_lines) - 1)
        while line in asked_meanings:
            line = random.randint(0, len(all_lines) - 1)
        value, answer = all_lines[line].split("=")
        if reverse_ask == True:
            answer_temp = value
            value = answer
            answer = answer_temp
        clear()
        answer_to_check = input(MESSAGES["ask_word_translated"].format(value, language_to_ask))
        if answer_to_check == answer:
            print(MESSAGES["keep_it_up"])
            time.sleep(1)
            asked_meanings.append(line)
        else:
            print(MESSAGES["wrong"].format(answer))
            time.sleep(2.5)
    

# Main functions
def main():
    menu_action = None
    while menu_action != "S":
        menu_action = ask_menu_action()
        menu_action = execute_menu_action(menu_action)

def make_list():
    filename = make_filename()
    open_file = open(filename, "w")
    first_language, second_language = ask_languages(open_file)
    when_to_break = ask_words(open_file, first_language, second_language)
    while when_to_break != "/S":
        when_to_break = ask_words(open_file, first_language, second_language)
    open_file.close()

def change_list():
    list_file = ask_wich_list_file()
    open_file = open(list_file)
    all_lines, first_language, second_language = import_lines(open_file)
    open_file.close()
    line_number = 1
    clear()
    for line in all_lines:
        print(str(line_number) + ": " + line)
        line_number += 1
    line_to_change = int(input(MESSAGES["line_to_change"]))
    while line_to_change not in range(1, len(all_lines)):
        line_to_change = input(MESSAGES["line_to_change"])
    line_to_change -= 1
    line_number = -1
    open_file = open(list_file, "w")
    for line in all_lines:
        line_number += 1
        if line_number == line_to_change:
            ask_words(open_file, first_language, second_language)
        else:
            open_file.write(line + "\n")
    open_file.close()

def learn_list():
    list_file = ask_wich_list_file()
    open_file = open(list_file)
    all_lines, first_language, second_language = import_lines(open_file)
    language_to_ask, reverse_ask = ask_language_order(first_language, second_language)
    ask_meanings(all_lines, language_to_ask, reverse_ask)

def remove_list():
    list_file = ask_wich_list_file()
    confirm_delete = input(MESSAGES["confirm_delete"].format(list_file[:-4]))
    if confirm_delete.title() in ("", "Y"):
        rm(list_file)
        print(MESSAGES["file_delete_exit_0"])
        time.sleep(1)


# Start execute
try:
    main()
except KeyboardInterrupt:
    clear()
    print('\nExited with exit code 0')
    try:
        exit(0)
    except SystemExit:
        os._exit(0)