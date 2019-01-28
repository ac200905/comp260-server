
listOfActions = []

listOfActions.append("move")
listOfActions.append("go")
listOfActions.append("die")

userInput: str = input("What do???")

if userInput == "move":
    print("Where to??")
elif userInput == "help":
    print(listOfActions)
elif userInput == "die":
    print("You died!")

