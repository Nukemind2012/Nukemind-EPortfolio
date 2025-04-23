from playsound import playsound
import os

# Utility function to play sounds from the audio directory
def play_sound(filename):
    path = os.path.join(os.path.dirname(__file__), 'audio', filename)
    if os.path.exists(path):
        playsound(path)
    else:
        print(f"[Sound missing: {filename}]")

#Jordan Eldon Schlinger

play_sound('ambient.mp3')

def show_instructions():
    print("The Legend of Melda: A Sink to the Past")
    print("Our brave hero, Sink, Champion of Higherrule, is currently imprisoned in Higherhigherrule Castle.")
    print("You must help him escape to bring Lanondorf down and elevate Higherrule and Higherhigherrule Castle to Highestrule.")
    print("Collect items and save the Princess—it's that simple. But Hey, Listen to the rest of the instructions!")
    print("Type these exactly to move around: 'go south', 'go north', 'go east', 'go west'")
    print("To pilfer an item and add it to your arsenal just type the following: 'get [item name]'")
    print("If you want to leave the game just type 'exit'.")

def show_map():
    play_sound('map.mp3')
    print("""
                 [Secret Room]
                      |
                   [Prison] -- [Peanut Gallery] -- [Annoying Companion Stables]
                                     |
                            [Merchant Enclave]
                             /     |       \
                 [Smithy]--       |        --[Labratory]
                                  |                |
                              [Wardrobe]        [Helpful Companion Stables]
                                  |                       |
                               [Exit Gate]           [Armory]
    """)

def show_status(current_room, inventory, rooms):
    print("\nYou are in the", current_room)
    print("Inventory:", inventory)
    if "item" in rooms[current_room]:
        print("You see a", rooms[current_room]["item"])

def calculate_player_stats(inventory, item_stats, level=0):
    stats = {"attack": 10, "defense": 5, "magic": 5}  # Starting stats
    for item in inventory:
        if item in item_stats:
            for stat in stats:
                stats[stat] += item_stats[item][stat]
    multiplier = 1 + 0.1 * level
    for stat in stats:
        stats[stat] = int(stats[stat] * multiplier)
    return stats

def fight_miniboss(player_stats, current_room, kill_count, difficulty_multiplier):
    global player_health
    miniboss_names = {
        'Prison': 'Malon',
        'Peanut Gallery': 'Falon',
        'Annoying Companion Stables': 'Moblin',
        'Merchant Enclave': 'Boblin',
        'Smithy': 'Goblin',
        'Labratory': 'Soblin',
        'Helpful Companion Stables': 'Roblin',
        'Armory': 'Tobin',
        'Wardrobe': 'Foblin',
        'Secret Room': 'Roblin'
    }
    miniboss_name = miniboss_names.get(current_room, "a mysterious foe")
    if current_room in ["Wardrobe", "Armory"]:
        miniboss = {"health": int(60 * difficulty_multiplier), "attack": int(20 * difficulty_multiplier), "defense": 0, "magic": 0}
    else:
        miniboss = {"health": int(30 * difficulty_multiplier), "attack": int(10 * difficulty_multiplier), "defense": 0, "magic": 0}
    # player_health already initialized

    print(f"{miniboss_name} blocks your path in the {current_room}!")
    while player_health > 0 and miniboss['health'] > 0:
        action = input(f"Choose your action against {miniboss_name} ('attack' or 'magic'): ").strip().lower()
        if action == 'attack':
            play_sound('attack.mp3')
            damage = max(player_stats['attack'] - miniboss['defense'], 0)
            miniboss['health'] -= damage
            print(f"You hit {miniboss_name} for {damage} damage! {miniboss_name}'s HP: {max(miniboss['health'], 0)}")
        elif action == 'magic':
            play_sound('magic.mp3')
            damage = max(player_stats['magic'] - miniboss['defense'], 0)
            miniboss['health'] -= damage
            print(f"You cast a spell on {miniboss_name} for {damage} damage! {miniboss_name}'s HP: {max(miniboss['health'], 0)}")
        else:
            print("Invalid action! Use 'attack' or 'magic'.")
            continue

        if miniboss['health'] <= 0:
            break

        damage = max(miniboss['attack'] - player_stats['defense'], 0)
        play_sound('damage.mp3')
        player_health -= damage
        print(f"{miniboss_name} attacks back for {damage} damage! Your HP: {max(player_health, 0)}")

    if player_health > 0:
        print(f"You have defeated {miniboss_name} in the {current_room}!")
        kill_count += 1
            play_sound('levelup.mp3')
        return True, kill_count
    else:
        print("You were defeated by the miniboss. Game over.")
        exit()

import sqlite3

def save_game(player_name, current_room, inventory, kill_count, player_health):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS saves (
                    player_name TEXT PRIMARY KEY,
                    current_room TEXT,
                    inventory TEXT,
                    kill_count INTEGER,
                    player_health INTEGER)''')
    inventory_str = ','.join(inventory)
    c.execute('''REPLACE INTO saves (player_name, current_room, inventory, kill_count, player_health)
                 VALUES (?, ?, ?, ?, ?)''', (player_name, current_room, inventory_str, kill_count, player_health))
    conn.commit()
    conn.close()

def load_game(player_name):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('SELECT current_room, inventory, kill_count, player_health FROM saves WHERE player_name = ?', (player_name,))
    result = c.fetchone()
    conn.close()
    if result:
        current_room, inventory_str, kill_count, player_health = result
        inventory = inventory_str.split(',') if inventory_str else []
        return current_room, inventory, kill_count, player_health
    return None

def main():
    global player_health, kill_count
    player_name = input("Enter your player name (default: Melda): ").strip() or "Melda"
    choice = input("Type 'load' to continue a saved game or press Enter to start new: ").strip().lower()

    if choice == 'load':
        loaded = load_game(player_name)
        if loaded:
            current_room, inventory, kill_count, player_health = loaded
            print(f"Loaded game for {player_name} in {current_room} with inventory: {inventory}")
        else:
            print("No saved game found. Starting a new game.")
            current_room, inventory, kill_count, player_health = 'Prison', [], 0, 100
    else:
        current_room, inventory, kill_count, player_health = 'Prison', [], 0, 100       # Tracks number of kills for leveling
    difficulty_input = input("Choose difficulty (easy, normal, hard): ").strip().lower()
    if difficulty_input == 'easy':
        difficulty_multiplier = 0.7
    elif difficulty_input == 'hard':
        difficulty_multiplier = 1.5
    else:
        difficulty_multiplier = 1.0
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

    item_stats = {
        "hat": {"attack": 2, "defense": 1, "magic": 3},
        "fairy": {"attack": 0, "defense": 2, "magic": 5},
        "bombs": {"attack": 10, "defense": 0, "magic": 2},
        "sword": {"attack": 15, "defense": 0, "magic": 0},
        "potion": {"attack": 0, "defense": 0, "magic": 10},
        "imp": {"attack": 3, "defense": 1, "magic": 7},
        "shield": {"attack": 0, "defense": 12, "magic": 0},
        "tunic": {"attack": 0, "defense": 5, "magic": 1},
        "ring": {"attack": 5, "defense": 5, "magic": 10}
    }

    lanondorf = {
        "name": "Lanondorf",
        "health": 100,
        "attack": 25,
        "defense": 15,
        "magic": 20
    }

    current_room = 'Prison'
    inventory = []
    visited_rooms = set()
    show_instructions()

    while True:
        show_status(current_room, inventory, rooms)

        level = kill_count if kill_count < 4 else 4 + (kill_count - 4) // 2
        player_stats = calculate_player_stats(inventory, item_stats, level)

        if current_room not in visited_rooms:
            if current_room != 'Exit Gate':
                miniboss_result, new_kill_count = fight_miniboss(player_stats, current_room, kill_count, difficulty_multiplier)
                if new_kill_count > kill_count:
                    kill_count = new_kill_count
                    player_health = 100  # Reset HP on level up
            visited_rooms.add(current_room)

        move = input("How would you like to move? You can also type 'save' to save your game, or 'map': ").strip().lower()

        if move == 'map':
            show_map()
            continue

        if move == 'save':
            save_game(player_name, current_room, inventory, kill_count, player_health)
            print("Game saved!")
            continue

        if move == 'exit':
            print("I hope you enjoyed my game! It was a joy to work on and my first real experience besides modding Victoria II and the like!")
            break

        if move.startswith("go "):
            direction = move.split()[1].lower()
            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]
            else:
                print("Sorry, that way is blocked! Please try another direction! Though I don't recommend facing the boss until you have enough items. How many is enough? How many indeed!")

        elif move.startswith("get "):
            item = move.split()[1].lower()
            if "item" in rooms[current_room] and rooms[current_room]["item"].lower() == item:
                inventory.append(item)
                print(f"{item.capitalize()} has been added to your inventory. Are you almost ready for the boss?")
                del rooms[current_room]["item"]
            else:
                print("That item isn't here! Maybe try the item that is listed, or check if it's already in your inventory!")

        else:
            print("That's not a valid command! Use 'go [direction]' or 'get [item]'.")

        if current_room == 'Exit Gate':
            player_stats = calculate_player_stats(inventory, item_stats)
            player_health = 100
            boss_health = lanondorf['health']

            print(f"\nFinal Battle! You face {lanondorf['name']}")
            print(f"Your Stats - Attack: {player_stats['attack']}, Defense: {player_stats['defense']}, Magic: {player_stats['magic']}, HP: {player_health}")
            print(f"{lanondorf['name']}'s Stats - Attack: {lanondorf['attack']}, Defense: {lanondorf['defense']}, Magic: {lanondorf['magic']}, HP: {boss_health}")

            while player_health > 0 and boss_health > 0:
                action = input("Choose your action ('attack' or 'magic'): ").strip().lower()
                if action == 'attack':
            play_sound('attack.mp3')
                    damage = max(player_stats['attack'] - lanondorf['defense'], 0)
                    boss_health -= damage
                    print(f"You strike Lanondorf for {damage} damage! Lanondorf HP: {max(boss_health, 0)}")
                elif action == 'magic':
            play_sound('magic.mp3')
                    damage = max(player_stats['magic'] - int(lanondorf['defense'] / 2), 0)
                    boss_health -= damage
                    print(f"You cast a magic spell for {damage} damage! Lanondorf HP: {max(boss_health, 0)}")
                else:
                    print("Invalid action! Use 'attack' or 'magic'.")
                    continue

                if boss_health <= 0:
                    break

                boss_damage = max(lanondorf['attack'] - player_stats['defense'], 0)
                play_sound('damage.mp3')
        player_health -= boss_damage
                print(f"Lanondorf strikes back for {boss_damage} damage! Your HP: {max(player_health, 0)}")

            if player_health > 0:
                if difficulty_input == 'hard':
                    kill_count += 2  # Bonus XP on hard mode
                else:
                    kill_count += 1
            play_sound('levelup.mp3')

                if len(inventory) == 8:
                    if difficulty_input == 'hard':
                        print("Thanks for playing, not only did you win with an SSS Tier Victory you did it on the hardest difficulty! You are the Hero of SSSSTime!")
                    else:
                        print("You obliterate Lanondorf with overwhelming power and win the TRUE END. SSS Tier Victory!")
                else:
                    print("You defeat Lanondorf! The land is free again. Well done, hero!")
            else:
                print("You fought bravely but were not strong enough. Lanondorf wins this time.")

            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()