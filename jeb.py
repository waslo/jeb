from discord.ext import commands
import random
import json, requests
import praw
import re
from bs4 import BeautifulSoup
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

messages_of_incredulity = [
    "what the hell is a '%s'?",
    "i have never heard of '%s'",
    "wot in tarnation is a '%s'?",
    "who is this hacker '%s'?",
    "i didn't thnks '%s' be like it is, but it do, my sources say",
    "what dost thou signifie with the phrase '%s'?",
    "i think i ate a '%s' once in thailand",
    "who is '%s'? she sounds expensive"
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

wolfram_appid = ""
with open('wolfram.txt', 'r') as myfile:
     wolfram_appid = myfile.read()

reddit = praw.Reddit(client_id='ME1edWqMxu_67A', client_secret="XbP_JLO_wa4bOxMAw6dxSIlcdfY", user_agent='jeb-discord')

################################################################################################################

# Helper functions

# Gets a random element from an iterable
def iter_sample_fast(iterable, samplesize):
    results = []
    iterator = iter(iterable)
    # Fill in the first samplesize elements:
    try:
        for _ in range(samplesize):
            results.append(iterator.next())
    except StopIteration:
        raise ValueError("Sample larger than population.")
    random.shuffle(results)  # Randomize their positions
    for i, v in enumerate(iterator, samplesize):
        r = random.randint(0, i)
        if r < samplesize:
            results[r] = v  # at a decreasing rate, replace random items
    return results

# Returns "i" if passed "you"
def i4u(x):
    if x == "you":
        return "i"

    return x

# Helper for clap command
def process_clap_args(strs):
    if len(strs) > 0 and strs[0] == "for":
        strs = strs[1:]

    strs = list(map(i4u, strs))
    return strs

def unique(args, ticker):
    for stock in args:
        if stock == ticker:
            return False
    return True

# Given a query, extracts the grammatical object of that query
def extractObj(q):
    obj = re.split("are|is|a|an", q.strip())[-1]
    if obj[-1] == "?":
        obj = obj[:-1]
    return obj.strip()

# Helper for Wolfram related queries
async def handleWolfram(q):
    url = 'http://api.wolframalpha.com/v2/query'
    payload = {'input': q, 'appid': wolfram_appid, 'output': 'json', 'format': 'plaintext'}
    resp = requests.get(url=url, params=payload)
    data = json.loads(resp.text)
    
    if data["queryresult"]["numpods"] == 0:
        obj = extractObj(q) 
        await bot.say(random.choice(messages_of_incredulity) % obj)
    else:
        result = ""
        backup = ""
        for pod in data["queryresult"]["pods"][:10]:
            if pod["error"]:
                continue
            for subpod in pod["subpods"]:
                backup += subpod["plaintext"] + "\n\n"
                if "img" in subpod:
                    backup += subpod["img"]["src"] + "\n\n"
            if "primary" in pod and pod["primary"]:
                for subpod in pod["subpods"]:
                    result += subpod["plaintext"] + "\n\n"
                    if "img" in subpod:
                        result += subpod["img"]["src"] + "\n\n"

                await bot.say(result)
                return
        await bot.say(backup)

stocks = dict.fromkeys(["colin", "tao", "wes", "adib"])
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
        diff = data["USD"] - state["last_eth"]
        reply += ", a difference of " + ("+" if diff > 0 else "") + ('%.2f' % diff) + " since I last checked"

    state["last_eth"] = data["USD"]
    await bot.say(reply)

@bot.command()
async def what(*args):
    await bot.type()
    if len(args) == 0:
        args = ["is jeb bush's birthday"]
    q = "what " + " ".join(args)
    await handleWolfram(q)

@bot.command(name="what?")
async def what2(*args):
    await bot.type()
    if len(args) == 0:
        args = ["is jeb bush's birthday"]
    q = "what " + " ".join(args)
    await handleWolfram(q)

@bot.command()
async def who(*args):
    await bot.type()
    if len(args) == 0:
        args = ["is jeb bush?"]
    q = "who " + " ".join(args)
    await handleWolfram(q)

@bot.command(name="who?")
async def who2(*args):
    await bot.type()
    if len(args) == 0:
        args = ["is jeb bush?"]
    q = "who " + " ".join(args)
    await handleWolfram(q)

@bot.command()
async def show(*args):
    if len(args) == 0:
        args = ["corgi"]
    subreddit = args[0]
    time_filter = 'day'
    if subreddit == "more":
        if len(args) == 1:
            args = ["more", "corgi"]
        subreddit = args[1]
        time_filter = 'week'
    sr = reddit.subreddit(subreddit)
    iterable = sr.top(time_filter=time_filter, limit=50)
    try:
        post = iter_sample_fast(iterable, 1)[0]
        if post.is_self:
            await bot.say(post.title + "\n\n\n" + post.selftext)
        else:
            await bot.say(post.url)
    except:
        await bot.say(random.choice(messages_of_incredulity) % subreddit)

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
        if len(data["data"]) > 0:
            await bot.say(random.choice(data["data"])["embed_url"])
        else:
            await bot.say(random.choice(messages_of_incredulity) % query)

@bot.command(name='+stock')
async def add_ticker(*args):
    args = " ".join(process_clap_args(args))
    args = args.split(' ')
    if len(args)<2:
        await bot.say("Your input is off. FORMAT: [jeb, +stock name Ticker1 Ticker2 Ticker3 ...]")
        return
    if (args[0] in stocks) and (not stocks[args[0]] is None):
         for ticker in stocks[args[0]]:
             if unique(args, ticker):
              args.append(ticker)
         stocks[args[0]] = args[1:len(args)]
    else:
        stocks[args[0]] = args[1:len(args)]
    await bot.say("Adding " + str(stocks[args[0]]) + " for " + args[0])

@bot.command(name='?stock')
async def search_ticker(*args):
    args = " ".join(process_clap_args(args))
    if stocks[args] is None:
        await bot.say('Create some stocks before you try to price them dog')
    else:
        requestedStocks = dict.fromkeys(stocks[args])
        for ticker in stocks[args]:
            url = 'https://ca.finance.yahoo.com/quote/'+ticker+'?p=' +ticker
            resp = requests.get(url=url)
            soup = BeautifulSoup(resp.content, "html.parser")
            prices = soup.find_all("span", "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
            requestedStocks[ticker] = prices[0].findAll(text=True)
        await bot.say(requestedStocks)

@bot.command(name='-stock')
async def remove_ticker(*args):
    args = " ".join(process_clap_args(args))
    args = args.split(" ")
    if len(args) < 2:
        await bot.say("Your input is off. FORMAT: [jeb, -stock name TickerToRemove]")
        return
    if stocks[args[0]] is None:
        await bot.say('Who r u, where am I')
    else:
        if not unique(stocks[args[0]], args[1]):
         stocks[args[0]].remove(args[1])
         await bot.say(args[1] + ' was removed ' +args[0]+ ' , sorry for your losses, next time you should buy low and sell high')
        else:
         await bot.say("You arent subscribed to that stock")

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