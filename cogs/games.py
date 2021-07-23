#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from random import choice, randint
from collections import Counter
from pengaelicutils import hangman_words, regional_indicators


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    name = "games"
    name_typable = name
    description = "All sorts of fun stuff!"
    description_long = description

    @commands.command(
        name="8ball",
        help="Ask the ball and receive wisdom... :eyes:",
        aliases=["magic8ball"],
        usage="[question]",
    )
    async def magic_8_ball(self, ctx, *, question=None):
        if question:
            await ctx.send(
                ":8ball:"
                + choice(
                    choice(
                        [
                            [
                                r"¯\\\_(ツ)\_/¯",
                                ":(\nYour computer ran into a problem and needs to restart",
                                "Answer is kinda hazy rn... Try again later",
                                "Ask again later",
                                "Better not tell you now",
                                "Cannot predict now",
                                r"Can't tell ¯\\\_(ツ)\_/¯",
                                "Concentrate and ask again",
                                "Concentrate harder and ask again",
                                "Couldn't tell ya if I wanted to, pal",
                                "idk lol",
                                "I like to keep secrets",
                                "I'm busy",
                                "`panic: cannot mount volume /dev/disk-by-label/8-Ball-Responses`",
                                "Probably shouldn't tell you now, lol",
                                "Reply hazy... Try again",
                                "The universe is weird sometimes... I can't find an answer",
                                "Try again, but harder",
                                "Try again later",
                                "Why would you ask such a stupid question?",
                            ],
                            [
                                "Don’t count on it",
                                "Don’t count on it, buster",
                                "Heck no",
                                "I don't think so",
                                "I don't think so, pal",
                                "I doubt it",
                                "LOL, no",
                                "My reply is no",
                                "My sources say no",
                                "My sources say no. My sources are Wikipedia",
                                "Not a chance",
                                "Outlook is terrible. Get Thunderbird instead",
                                "Outlook not so good",
                                "Outlook not so good. Use Gmail instead",
                                "Pfft, don’t count on it",
                                'The law requires that I answer "no"',
                                "Very doubtful",
                                "Uh, no",
                                ":thumbsdown:",
                                ":x:",
                            ],
                            [
                                "Absolutely",
                                "Always",
                                "Always and forever",
                                "Certainly",
                                "Definitely",
                                "Definitively",
                                "Doubtless",
                                "I'd say so",
                                "It is certain",
                                "It is decidedly so",
                                "I think so",
                                "I would think so",
                                "I'm pretty sure, yeah",
                                "It is obvious",
                                "Lookin' good",
                                "Maybe...",
                                "mhm",
                                "Most likely",
                                "Obviously",
                                "Oh yeah",
                            ],
                            [
                                "Outlook good",
                                "Pfft, yeah!",
                                "Probably lol",
                                "Probably",
                                "Seems like it",
                                "Signs point to yes",
                                "Sure",
                                "Sure, why not?",
                                "Totally",
                                "Uh... yeah!",
                                "Without a doubt",
                                "ye",
                                "Yeah",
                                "Yeah, sure",
                                "Yeah, totally!",
                                "Yep",
                                "Yes",
                                "You may rely on it",
                                ":thumbsup:",
                                ":white_check_mark:",
                            ],
                        ]
                    )
                )
            )
        else:
            await ctx.send(":8ball:You didn't ask the 8-ball anything.")

    @commands.command(
        name="roll",
        help="Roll some dice!",
        aliases=["dice"],
        usage="[number of dice (1)]\n[number of sides (6)]",
    )
    async def roll_dice(self, ctx, dice: int = 1, sides: int = 6):
        if dice == 0:
            response = "You didn't roll any dice."
        elif sides == 0:
            response = "You rolled thin air."
        elif dice < 0:
            response = "You rolled NaN dice and got [REDACTED]"
        elif dice > 1000000:
            response = f"{dice} dice? That's just silly."
        elif sides < 0:
            if dice == 1:
                response = "You rolled a [ERROR]-sided die and got `DivideByZeroError`"
            if dice > 1:
                response = f"You rolled {dice} `err`-sided dice and got [NULL]"
        elif sides > 1000000:
            response = f"{sides}-sided dice? That's just silly."
        else:
            side_list = [side for side in range(1, sides)]
            roll_results = [
                side_list[randint(0, side_list[-1]) - 1] for _ in range(dice)
            ]
            total = sum(roll_results)
            if dice > 1:
                if len(str(roll_results[:-1])[1:-1]) < 2000:
                    response = f"{str(roll_results[:-1])[1:-1]}, and {roll_results[-1]}, totalling {total}"
                else:
                    response = f"a total of {total}"
            else:
                response = str(total)
        await ctx.send(":game_die:You rolled " + response)

    @commands.command(
        name="flip",
        help="Flip some coins!",
        aliases=["coin", "coinflip"],
        usage="[number of coins (1)]",
    )
    async def flip_coins(self, ctx, coins: int = 1):
        if coins == 1:
            response = f"You flipped a {choice(['head', 'tail'])}"
        elif coins == 0:
            response = "You flicked your thumb in the air."
        elif coins == -1:
            response = "You flipped a [REDACTED]"
        elif coins < -1:
            response = "You flipped NaN heads and [ERROR] tails."
        else:
            if coins > 1000000:
                response = f"{coins} coins? That's just silly."
            else:
                results = [randint(0, 2) for _ in range(coins)]
                for _ in range(10):
                    if 2 in results:
                        for result in range(len(results)):
                            if results[result] == 2:
                                results[result] = randint(0, 2)
                if results.count(2) > 0:
                    if results.count(2) == 1:
                        response = ", and a coin even landed on its edge."
                    else:
                        response = (
                            f", and {results.count(2)} coins landed on their edges."
                        )
                else:
                    response = "."
                response = f"You flipped {results.count(0)} heads and {results.count(1)} tails{response}"
        await ctx.send(":moneybag:" + response)

    @commands.command(
        name="draw",
        help="Draw some cards!",
        aliases=["card"],
        usage="[number of cards (1)]\n[replace cards in deck (False)]",
    )
    async def draw_cards(self, ctx, cards: int = 1, replace_cards: bool = False):
        suits = ["Diamonds", "Spades", "Hearts", "Clubs"]
        values = {
            1: "Ace",
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10,
            11: "Jack",
            12: "Queen",
            13: "King",
        }
        all_cards = []
        faces = []
        numbers = []
        drawn = []
        if replace_cards:
            for _ in range(cards):
                random_value = str(choice(list(values.values())))
                card = str(
                    random_value
                    + (" " * (6 - len(random_value)))
                    + "of "
                    + choice(suits)
                )
                if card[1] == "0" or card[1] == "1" or card[1] == "2" or card[1] == "3":
                    faces.append(card)
                else:
                    numbers.append(card)
            drawn = faces + numbers
        else:
            for suit in range(int(len(suits) / 1)):
                for value in values:
                    if value == 10:
                        length = 2
                    elif value == 1:
                        length = 3
                    elif value == 11 or value == 13:
                        length = 4
                    elif value == 12:
                        length = 5
                    else:
                        length = 1
                    all_cards.append(
                        str(values[value]) + (" " * (6 - length)) + "of " + suits[suit]
                    )
            if cards > 52:
                await ctx.send(":black_joker:You can't draw more than the entire deck!")
                return
            elif cards == 52:
                await ctx.send(
                    ":black_joker:You picked up the entire deck. What was the point of that?"
                )
                return
            else:
                for _ in range(cards):
                    card = choice(all_cards)
                    if (
                        card[1] == "0"
                        or card[1] == "1"
                        or card[1] == "2"
                        or card[1] == "3"
                    ):
                        faces.append(card)
                    else:
                        numbers.append(card)
                    all_cards.remove(card)
                drawn = faces + numbers
        if cards == 1:
            while "  " in drawn[0]:
                drawn[0] = drawn[0].replace("  ", " ")
            await ctx.send(f":black_joker:You drew {drawn[0]}")
        else:
            await ctx.send(
                ":black_joker:You drew...```{}```".format(
                    str(drawn)[1:-1].replace("'", "").replace(", ", "\n")
                )
            )

    @commands.command(
        name="pop",
        help="Get a sheet of bubble wrap! Click to pop.",
        aliases=["bubblewrap", "bubbles"],
        usage="[size of sheet (5x5 or 5)",
    )
    async def bubblewrap(self, ctx, size: str = "5"):
        try:
            if len(size) == 5:
                width = int(size[0:1])
                height = int(size[3:4])
            elif len(size) == 4:
                if "x" == size[1]:
                    width = int(size[0])
                    height = int(size[2:3])
                elif "x" == size[2]:
                    width = int(size[0:1])
                    height = int(size[3])
            elif len(size) == 3:
                width = int(size[0])
                height = int(size[2])
            elif len(size) == 2 or len(size) == 1:
                width = int(size)
                height = int(size)
            else:
                raise (SyntaxError)
            if width > 10 or height > 10:
                raise (SyntaxError)
        except SyntaxError:
            await ctx.send(
                "Invalid size parameter. Use just a single number or two numbers with an `x` in between (e.g. `3x5`), and no larger than `10x10`"
            )
            return
        sheet = ""
        for _ in range(height):
            sheet = (
                sheet
                + str(["||pop||" for _ in range(width)])[1:-1]
                .replace("'", "")
                .replace(", ", "")
                + "\n"
            )
        await ctx.send(sheet)

    @commands.command(
        name="hangman",
        help="A classic! Guess the letters to solve the word before you run out of attempts.",
    )
    async def hangman(self, ctx):
        word = choice(list(hangman_words.keys()))
        vowels = 0
        for i in word:
            if i in ["a", "e", "i", "o", "u", "y"]:
                vowels += 1
        await ctx.send(
            f"React to this message and guess the word.\nHINT: The word has {vowels} vowels."
        )
        the_word = await ctx.send(" ".join(list("_" * len(word))).replace("_", "\_"))
        # list for storing the letters guessed by the player
        past_guesses = ""
        letter_guessed = ""
        chances = 6
        correct = 0
        flag = False
        chance_counter = await ctx.send(f"{chances} chances remaining.")
        while (
            chances != 0
        ) and flag == False:  # flag is updated when the word is correctly guessed

            def check(reaction, user):
                return user == ctx.author and reaction.emoji in list(
                    regional_indicators.keys()
                )

            reaction, user = await self.client.wait_for("reaction_add", check=check)
            if user:
                guess = regional_indicators[reaction.emoji]
            # Validation of the guess
            if not guess.isalpha():
                await ctx.send("Enter only a letter!")
            elif len(guess) > 1:
                await ctx.send("Enter only a SINGLE letter")
            elif guess in letter_guessed or guess in past_guesses:
                await ctx.send("You have already guessed that letter")
            elif guess in word:  # If letter is guessed correctly
                k = word.count(
                    guess
                )  # k stores the number of times the guessed letter occurs in the word
                for _ in range(k):
                    letter_guessed += (
                        guess  # The guess letter is added as many times as it occurs
                    )
            else:  # if letter is guessed incorrectly
                chances -= 1
                past_guesses += guess
                await chance_counter.edit(content=f"{chances} chances remaining.")
            # Print the word
            word_to_print = ""
            for char in word:
                if char in letter_guessed and (
                    Counter(letter_guessed) != Counter(word)
                ):
                    word_to_print += char
                    correct += 1
                # If user has guessed all the letters
                elif Counter(letter_guessed) == Counter(
                    word
                ):  # Once the correct word is guessed fully,
                    # the game ends, even if chances remain
                    await chance_counter.edit(
                        content="Congratulations, you won!\n" + hangman_words[word]
                    )
                    await the_word.edit(content=" ".join(list(word)))
                    flag = True
                    break
                else:
                    word_to_print += "_"
            await the_word.edit(
                content=" ".join(list(word_to_print)).replace("_", "\_")
            )

        # If user has used all of his chances
        if chances <= 0 and (Counter(letter_guessed) != Counter(word)):
            await chance_counter.edit(content=f'You lost!\nThe word was "{word}".')

    @magic_8_ball.error
    @roll_dice.error
    @flip_coins.error
    @draw_cards.error
    @bubblewrap.error
    @hangman.error
    async def error(self, ctx, error):
        if (
            str(error)
            == """Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
In content: Must be 2000 or fewer in length."""
        ):
            await ctx.send(
                "Sorry, you specified numbers that were too large. Sending all that would put me over the 2000-character limit!"
            )
        elif (
            str(error)
            == "Command raised an exception: HTTPException: 400 Bad Request (error code: 50006): Cannot send an empty message"
        ):
            pass
        else:
            await ctx.send(
                f"Unhandled error occurred:\n```{error}```\nIf my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!"
            )


def setup(client):
    client.add_cog(Games(client))
