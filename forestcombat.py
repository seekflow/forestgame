from random import randint, random
from textwrap import dedent

def gamemode(mode):
    """Sets the gamemode based on the user input dosage"""

    # default player attributes
    player_attributes = {
        'health': 10,
        'XP': 1,
        'elixir': ['apple', 'meat tart']
    }

    # default monster attributes
    monster_attributes = {
        'health': 10,
        'attack_power': 4
    }

    if mode == 'hard':
        # assigns player XP, player health, player elixir
        # also assigns monster attack power and health
        player_attributes['health'] = 10
        monster_attributes['health'] = 10
        monster_attributes['attack_power'] = 5
    elif mode == 'medium':
        pass
    elif mode == 'easy':
        player_attributes['health'] = 10
        monster_attributes['health'] = 7
        monster_attributes['attack_power'] = 3
    elif mode == 'none':
        pass

    return player_attributes, monster_attributes


class Player(object):

    def __init__(self, playerName, playerHealth, playerXP, playerElixir):
        self.name = playerName
        self.health = playerHealth
        self.XP = playerXP
        self.elixir = playerElixir


    def player_status(self):
        """Prints the player's attributes"""
        print(f"""

        ------------------------------------------
        |            ~ PLAYER STATUS ~           |
        | ----------------------------------------
        | -> Name           | {self.name}
        | -> Health         | {self.health}
        | -> XP             | {self.XP}
        | -> Items          | {', '.join(self.elixir)}
        | -> Rides Harley?  | y
        ------------------------------------------

        """)

    ##### PLAYER COMBAT #####

    # the moves themselves
    def consume_item(self, spirit):
        print("SELECT ITEM FROM KNAPSACK:")
        for item in self.elixir:
            print('\t> ',item)

        print()
        item_choice = input("> ")

        if item_choice == 'apple':
            print(dedent(f"""
                Juicy! The sweetness restores some of your health.

                -> PLAYER HEALTH: +2
                """))
            self.health += 2
            self.elixir.pop(self.elixir.index(item_choice))
        elif item_choice == 'meat tart':
            print(dedent(f"""
                Savory! The meat boosts your strength!

                -> PLAYER XP: +2
                """))
            self.XP += 2
            self.elixir.pop(self.elixir.index(item_choice))
        elif item_choice == 'map':
            print(dedent(f"""
                You bite off a corner of the map in desperation and nothing happens. Strange move!
                """))
            self.elixir.pop(self.elixir.index(item_choice))
        elif item_choice == 'necklace':
            print(dedent(f"""
                You pull out the claw necklace and feel the strength of the great bear course through
                your veins. Primal! Raw! Smelling faintly like salmon!

                The spirit takes a step back -- only a worthy warrior possesses such charms!

                -> PLAYER XP: +2
                -> NEXT TURN: 2x CRITICAL STRIKE MULTIPLIER
                """))
            self.XP += 2
            self.elixir.pop(self.elixir.index(item_choice))
            # placing the critical strike multiplier in the player's elixir list
            self.elixir.append('multiplier')
        else:
            print("What's that? This is no time to mess around!")

        return self, spirit

    def eye_poke(self, spirit):
        """A middling strike with average accuracy and attack power"""
        # each combat move has a base damage and an accuracy factor, which is affected by the player's XP
        # these two factors will vary with each attack
        base_damage = (2 + self.XP)
        accuracy = randint(0,3)

        # if the player possesses the multiplier, double the damage to the spirit
        if 'multiplier' in self.elixir:
            base_damage *= 2
            self.elixir.pop(self.elixir.index('multiplier'))

        # then, knock the spirit's health by the total damage done
        total_damage = int(base_damage * accuracy * 0.25)

        # also account for the shield -- this reduces the damage by 2
        if 'shield' in spirit.elixir:
            spirit.elixir.pop(spirit.elixir.index('shield'))
            total_damage -= 2
            if total_damage < 0:
                total_damage = 0
        spirit.health -= total_damage

        # outputs based on the amount of damage done
        if total_damage == 0:
            print(f"Unlucky -- the spirit dodges the poke! No damage done!\n")
        else:
            print(f"Right on target! Fingers meet eye jelly and the spirit takes {total_damage} damage!\n")

            stun_chance = randint(0,9)
            if stun_chance >= 8:
                spirit.elixir.append('frozen')
                print("Blinking in confusion, the spirit is stunned by the attack!")

        return self, spirit

    def stab(self, spirit):
        """A high power, low accuracy attack for dishing out big hits"""
        # each combat move has a base damage and an accuracy factor, which is affected by the player's XP
        # these two factors will vary with each attack
        base_damage = (3 + self.XP)
        accuracy = randint(0,1)

        # if the player possesses the multiplier, double the damage to the spirit
        if 'multiplier' in self.elixir:
            base_damage *= 2
            self.elixir.pop(self.elixir.index('multiplier'))

        # then, knock the spirit's health by the total damage done
        total_damage = int(base_damage * accuracy * 0.25)

        # also account for the shield -- this reduces the damage by 2
        if 'shield' in spirit.elixir:
            spirit.elixir.pop(spirit.elixir.index('shield'))
            total_damage -= 2
            if total_damage < 0:
                total_damage = 0
        spirit.health -= total_damage

        # outputs based on the amount of damage done
        if total_damage == 0:
            print(f"No hit -- the spirit sidesteps your lunge!\n")
        else:
            print(f"A rustle of leaves as your sword pierces the spirit's figure, dishing out {total_damage} damage!\n")

            stun_chance = randint(0,9)
            if stun_chance >= 6:
                spirit.elixir.append('frozen')
                print("Doubled over in pain, the spirit is rattled by the strike!")

        return self, spirit

    def blow(self, spirit):
        """A low power, high accuracy move that can be relied upon for consistent damage. Requires XP > 0"""
        # each combat move has a base damage and an accuracy factor, which is affected by the player's XP
        # these two factors will vary with each attack
        base_damage = (0 + self.XP)
        accuracy = randint(2,3)

        # if the player possesses the multiplier, double the damage to the spirit
        if 'multiplier' in self.elixir:
            base_damage *= 2
            self.elixir.pop(self.elixir.index('multiplier'))

        # then, knock the spirit's health by the total damage done
        total_damage = int(base_damage * accuracy * 0.25)

        # also account for the shield -- this reduces the damage by 2
        if 'shield' in spirit.elixir:
            total_damage -= 2
            spirit.elixir.pop(spirit.elixir.index('shield'))
            if total_damage < 0:
                total_damage = 0
        spirit.health -= total_damage

        # outputs based on the amount of damage done
        if total_damage == 0:
            print(f"The spirit is unaffected!\n")
        else:
            print(f"The spirit's form flutters for a moment as it takes {total_damage} damage!\n")

            stun_chance = randint(0,9)
            if stun_chance >= 9:
                spirit.elixir.append('frozen')
                print("The spirit is stunned by your breath! Whew, is that meat tart?")

        return self, spirit

    def suicide(self, spirit):
        """Kills self"""
        print(dedent("""
        You know your time has come. Preservation of honor is preferable to a death in shame.

        Turning your sword inward toward your chest, you plunge it deep and shudder, gasping your last breath.
        """))
        self.health = 0

        return self, spirit

    # dictionary storing the different moves available, later to be called as functions
    move_options = {
        '1. consume item': consume_item,
        '2. eye poke': eye_poke,
        '3. stab': stab,
        '4. blow really hard': blow,
        '5. suicide': suicide
    }

    # And then the function that aggregates those as available subroutines
    def player_move(self, spirit):
        """Call this for each turn of the player in combat"""

        # print available moves
        print(f"\nCHOOSE A MOVE, {self.name}:\n")
        for option in self.move_options:
            print('\t',option)
        print()

        # take user input for which number move they'd like to execute
        try:
            turn_action = int(input("Select your move: "))
        except ValueError:
            print("\nWhat!? This is no time for tomfoolery!\n")
            return self, spirit

        # iterate through the move_options dictionary to find the function that matches the user's input
        # then set the move_key to the corresponding key in the dictionary
        # we'll call this move key when it's time to run the function
        move_key = ''
        for option in self.move_options:
            if int(option[0]) == turn_action:
                move_key = option

        # calling the appropriate function with the necessary parameters
        # and printing the user's choice prior to calling the move
        if move_key in self.move_options:
            print(dedent(f"""
            {self.name} chooses {move_key[3:]}!
            """))

            self.move_options[move_key](self, spirit)
        else:
            print("\nWho taught you to read?! This is no time for tomfoolery!\n")

        return self, spirit



class Spirit(object):

    def __init__(self, spiritHealth, spiritAttack, spiritElixir):
        self.health = spiritHealth
        self.attack = spiritAttack
        self.elixir = spiritElixir

    def spirit_status(self):
        """Prints the spirit's attributes"""
        print(f"""

        ------------------------------------------
        |            ~ SPIRIT STATUS ~           |
        | ----------------------------------------
        | -> Health         | {self.health}
        | -> Attack Power   | {self.attack}
        ------------------------------------------

        """)

    def immortality(self, player):
        print(dedent("""
            Calling upon the healing wisdom of the forest, the spirit uses IMMORTALITY.
            Leaves swirl about from the ground around you, collecting upon its figure.

            -> Spirit Health: +2
            -> Spirit Shield: +2
            """))
        self.health += 2
        self.elixir.append('shield')

        return player, self

    def boil_blood(self, player):

        print("\nThe spirit summons BOIL BLOOD. Menacing clouds swirl overhead.")

        # establish the damage of the attack based on attack power and accuracy
        base_damage = (2 + self.attack)
        accuracy = randint(0,3)

        # then, knock the player's health by the total damage done
        total_damage = int(base_damage * accuracy * 0.25)

        # outputs based on the amount of damage done
        if total_damage == 0:
            print("\nFortunately, there's no effect! Such a curse can have a mind of its own at times...")
        else:
            print(dedent(f"""
                Your limbs start to seize up... a vicious burn emanates from every inch of your flesh
                as your very essence is thrashed from the inside by the spirit's dark magic!

                -> {player.name} takes {total_damage} damage!
                """))
            player.health -= total_damage

        return player, self

    def entangle(self, player):
        print("\nThe spirit uses ENTANGLE. Vines creep from all directions, growing and spiraling toward you.")

        # establish the damage of the attack based on attack power and accuracy
        base_damage = (1 + self.attack)
        accuracy = randint(0,4)

        # then, knock the player's health by the total damage done
        total_damage = int(base_damage * accuracy * 0.25)

        # outputs based on the amount of damage done
        if total_damage == 0:
            print("\nYou slash and dodge your way through the onslaught! No damage done!")
        else:
            print(dedent(f"""
                Despite your best efforts to cut your way through the thorny onslaught, it's too much! Your
                arms and legs are completely restricted by the tightening grip of the forest!

                -> {player.name} takes {total_damage} damage!
                -> {player.name} is immobilized!
                """))
            player.health -= total_damage
            player.elixir.append('frozen')

        return player, self

    def sacred_deer(self, player):
        print("\nThe spirit calls SACRED DEER. You notice a disturbing glow approaching from deep in the woods...")

        # establish the damage of the attack based on attack power and accuracy
        base_damage = (6 + self.attack)
        accuracy = randint(0,1)

        # then, knock the player's health by the total damage done
        total_damage = int(base_damage * accuracy * 0.25)

        # outputs based on the amount of damage done
        if total_damage == 0:
            print("\nThe deer's whims are on your side! With a mind of its own, it never sets foot in the grove.")
        else:
            print(dedent(f"""
                You squint as the light becomes blinding. Raising your arm to protect your eyes, you're met
                with the sudden force of a runaway ox-cart as the sacred deer's antlers pierce your side.

                -> {player.name} takes {total_damage} damage!
                """))
            player.health -= total_damage

            if 'necklace' in player.elixir:
                player.elixir.pop(player.elixir.index('necklace'))
                print(f"-> {player.name} drops the Bear Claw Necklace!")

        return player, self

    def spirit_move(self, player):
        """Call this for each turn of the spirit in combat"""

        ### making the spirit's move ###
        # first, randomly select a spirit move based on a simple weighting
        randomize_move = random()

        # then selecting the corresponding spirit move based on the random float value
        total = 0.0
        select_move = ''
        for key in self.move_options:
            total += self.move_options[key]
            if total >= randomize_move:
                select_move = key
                break

        # and then finally calling the spirit's move
        select_move(self, player)

        return player, self

    # the spirit's move options and their corresponding probabilities
    move_options = {
        immortality: 0.2,
        boil_blood: 0.3,
        entangle: 0.3,
        sacred_deer: 0.2,
    }







#
