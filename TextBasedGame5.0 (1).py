#Jordan Eldon Schlinger


def show_instructions():
    # This section shows the player everything they need to do and can do- breaking it down into simple chunks for them.
    print("The Legend of Melda: A Sink to the Past")
    # Exposition and backstory- not needed for a silly little thing but still. 
    print("Our brave hero, Sink, Champion of Higherrule, is currently imprisoned in Higherhigherrule Castle.")
    print("You must help him escape to bring Lanondorf down and elevate Higherrule and Higherhigherrule Castle to Highestrule.")
    print("Collect items and save the Princess—it's that simple. But Hey, Listen to the rest of the instructions!")
    print("Type these exactly to move around: 'go south', 'go north', 'go east', 'go west'")
    print("To pilfer an item and add it to your arsenal just type the following: 'get [item name]'")
    print("If you want to leave the game just type 'exit'.")

def show_status(current_room, inventory, rooms):
    # This shows the player their current position, inventory, and items in the room.
    print("\nYou are in the", current_room)
    print("Inventory:", inventory)
    if "item" in rooms[current_room]:
        print("You see a", rooms[current_room]["item"])

def main():
    # The Beginning of the main game, has our library with all rooms, their connections, and the directions! Secret room was added at the very end- literally at 9:49 PM CST- and I couldn't think of a better name for it. 
    rooms = {
        'Prison': {'east': 'Peanut Gallery', 'north': 'Secret Room'},
        'Peanut Gallery': {'north': 'Merchant Enclave', 'east': 'Annoying Companion Stables', 'west': 'Prison', 'item': 'hat'},
        'Annoying Companion Stables': {'west': 'Peanut Gallery', 'item': 'fairy'},
        'Merchant Enclave': {'south': 'Peanut Gallery', 'east': 'Labratory', 'west': 'Smithy', 'north': 'Wardrobe', 'item': 'bombs'},
        'Smithy': {'east': 'Merchant Enclave', 'item': 'sword'},
        'Labratory': {'west': 'Merchant Enclave', 'north': 'Helpful Companion Stables', 'item': 'potion'},
        'Helpful Companion Stables': {'south': 'Labratory', 'north': 'Armory', 'item': 'imp'},
        'Armory': {'south': 'Helpful Companion Stables', 'west': 'Wardrobe', 'item': 'shield'},
        'Wardrobe': {'east': 'Armory', 'south': 'Merchant Enclave', 'west': 'Exit Gate', 'item': 'tunic'},
        'Secret Room': {'south': 'Prison', 'item': 'ring'},
        'Exit Gate': {'east': 'Wardrobe'}
    }

    # Initial conditions
    current_room = 'Prison'  # Start room- after all Sink has been captured!
    inventory = []  # This will allow us to store the items collected. It will be expanded as time goes on. 
    total_items = 8  # Total number of items—only 6 are needed to win.

    show_instructions()

    while True:
        show_status(current_room, inventory, rooms)

        # Reminder on how to move even when it is at the top.
        move = input("How would you like to move? Remember you just need to type 'go [direction]': ").strip().lower()

        # A way to quit.
        if move == 'exit':
            print("I hope you enjoyed my game! It was a joy to work on and my first real experience besides modding Victoria II and the like!")
            break

        # Handles movement and checks if the move is possible. If not it gives an error.
        if move.startswith("go "):
            direction = move.split()[1].lower()
            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]
            else:
                print("Sorry, that way is blocked! Please try another direction! Though I don't recommend facing the boss until you have enough items. How many is enough? How many indeed!")

        # Handles item collection and manaement of items in rooms.
        elif move.startswith("get "):
            item = move.split()[1].lower()
            if "item" in rooms[current_room] and rooms[current_room]["item"].lower() == item:
                inventory.append(item)  # This puts the current item in the inventory of Sink/the Player.
                print(f"{item.capitalize()} has been added to your inventory. Are you almost ready for the boss?")
                del rooms[current_room]["item"]  # Removes the item from the room after collection by the player- that way we can neither have duplicates or, worse, have a player trying to collect the same item ad infinum.
            else:
                print("That item isn't here! Maybe try the item that is listed, or check if it's already in your inventory!")

        # Handles invalid inputs. Players make the darndest mistakes after all!
        else:
            print("That's not a valid command! Use 'go [direction]' or 'get [item]'.")

        # Here we have the different win and lose conditions. Each has it's own dialogue to encourage the player to do better. SSS Tier is something from Japanese games- generally A tier is not seen as enough so they added S, then SS, then SSS. SOme games even have SSSS! 
        if current_room == 'Exit Gate':
            if len(inventory) < 5:
                print("You reach the Exit Gate but lack the tools to defeat Lanondorf. He overpowers you. Neither you nor the princess will ever be heard of again- but screams can sometimes be heard as he performs dental work. Could this be you?")
                print("Thanks for playing the game. Hope you enjoyed it... loser.")
                break
            elif len(inventory) == 5:
                print("Alas brave hero, you were so close to victory. After a clash of steel, Lanondorf managed to incapacitate you! If only you gathered more items!")
                print("Thanks for playing the game. Hope you enjoyed it. You were one away from escaping!")
                break
            elif len(inventory) == 6:
                print("You managed to defeat Lanondorf. While you don't have the strength to slay him, you can now escape!")
                print("You won... but at what cost? Such a rush job leaves the princess still in danger!")
                break
            elif len(inventory) == 7:
                print("You have slain Lanondorf and saved the Kingdom from his dark dental magicks. The fair princess has been freed from her imprisonment and granted you a large estate in the countryside—YawnYawn Ranch.")
                print("Thanks for playing the game. Hope you enjoyed it. You were one away from the True End!")
                break
#By changing the indentation I made it like some games I played in the past- byt getting every single item available you automatically win- IE if you get 6 or 7 you go to the end. But by moving this elif to the left (one less indentation) it gets out of that Exit Gate. And thus it is possible to win with 8 items but not making it to the exit gate as it is easy to get lost.
        elif len(inventory) == 8:
            print("Lanondorf came running on realizing how many items you aquired but it mattered not- he was swatted aside like a fly. Not only have you slain Lanondorf and ended his dark Dentist Magicks, but after a bit of a mix-up with the ring from the secret room, you now get to rule Higherrule by your Angelic Bride. SSS Tier Victory!")
            print("Thanks for playing, you got the true end! A great job! BTW I added that last item in the last few minutes of working on this so I hope it was worth it! You are a true hero!")
            break

# Start the game
if __name__ == "__main__":
    main()