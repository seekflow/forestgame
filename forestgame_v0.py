from random import randint, random
from textwrap import dedent
import forestcombat


class Engine(object):

    # initializing the player and the spirit by calling to forestcombat
    def initialize_characters(self, mode, player_name):
        """Sets up the player and spirit characters based on the initial dosage"""

        player_attributes, spirit_attributes = forestcombat.gamemode(mode)
        name = player_name.lower()

        player_1 = forestcombat.Player(name, player_attributes['health'], player_attributes['XP'], player_attributes['elixir'])
        forest_spirit = forestcombat.Spirit(spirit_attributes['health'], spirit_attributes['attack_power'], [])

        return player_1, forest_spirit

    def play_scene(self, scene, map, player, spirit):
        """Plays a given scene and returns the name of the next scene, along with the player, spirit, and mode"""
        new_scene = map[scene]
        next_scene, player, spirit = new_scene.enter(player, spirit)

        return next_scene, player, spirit

    def play_game(self):
        """Plays the game"""

        # initializing the appropriate variables for the rooms and the map
        game_map = Map()
        scenes = game_map.scene_map
        active_game = 'Y'

        # setting the starting version of the variables that will be fed into each room / play function
        # also taking player input for the name, to be fed in as the name for the player character
        current_scene = 'forest_entrance'

        # initializing the player and the spirit, which will be passed into each room's enter() function
        player_1, forest_spirit = '', ''

        # loop that runs through the duration of the game using the variables already created
        while active_game == 'Y':
            current_scene, player_1, forest_spirit = self.play_scene(current_scene, scenes, player_1, forest_spirit)

            if current_scene == 'fin':
                active_game = 'N'

        # allowing the player to run it back
        play_again = input(">> Would you like to play again? Y or N: ")

        if play_again == 'Y':
            round_two = Engine()
            round_two.play_game()



"""

# SCENES
#
#
#
#



"""

class Death(object):

    def enter(self, player, spirit):

        quips = [
            "Life and death are illusions. We are in a constant state of transformation.",
            "Life and death are one thread, the same line viewed from different sides.",
            "Serenity is the balance between good and bad, life and death, horrors and pleasures. Life is, as it were, defined by death. If there wasn't death of things, then there wouldn't be any life to celebrate.",
            "If you make every game a life and death proposition, you're going to have problems. For one thing, you'll be dead a lot.",
            "Life and death are important. Don't suffer them in vain.",
            "Nothing is a matter of life and death except life and death.",
            "When confronted with two alternatives, life and death, one is to choose death without hesitation.",
            "Do not be afraid of death. Just try not to be there when it happens.",
        ]

        quip = randint(0,len(quips) - 1)

        print(dedent(f"""
            Woozy, you feel your light fading. The last patch of sky spins in your dimming
            vision and the chirp of the forest becomes muffled...

            ~

            You awaken, sprawled at the entrance of the forest. Weary, confused, and with a
            headache known not by even the heaviest of mead drinkers, you gather yourself
            before a long trudge back to the village. Perhaps you'll eventually discover the
            secrets of the forest, but today is not that day.

            Please dear traveler, do return.

            Your journey is not yet over, {player.name}.


                        x
                    ~       ~
                ~               ~
            ~                       ~
        ~                               ~

    {quips[quip]}

                """))

        return 'fin', player, spirit


class ForestEntrance(object):
    # where the player enters the forest
    def enter(self, player, spirit):


        print(dedent("""
            You come upon a massive grove of trees, each one reaching
            hundreds of feet into a blue sky dotted with fluffy marshmallow clouds.

            A path before you stretches deep into the forest, darkening and twisting
            out of sight. This must be the enchanted forest the villagers were
            talking about back in town.

            You pull your knapsack higher up on your back and absentmindedly reach your hand
            to the hilt of your grandfather's sword. This is where heroes are made, they say.
            Let's find out if that's true...
            """))

        cont = input("~\n\nPress ENTER to continue ")

        return 'mushroom_patch', player, spirit


class MushroomPatch(object):

    def enter(self, player, spirit):
        print(dedent("""
            As you stroll down the path, the trees begin to blot out the clear
            blue sky. You keep walking, going deeper and deeper into the darkness
            of the forest.

            After the passing of what feels like hours, you notice a lone column of
            sunlight shining down from the canopy. Smiling rays illuminate
            a patch of ground to the side of the dirt trail.

            Curious, you step closer to the golden foliage basking in the sun and
            behold a patch of mushrooms. Large red caps with white spots beckon,
            bouncing left and right with joy.

            You reach toward the dozen or so mushrooms and let the sun
            warm the back of your hand. Pausing, you recall the village baker
            mentioning that most people can withstand only 10 of the
            innocent-looking little fellas. There must be at least 20 here...
            """))

        dosage = input(">> How many do you want to take? ")

        print()

        try:
            dosage = int(dosage)
        except ValueError:
            print(dedent("""
                Without mathematics, there's nothing you can do.
                Everything around you is mathematics.
                Everything around you is numbers.

                - Shakuntala Devi

                Please my friend, input a number.

                """))
            return 'mushroom_patch', player, spirit

        if dosage == 6900:
            print("You instantly transcend your physical form. Immediately advance to GO and collect $400.")
            mode = 'none'
            next_room = 'enlightenment'
        elif dosage > 40:
            print("There aren't that many mushrooms here! Try again...\n")
            mode = 'none'
            next_room = 'mushroom_patch'
        elif dosage <= 40 and dosage > 20:
            print("That's enough to sedate an elephant! You are not yet ready, my friend...\n")
            mode = 'none'
            next_room = 'death'
        elif dosage <= 25 and dosage >= 15:
            print("Enough to sedate a horse... scrumptious!\n")
            mode = 'hard'
            next_room = 'forest_clearing'
        elif dosage < 15 and dosage >= 10:
            print("You're in for a ride... scrumptious!\n")
            mode = 'medium'
            next_room = 'forest_clearing'
        elif dosage < 10:
            print("A conservative approach... scrumptious!\n")
            mode = 'easy'
            next_room = 'forest_clearing'
        else:
            print("Are you sure you ate anything?\nLet's try this again...\n")
            next_room = 'mushroom_patch'


        # this is where we also affect the player and spirit attributes... probably don't need to pass gamemode through
        # every function... could clean that up later

        # what is the best way to affect the player and spirit's attributes now? I already have a name for the player...
        # if I take it out of the play() function, I need to change player_name to a user input
        print(dedent(f"""
            >> GAMEMODE: {mode}
            """))

        player_name = input("\n>> Remind me... what is your name, weary traveler? ")

        player, spirit = Engine.initialize_characters(self, mode, player_name)

        cont = input("\n~\n\nPress ENTER to continue ")

        return next_room, player, spirit


class ForestClearing(object):

    def enter(self, player, spirit):
        print(dedent(f"""
            As you continue your march deeper into the wood, the thicket of
            trees starts to pulse and sway, welcoming your presence. Drawing you deeper.

            A clearing opens up before you. Sparkling in the light of a long midsummer's day is
            a glassy lake, fed by a fearsome river of ages old.

            You close your eyes and for a moment, simply enjoy the view.

            -> PLAYER XP: +1
            """))
        player.XP += 1

        cont = input("~\n\nPress ENTER to continue ")

        # printing the player's attributes
        player.player_status()

        cont = input("~\n\nPress ENTER to continue ")

        print(dedent(f"""
            Suddenly, a chilling breeze cuts across your body. Your hair stands on end, charged by
            the faint electricity of an ancient wind.

            Your senses peak. Sharp inhale. Eyes open.

            You capture the briefest flash of movement in the direction of the babbling stream. Your heart
            jumps a beat -- the forest spirit! It's time to move, {player.name}!
            """))

        cont = input("~\n\nPress ENTER to continue ")

        print(dedent(f"""
            To the left of the water is a dense thicket of thorns. To the right, an old oak
            scarred by the claws of a massive beast. Beached and bleached, a wooden raft lies at the foot
            of the lake. Years of lying under the eternal sun of the forest have left their mark.

            SELECT ACTION:

            1. Go left.
            2. Go right.
            3. Board the raft.
            """))

        raw_input = input(">> Choose a path: ")

        try:
            action = int(raw_input)
        except ValueError:
            print("\nPlease, do try again.\n")
            next_room = 'forest_clearing'
            return next_room, player, spirit

        if action == 1:
            print(dedent("""
                You begin scrambling through the thorns. Pricks of blood dot your skin as
                you hack your way along. But these plants, not unlike the trees and mushrooms before them,
                are enchanted with the life of the forest. They begin to weave themselves about you, wrapping around
                your arms and legs. Tightening... Suffocating...
                """))
            next_room = 'death'
        elif action == 2:
            print(dedent("""
                Few have seen a forest bear and lived to tell the tale, but you follow your intuition past
                the telltale claw marks of one such behemoth. Legend has it that even their young can
                swallow a man whole, but the reward for a bear slayer can be -- * GASP *

                A near imperceptible rustle of leaves from behind stops you cold.
                """))

            cont = input("~\n\nPress ENTER to continue ")

            print(dedent(f"""
                Hoping to the heavens that it doesn't know it's entered your awareness, you silently slide
                your hand to the hilt of your sword. In one crisp, rehearsed stroke, you pivot your torso and come
                down with the force of god toward of the monster.
                """))

            cont = input("~\n\nPress ENTER to continue ")

            print(dedent(f"""
                Its head rolls past your outretched foot. Your gasping breath hangs in the otherwise silent air.
                Had you waited a moment longer, the bear's lunge would have opened your torso from neck to waist.

                The gash across your arm won't be too much to bandage, fortunately. The villagers still may
                be slow to believe you, but this can't hurt your credibility. Maybe sailing was a better idea,
                you think to yourself...

                You go back to shore and load the raft for a voyage across the lake.

                -> PLAYER HEALTH: -2
                -> PLAYER XP: +1
                -> NEW ITEM: Bear Claw Necklace [Necklace]
                """))
            player.health -= 2
            player.XP += 1
            player.elixir.append('necklace')
            next_room = 'waterfall'
        elif action == 3:
            print(dedent("""
                You throw your gear onto the raft and give it a hard shove off of the sand.
                It creaks and groans as it bobs out onto the crystal blue water in front of you.

                You leap! The corner of the raft dips below the surface violently and you fall forward onto
                your knapsack. But just as suddenly, the old planks right themselves. You're sailing now.
                """))
            next_room = 'waterfall'
        else:
            print("\nHuh?\n")
            next_room = 'forest_clearing'

        cont = input("~\n\nPress ENTER to continue ")

        # printing the player's attributes
        player.player_status()

        return next_room, player, spirit


class Waterfall(object):

    def enter(self, player, spirit):
        print(dedent(f"""
            ~

            Storms threaten on the horizon but fortunately, their dance keeps to the far edges of the boundless lake.
            Sailing is effortless, as the winds are taking you straight to where you know the lake ends.

            You realize how long it's been since you last ate. Now could be a great time to restore your vitality
            and prepare for the remainder of the voyage. You have {' and '.join(player.elixir)} in your pack.
            """))

        snack = input(">> Type food or if you're not hungry, 'no': ")

        if snack == 'apple':
            print(dedent(f"""

            -> {player.name} CONSUMES APPLE

            Great choice. A juicy fruit under the hot sun restores you.

            -> PLAYER HEALTH: +2
            """))
            player.health += 2
            player.elixir.pop(0)
            next_room = 'sacred_tree'
        elif snack == 'meat tart':
            print(dedent(f"""

            -> {player.name} CONSUMES MEAT TART

            Great choice. A bit salty on an already parched tongue, but restorative nonetheless.

            -> PLAYER XP: +3
            """))
            player.XP += 2
            player.elixir.pop(1)
            next_room = 'sacred_tree'
        elif snack == 'no':
            print(dedent(f"""

            As you keep your focus on the shifting waters around you, you notice a glass bottle bobbing
            along the foam of the white caps. You reach down into the salty spray to snag it.

            Inside the corked green glass is a faded old map.

            -> NEW ITEM: Swashbuckler's Survey [Map]
            """))
            player.elixir.append('map')
            next_room = 'sacred_tree'
        else:
            print("What's that?\n")
            next_room = 'waterfall'
            return next_room, player, spirit


        cont = input("~\n\nPress ENTER to continue ")

        # printing the player's attributes
        player.player_status()

        # the next phase of the room
        print(dedent("""

            Finally, you spot land.

            ~

            Your raft slides up onto the sand about 50 yards from a great river whose mouth feeds the lake.
            Amongst massive pines reminiscent of those at the entrance of the forest, you trace the river's
            winding path until it splits into two equally-sized tributaries. Neither of them seems like
            the obvious way to go...
            """))

        if 'map' in player.elixir:

            cont = input("~\n\nPress ENTER to continue ")

            print(dedent("""
                You pull out the tattered map from your knapsack. Yellowed and faded as it is, it clearly shows the left
                hand path leading directly to the sacred tree at the heart of the enchanted forest. Your pulse jumps.
                This means you're finally getting close!
                """))
        else:
            direction = input(">> Choose path, L or R: ")

            if direction == 'L':
                print(dedent("""
                    Navigating to a shallow section of the river, you wade across to the left bank. As you start
                    tracking up the path, you notice a faint buzz. Bees!
                    """))

                cont = input("~\n\nPress ENTER to continue ")

                if 'apple' in player.elixir:
                    print(dedent("""
                        They start to land on you one by one, smelling the apple in your knapsack. With a pinpoint heat like
                        that of the blacksmith's forge, their curiousity flips to fury as they start to sting...


                        * SPLASH *


                        Even underwater, you can still hear the hum of the swarm a mere feet above your head.
                        You keep your head under until your lungs are ready to burst...
                        """))

                    cont = input("~\n\nPress ENTER to continue ")

                    print(dedent(f"""
                        Gasping for air, you brace for more stinging...

                        Nothing! It seems you've waited them out. You swim past the hive to be safe, and then climb back out to
                        the safety of dry land. The sacred tree at the heart of the enchanted forest can't be much further.

                        PLAYER HEALTH: -2
                        PLAYER XP: +1
                        """))
                    player.health -= 2
                    player.XP += 1
                else:
                    print(dedent("""
                        Fortunately, you offloaded your apple on the raft. Otherwise, the bees would have smelled you
                        crossing beneath their massive hive. You continue to slink alongside the charging waters.

                        The sacred tree at the heart of the enchanted forest can't be much further.
                        """))
            elif direction == 'R':
                print(dedent("""
                    You resume your course along the right half of the river. The path begins to slope downward and your feet
                    start to stick for a split second more when you try to pick them up. With each step, your foot
                    sinks just a bit deeper into the softening earth below you.

                    It's really getting difficult to walk as the mud thickens. You nearly fall as your left heel
                    gets stuck -- stopping to catch your balance, you notice yourself sinking. Quicksand!
                    """))

                cont = input("~\n\nPress ENTER to continue ")

                if 'meat tart' in player.elixir:
                    print(dedent("""
                        Desparately, you lift your arms up toward your head to keep them from getting stuck. Attempting
                        to roll onto your back to distribute your weight on the surface, you remember the thick meat tart
                        in your knapsack -- its beefy bulk is getting caught and dragging you deeper...
                        """))

                    cont = input("~\n\nPress ENTER to continue ")

                    print(dedent(f"""
                        Only after sinking nearly to the bottom and finding a tree root to pull yourself up with, you
                        emerge on the other side of the sand pit. Caked with thick mud, you're just grateful to be alive
                        and back on the trail. The sacred tree at the heart of the enchanted forest can't be much further.

                        PLAYER HEALTH: -2
                        PLAYER XP: +1
                        """))
                    player.health -= 2
                    player.XP += 1
                else:
                    print(dedent("""
                        With grace, you roll onto your back to spread your weight evenly across the surface of the quicksand.

                        Fortunately, you offloaded your meat tart on the raft. Otherwise, its thick meaty bulk would
                        have gotten caught in the mud and made that maneuver much more difficult.

                        You get back on your feet and resume your journey.
                        The sacred tree at the heart of the enchanted forest can't be much further.
                        """))

            else:
                print("What's that you say? Let's try this again.\n")
                next_room = 'waterfall'

        cont = input("~\n\nPress ENTER to continue ")

        # printing the player's attributes
        player.player_status()

        return next_room, player, spirit


class SacredTree(object):

    def enter(self, player, spirit):
        # dialogue once the player enters the room
        print(dedent(f"""
            A grove of ancient trees opens before you. Ancestral whisperings feather about as you step into the ring.

            An infinite tangle of vines spirals up the behemoth of a tree in the center of the rotunda. The air, cool,
            humming with static energy, chills you to your bones.
            """))

        cont = input("~\n\nPress ENTER to continue ")

        print(dedent(f"""
            Realizing you're holding your breath, you begin to let it out slowly through pursed lips. Just as you do,
            leaves swirl about, faster and faster in front of the central trunk. The whispers grow louder, louder, louder!

            Then nothing. Pure silence.

            The whirlwind of leaves slows, settling into a human-shaped figure in front of the central trunk.
            """))

        cont = input("~\n\nPress ENTER to continue ")

        print(dedent(f"""
            With the rasp of eternal wisdom, a deep voice shakes loose from the swirl of leaves.

            FOREST SPIRIT:  I AM THE FOREST SPIRIT, SPIRIT OF FORESTS
                            WELCOME TO DIE

            {player.name}:      ...
            """))

        cont = input("~\n\nPress ENTER to continue ")

        print(dedent(f"""
            FOREST SPIRIT:  THE SECRETS OF THE ENCHANTED FOREST MAKE THEMSELVES KNOWN TO NO MERE MORTAL
                            I SHALL BREAK YOU A THOUSAND TIMES, THEN BUILD YOU ANEW,
                            THAT YOU MIGHT DIE ANOTHER DEATH

            {player.name}:      uh oh.

            ______________________________________________________________________________________________

            """))

        cont = input("~\n\nPress ENTER to continue ")

        player.player_status()
        spirit.spirit_status()

        cont = input("~\n\nLet the battle begin! ")

        # while-loop that runs through the battle
        # this will be composed of a player move (then CHECK) followed by a spirit move (CHECK again)
        while True:

            # PLAYER TURN >> first test if the player gets a turn
            if 'frozen' in player.elixir:
                print(f"\nTry as you might, you're unable to attack!")
                player.elixir.pop(player.elixir.index('frozen'))
            else:
                # call player_move function from forestcombat
                # pulls from other methods in Player() and then appropriately alters both the player and the spirit
                player.player_move(spirit)

                cont = input("\n~\n\nPress ENTER to continue ")

                # check for player death, followed by spirit death
                if player.health <= 0:
                    print(dedent("""
                        The battle is over nearly as quickly as it began.
                        """))
                    return 'death', player, spirit
                elif spirit.health <= 0:
                    print(dedent("""
                        In disbelief, you stare ahead as the spirit howls in rage. The remaining leaves fall
                        away from its wispy form. It's a CRITICAL strike!
                        """))
                    return 'enlightenment', player, spirit

            # SPIRIT TURN >> similar to the player's turn
            if 'frozen' in spirit.elixir:
                print(f"\nThe spirit, unable to move, fails to launch a counter!")
                spirit.elixir.pop(spirit.elixir.index('frozen'))

                print("\nTURN SUMMARY:")
                player.player_status()
                spirit.spirit_status()
                print("______________________________________________________________________________________________\n")
                cont = input("~\n\nPress ENTER to continue ")
            else:
                # call spirit_move function from forestcombat
                # pulls from other methods in Player() and then appropriately alters both the player and the spirit
                spirit.spirit_move(player)

                cont = input("~\n\nPress ENTER to continue ")
                print("\nTURN SUMMARY:")
                player.player_status()
                spirit.spirit_status()
                print("______________________________________________________________________________________________\n")
                cont = input("~\n\nPress ENTER to continue ")

                # check for player death, followed by spirit death
                if player.health <= 0:
                    print(dedent("""
                        With that strike, the spirit's assault has become too much for your mortal fiber.
                        The battle is over nearly as quickly as it began.
                        """))
                    return 'death', player, spirit

            # then repeat until either the spirit or the player is exhausted

        return next_room, player, spirit


class Enlightenment(object):

    def enter(self, player, spirit):
        print(dedent("""
            A chilling breeze once more sweeps through the grove, taking with it the last indications
            of the spirit's formerly strong figure. You've defeated the spirit, in all its wisdom and strength.

            From the middle tree, vines start to unravel, revealing an arching doorway. It calls to you.
            """))

        cont = input("~\n\nPress ENTER to step through the doorway ")

        print(dedent("""
            Inside, a hearth. As you peer into its licking flames, you see dancing visions of the villagers. Next,
            the dirt trail leading to the forest. The forest's entrance. The mushroom patch smiles back,
            sensing your awareness. You feel every inch of the forest coming to form within the flames.

            From deep in your chest, you feel the fire reflected within you, too. It's telling you something.
            Offering you something... you look down and see yourself staring back.
            """))

        cont = input("~\n\nDo you accept the forest's call? ")

        print(dedent("""
            From the bottom up, your body begins to evaporate -- momentary panic, replaced by a building sense
            of understanding...

            Having proven yourself worthy, you've assumed the mantle of the forest spirit. Blessed with the wisdom
            of interconnectedness, you can feel every tree, every blade of grass, as if they were your own limbs.

            The web of life extends through you as a central node. As its new keeper.
            """))

        cont = input("~\n\nPress ENTER to continue ")

        print(dedent(f"""
            You did battle with the most formidable enemy this world has known, and came out the other side
            to assume its place as enlightened protector of the enchanted forest.

            Congratulations, {player.name}, for you have found all that you were seeking and more.


            fin.

            ______________________________________________________________________________________________

            """))


        return 'fin', player, spirit


class Map(object):

    # storing the mapping from scene output to engine input (simple dict)
    scene_map = {
        'death': Death(),
        'forest_entrance': ForestEntrance(),
        'mushroom_patch': MushroomPatch(),
        'forest_clearing': ForestClearing(),
        'waterfall': Waterfall(),
        'sacred_tree': SacredTree(),
        'enlightenment': Enlightenment()
    }




test = Engine()
test.play_game()
