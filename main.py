import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import asyncio
from random import randint
import pokedex
import secrets

pokebot = commands.Bot(command_prefix="/")

regions = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola"]

whos_that = "pokemon"

points = 50

@pokebot.command()
async def who():
	index = randint(1, 151)
	pokemon = pokedex.pokelist[index]
	global whos_that 
	whos_that = pokemon
	print("Pokemon : {}".format(pokemon), "\n\nWho's that Pokemon? --> {}".format(whos_that))
	entry = pokedex.entries[pokemon]
	hint = entry
	await pokebot.say(hint)

	while points > 1:
		asyncio.sleep()

@pokebot.command()
async def its(answer):
	correct = "{} is correct!".format(answer)
	incorrect = "{} is not the pokemon we're looking for.".format(answer)

	print(whos_that.lower())

	if answer.lower() == whos_that.lower():
		await pokebot.say(correct)
	elif whos_that == "Nidoran F" or "Nidoran M":
		if answer.lower() == "nidoran":
			await pokebot.say(correct)
		else:
			await pokebot.say(incorrect)
	else:
		await pokebot.say(incorrect)

@pokebot.command()
async def tell():
	await pokebot.say("It is... {}!".format(whos_that))

@pokebot.command()
async def get(index):
	index = int(index)
	pokemon = pokedex.pokelist[index]
	entry = pokedex.entries[pokemon]
	await pokebot.say("{} : \n{}".format(pokemon, entry))

pokebot.run(secrets.bot_token)