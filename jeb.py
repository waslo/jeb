from discord.ext import commands
import random
import json, requests
#Testing webhook7
description = 'John Ellis "Jeb" Bush Sr. is an American businessman and politician who served as the 43rd Governor of Florida from 1999 to 2007.'
bot = commands.Bot(command_prefix='jeb, ', description=description)

messages_of_resilience = ["fuck u bitch u dont know me", "i've got real ones past kennedy road so sit bro", "my brother was once president; he'll get u for that", "you're on a list", "i did benghazi and i'll do ur mom"]
secret = "blank"
with open('secret.txt', 'r') as myfile:
    secret=myfile.read()

def i4u(x):
    if x == "you":
        return "i"

    return x

def process_clap_args(strs):
    if len(strs) > 0 and strs[0] == "for":
        strs = strs[1:]

    strs = list(map(i4u, strs))
    return strs

@bot.event
async def on_ready():
    print('Logged in!!')

state = {"last_eth": -1}

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
async def please(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is not _clap:
        await bot.say(random.choice(messages_of_resilience))

@please.command(name='clap')
async def _clap(*args):
    args = " ".join(process_clap_args(args))
    print(args)
    await bot.say('👏 ' + args + ' 👏 ' + args + ' 👏 ' + args + ' 👏 ' + args + ' 👏 ')

bot.run(secret)
