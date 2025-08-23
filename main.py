from desktop import *
from os import system
from requests.exceptions import ConnectionError

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
        print(" * To exit - input 'e'")
        
        if(input().lower() == "e"):
            run = False

        else:
            system("cls")

    except ConnectionError:
        print("Error. You not connected to Internet!")
        print("Press <Enter> to continue")

        input()
        system("cls")

    except Exception as error:
        print("Error. Unknown error:")
        print(error)
        print("Press <Enter> to continue")
        
        input()
        system("cls")

printExit()