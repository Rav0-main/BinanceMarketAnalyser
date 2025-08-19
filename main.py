from desktop import *

printVersion()

run = True
while(run):
    printMenuScreen()
    choice: int = inputScreenNumberFromMenu()
    run = not compelete(choice)

printExit()