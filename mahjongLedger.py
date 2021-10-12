# Author: Jason Lee

import configparser
def main():
    Introduction()

    # Menu
    while True:
        options = {1:addPlayer,
                    2:viewBalance,
                    3:startGame,
                    4:exit}
        try:
            choice = int(input("""
            What would you like to do?
            1. Add player(s)
            2. View Balances
            3. Start Game
            4. Exit
            """))
            options[choice]()
        except (ValueError, KeyError):
            print("Invalid input!")
            pass
def Introduction():
    print("Welcome to the Lee Family Mahjong Ledger!")
def addPlayer():
    config = configparser.ConfigParser(strict=False) # strict = false to append instead of override
    config.read("players.ini")
    name = input("Player Name? ")
    config.set("players", name, "0")
    with open("players.ini", "w") as file:
        config.write(file)
def viewBalance():
    # get data from balance to view 
    config = configparser.ConfigParser()
    config.read("players.ini")
    print("{:<15} {:<15}".format('Name', "Relative Money"))
    for key in config["players"]:
        print("{:<15} {:<15}".format(key, config["players"][key]))
    input("Press enter to go back to menu.")
def startGame():
    config = configparser.ConfigParser(strict=False)
    config.read("players.ini")
    registeredPlayers = [key for key in config["players"]]
    playing = []
    print("Who is playing?")
    for i in range(4):
        playing.append(input("Player " + str(i+1) + ": ").lower().strip())

    for player in playing:
        if player.strip() not in registeredPlayers:
            print(player, "is unregistered. Please add them.")
            return
    samePlayers = True
    while samePlayers == True:
        winner = input("Who won? If 4 of a kind money, input Money. ")
        winner.strip()
        while winner == "Money":
            winner = input("Who got Free Money? ")
            winner.strip()
            selfPicked = False
            text = input("Self Picked? (y/n)")
            if text.lower().strip() == "y":
                selfPicked = True
            if selfPicked == False:
                win = 2
            else:
                win = 4
            for player in playing:
                player = player.strip()
                config["players"][player] = str(int(config["players"][player]) - win)
            config["players"][winner] = str(int(config["players"][winner]) + 4 * win)
            with open("players.ini", "w") as file:
                config.write(file)
            winner = input("Who won? If 4 of a kind money, input Money.")
            winner.strip()
        while winner not in playing:
            print("Winner not found in current players. Try again.")
            winner = input("Who won? ")
            winner.strip()
        while True:
            try:
                doubles = int(input("How many doubles? "))
                break
            except ValueError:
                print("Invalid input. Try again.")
        picked = input("Who gave out the winning card? If self-picked, type the winner. ")
        while picked not in playing:
            print("Person must be playing in the game. Try again.")
            picked = input("Who gave out the winning card? If self-picked, type the winner. ")
        winAmount = 2 ** doubles
        bigWinAmount = 2 * winAmount
        if picked == winner:
            #update amounts from players using BWA
            for player in playing:
                player = player.strip()
                config["players"][player] = str(int(config["players"][player]) - bigWinAmount)
            config["players"][winner] = str(int(config["players"][winner]) + 4 * bigWinAmount)
            with open("players.ini", "w") as file:
                config.write(file)
        else:
            #update amounts using winA, except for picked
            for player in playing:
                player = player.strip()
                if player == picked:
                    config["players"][player] = str(int(config["players"][player]) - bigWinAmount)
                else:
                    config["players"][player] = str(int(config["players"][player]) - winAmount)
            config["players"][winner] = str(int(config["players"][winner]) + 5 * winAmount)
            with open("players.ini", "w") as file:
                config.write(file)
        text = input("Play again with the same players? (y/n)")
        if text.lower().strip() != "y":
            samePlayers = False
main()