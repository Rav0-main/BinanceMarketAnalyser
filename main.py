from desktop import *
from os import system

printVersion()

system("title Binance Market Analyser")

run = True
while(run):
    printMenuScreen()
    try:
        choice: int = inputScreenNumberFromMenu()
    except KeyboardInterrupt:
        break
    
    try:
        run = not compelete(choice)
        if(run):
            system("cls")

    except KeyboardInterrupt:
        system("cls")
        print("Are you want return back or exit?")
        print(" * To return back - press <Enter>")
        print(" * To exit - input e")
        
        if(input().lower() == "e"):
            run = False

        else:
            system("cls")

printExit()