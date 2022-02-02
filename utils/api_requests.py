import discord
import requests
import json
import praw
import random
import utils.config as config  # import os

previous_urls = {"memes": None, "coder": None,
                 "homicide": None, "linux": None, "copypasta": None}
reddit = praw.Reddit(client_id=config.praw_id, client_secret=config.praw_secret,
                     username=config.praw_username, password=config.praw_password, user_agent="DragonBot")
# reddit = praw.Reddit(client_id=os.environ['RedID'], client_secret=os.environ['RedSecret'],
#                      username=os.environ['RedName'], password=os.environ['RedPass'], user_agent="DragonBot")


def get_quote():
    response = requests.get("http://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    return f'''*"{json_data[0]['q']}"* - {json_data[0]['a']}'''


def view_nft_values(currency_type=""):
    try:
        btc_url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency_type}"
        pvu_url = f"https://api.coingecko.com/api/v3/simple/price?ids=plant-vs-undead-token&vs_currencies={currency_type}"
        bnb_url = f"https://api.coingecko.com/api/v3/simple/price?ids=binancecoin&vs_currencies={currency_type}"
        slp_url = f"https://api.coingecko.com/api/v3/simple/price?ids=smooth-love-potion&vs_currencies={currency_type}"
        bomb_url = f"https://api.coingecko.com/api/v3/simple/price?ids=bomber-coin&vs_currencies={currency_type}"

        btc_value = requests.get(btc_url, headers={
            'accept': 'application/json'}).json()["bitcoin"][f"{currency_type}"]
        pvu_value = requests.get(
            pvu_url, headers={'accept': 'application/json'}).json()["plant-vs-undead-token"][f"{currency_type}"]
        bnb_value = requests.get(
            bnb_url, headers={'accept': 'application/json'}).json()["binancecoin"][f"{currency_type}"]
        slp_value = requests.get(slp_url, headers={
            'accept': 'application/json'}).json()["smooth-love-potion"][f"{currency_type}"]
        bomb_value = requests.get(bomb_url, headers={
                                  'accept': 'application/json'}).json()["bomber-coin"][f"{currency_type}"]

        currency = currency_type.upper()
        return f"""
>>> **Cryptocurrency Token Values:** :moneybag:
BitCoin (BTC): `{'{:,}'.format(btc_value)} {currency}`
BinanceCoin (BNB): `{'{:,}'.format(bnb_value)} {currency}`
PlantsVsUndead Token (PVU): `{'{:,}'.format(pvu_value)} {currency}`
Smooth Love Potion (SLP): `{'{:,}'.format(slp_value)} {currency}`
Bomber Coin (BCOIN): `{'{:,}'.format(bomb_value)} {currency}`"""
    except KeyError:
        responses = ("That's an... Invalid input", "Well that's an invalid input",
                     "You need to enter a valid currency", "Invalid input")
        if len(currency_type) > 3:
            return random.choice(responses)
        return "Unsupported Currency"


def get_meme(genre=""):
    genres = {"memes": ("shitposting", "comedyheaven", "ChoosingBeggars"),
              "coder": ("ProgrammerHumor", "programmingmemes"),
              "homicide": ("comedyhomicide", "ComedyCemetery"),
              "linux": ("unixporn", "unixporn")}

    subreddit = reddit.subreddit(random.choice(genres[genre]))
    all_subs = []
    hot = subreddit.hot(limit=60)

    for submission in hot:
        all_subs.append(submission)

    while True:
        random_post = random.choice(all_subs)
        url = random_post.url
        if url != previous_urls[genre]:
            break

    name = random_post.title
    embed = discord.Embed(title=name)
    embed.set_image(url=url)

    previous_urls[genre] = url
    return embed


def get_copypasta():
    subreddit = reddit.subreddit("copypasta")
    all_subs = []
    hot = subreddit.hot(limit=70)

    for submission in hot:
        all_subs.append(submission)

    while True:
        random_post = random.choice(all_subs)
        url = random_post.url
        if url != previous_urls["copypasta"]:
            break

    name = random_post.title
    content = random_post.selftext

    embed = discord.Embed(title=name, url=url, description=content)
    previous_urls["copypasta"] = url
    return embed
