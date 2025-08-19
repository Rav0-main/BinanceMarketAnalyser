from desktop import *
from os import system

printVersion()

run = True
while(run):
    printMenuScreen()
    choice: int = inputScreenNumberFromMenu()
    run = not compelete(choice)
    if(run):
        system("cls")

printExit()