import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import asyncio
from random import randint
import pokedex
import secrets

pokebot = commands.Bot(command_prefix="/")
instances = {}

class Instance(object):
	"""docstring for Instance"""
	def __init__(self, server):
		super(Instance, self).__init__()
		self.server = server
		self.id = server.id
		self.name = server.name
		self.regions = []
		self.pokelist = ["Pokemon :"]
		self.whos_that = "pokemon"
		self.points = 60

	def addRegion(self, regionName):
		region = pokedex.regions[regionName]
		if region not in self.regions:
			self.regions.append(region)
			for pokemon in region:
				self.pokelist.append(pokemon)
			return True
		else:
			return False

	def resetPokelist(self):
		for region in self.regions:
			for pokemon in region:
				self.pokelist.append(pokemon)

def getInstance(ctx):
	server = ctx.message.server
	instance = Instances[server.id]
	return instance

async def startTimer():
	global points

	while points > 1:
		asyncio.sleep(1)
		points += -1

	await pokebot.say('Uh oh! All out of time!')
	tell()

@pokebot.command(pass_context=True)
async def add(ctx, regionName):
	instance = getInstance(ctx)
	regionName = regionName.lower()
	added = instance.addRegion(regionName)
	if added:
		await pokebot.say("The {} region was added.".format(regionName))
	else:
		await pokebot.say("The {} region is already present in the list of Pokemon.".format(regionName))

@pokebot.command(pass_context=True)
async def get(ctx, index):
	instance = getInstance(ctx)
	index = int(index)
	pokemon = instance.pokelist[index]
	entry = pokedex.entries[pokemon]
	await pokebot.say("{} : \n{}".format(pokemon, entry))

@pokebot.command(pass_context=True)
async def init(ctx):
	server = ctx.message.server
	instance = Instance(server)
	instances[server.id] = instance

@pokebot.command(pass_context=True)
async def its(ctx, *userInput):
	instance = getInstance(ctx)
	whos_that = instance.whos_that
	answer = ''
	for part in userInput:
		answer += part

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
	elif whos_that == "Mr. Mime":
		if answer.lower() == "mr.mime":
			await pokebot.say(correct)
		else:
			await pokebot.say(incorrect)
	else:
		await pokebot.say(incorrect)

@pokebot.command(pass_context=True)
async def tell(ctx):
	instance = getInstance(ctx)
	await pokebot.say("It is... {}!".format(instance.whos_that))

@pokebot.command(pass_context=True)
async def who(ctx):
	instance = getInstance(ctx)
	pokelist = instance.pokelist

	remaining = len(pokelist)
	if remaining < 2:
		instance.resetPokelist()

	index = randint(1, len(pokelist) - 1)
	pokemon = pokelist[index]
	instance.whos_that = pokemon
	print("Pokemon : {}".format(pokemon), "\n\nWho's that Pokemon? --> {}".format(instance.whos_that))
	entry = pokedex.entries[pokemon]
	hint = entry
	await pokebot.say(hint)

	pokelist.remove(pokemon)

pokebot.run(secrets.bot_token)