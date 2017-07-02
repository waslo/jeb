from discord.ext import commands
import random
import json, requests

################################################################################################################

# Initialization

description = 'John Ellis "Jeb" Bush Sr. is an American businessman and politician who served as the 43rd Governor of Florida from 1999 to 2007.'
bot = commands.Bot(command_prefix='jeb, ', description=description)

state = {"last_eth": -1}

messages_of_resilience = [
    "fuck u bitch u dont know me", 
    "my dad is the greatest man alive; if anybody disagrees, we'll go outside", # an actual quote, apparently
    "i've got real ones past kennedy road so sit bro", 
    "my brother was once president; he'll get u for that", 
    "you're on a list", 
    "i did benghazi and i'll do ur mom",
    "this is harlem; we do walk-bys"
]

nude_photographs = [
	"https://media.giphy.com/media/l4KhVo1OrKsqgToeQ/giphy.gif",
	"http://i2.cdn.cnn.com/cnnnext/dam/assets/150312132133-jeb-bush-gallery-9-super-169.jpg",
	"http://i.huffpost.com/gen/2948872/images/o-JEB-BUSH-facebook.jpg",
	"http://a57.foxnews.com/images.foxnews.com/content/fox-news/opinion/2014/06/20/two-reasons-why-democrats-should-fear-jeb-bush-2016-presidential-bid/_jcr_content/par/featured-media/media-1.img.jpg/0/0/1422725617420.jpg?ve=1",
	"http://i.imgur.com/zhjQf4V.jpg",
	"http://static.wixstatic.com/media/717f4e_5d4fd182c2d34f4988ecf42d6c905130.jpg"
]

giphy_api_key = ""
with open('giphy.txt', 'r') as myfile:
    giphy_api_key = myfile.read()

################################################################################################################

# Helper functions

def i4u(x):
    if x == "you":
        return "i"

    return x

def process_clap_args(strs):
    if len(strs) > 0 and strs[0] == "for":
        strs = strs[1:]

    strs = list(map(i4u, strs))
    return strs

################################################################################################################

# Bot commands

@bot.event
async def on_ready():
    print('Logged in!')

@bot.command()
async def eth():
    url = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD'
    resp = requests.get(url=url)
    data = json.loads(resp.text)

    reply = "The price of ether is $" + str(data["USD"])
    if state["last_eth"] > 0:
        reply += ", a difference of " + ('%.2f' % (data["USD"] - state["last_eth"])) + " since I last checked"

    state["last_eth"] = data["USD"]
    await bot.say(reply)

@bot.group(pass_context=True)
async def send(ctx, *args):
    query = " ".join(args)
    if query == "nudes" :
        await bot.say(random.choice(nude_photographs))
    else:
        url = 'https://api.giphy.com/v1/gifs/search'
        payload = {'api_key': giphy_api_key, 'q': query}
        resp = requests.get(url=url, params=payload)
        data = json.loads(resp.text)
        await bot.say(random.choice(data["data"])["embed_url"])

@bot.group(pass_context=True)
async def please(ctx):
    if ctx.invoked_subcommand is not _clap:
        await bot.say(random.choice(messages_of_resilience))

@please.command(name='clap')
async def _clap(*args):
    args = " ".join(process_clap_args(args))
    await bot.say('👏 ' + args + ' 👏 ' + args + ' 👏 ' + args + ' 👏 ' + args + ' 👏 ' + args + ' 👏 ')

################################################################################################################

# Run bot 

with open('secret.txt', 'r') as myfile:
    bot.run(myfile.read())