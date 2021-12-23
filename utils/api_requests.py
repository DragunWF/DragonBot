import discord
import requests
import json
import praw
import random
import config  # import os

reddit = praw.Reddit(client_id=config.praw_id, client_secret=config.praw_secret,
                     username=config.praw_username, password=config.praw_password, user_agent="DragonBot")
# reddit = praw.Reddit(client_id=os.environ['RedID'], client_secret=os.environ['RedSecret'],
#                      username=os.environ['RedName'], password=os.environ['RedPass'], user_agent="DragonBot")


def get_quote():
    response = requests.get("http://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    return f'''*"{json_data[0]['q']}"* - {json_data[0]['a']}'''


def view_nft_values(type=""):
    try:
        btc_url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={type}"
        pvu_url = f"https://api.coingecko.com/api/v3/simple/price?ids=plant-vs-undead-token&vs_currencies={type}"
        bnb_url = f"https://api.coingecko.com/api/v3/simple/price?ids=binancecoin&vs_currencies={type}"
        slp_url = f"https://api.coingecko.com/api/v3/simple/price?ids=smooth-love-potion&vs_currencies={type}"
        btc_value = requests.get(btc_url, headers={
            'accept': 'application/json'}).json()["bitcoin"][f"{type}"]
        pvu_value = requests.get(
            pvu_url, headers={'accept': 'application/json'}).json()["plant-vs-undead-token"][f"{type}"]
        bnb_value = requests.get(
            bnb_url, headers={'accept': 'application/json'}).json()["binancecoin"][f"{type}"]
        slp_value = requests.get(slp_url, headers={
            'accept': 'application/json'}).json()["smooth-love-potion"][f"{type}"]
        currency = type.upper()
        return f"""
**Cryptocurrency Token Values:** :moneybag:
BitCoin (BTC): `{btc_value} {currency}`
BinanceCoin (BNB): `{bnb_value} {currency}`
PlantsVsUndead Token (PVU): `{pvu_value} {currency}`
Smooth Love Potion (SLP): `{slp_value} {currency}`"""
    except KeyError:
        return "You either sent an unsupported currency or you sent some random jibberish"


def get_meme(type=""):
    if type == "memes":
        subs = ("shitposting", "comedyheaven", "ChoosingBeggars")
    elif type == "coder":
        subs = ("ProgrammerHumor", "programmingmemes")
    elif type == "homicide":
        subs = ("comedyhomicide", "ComedyCemetery")
    elif type == "linux":
        subs = ("unixporn", "unixporn")
    subreddit = reddit.subreddit(random.choice(subs))
    all_subs = []
    hot = subreddit.hot(limit=60)
    for submission in hot:
        all_subs.append(submission)
    random_post = random.choice(all_subs)
    name, url = random_post.title, random_post.url
    embed = discord.Embed(title=name)
    embed.set_image(url=url)
    return embed


def get_copypasta():
    subreddit = reddit.subreddit("copypasta")
    all_subs = []
    hot = subreddit.hot(limit=70)
    for submission in hot:
        all_subs.append(submission)
    random_post = random.choice(all_subs)
    name, url, content = random_post.title, random_post.url, random_post.selftext
    embed = discord.Embed(title=name, url=url, description=content)
    return embed
