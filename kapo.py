from discord.ext import commands
import discord
import random
import requests
from bs4 import BeautifulSoup
import re
import os
from googleapiclient.discovery import build
import unicodedata,string

client = discord.Client(max_messages=10000)
bot = commands.Bot(command_prefix=('?','!'))

greek = 'ςερτυθιοπασδφγηξκλζχψωβνμΕΡΤΥΘΙΟΠΑΣΔΛΚΞΦΗΓΖΧΨΜΝΒΩ'
def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.printable or x in greek).lower()

def max_number():
    req = requests.get('https://www.slang.gr/definitions')
    max_number = BeautifulSoup(req.text,'lxml').find('div', class_='page-header')
    regex = re.compile(r'\d{5}')
    res = regex.search(max_number.text)
    return int(res.group())

def formatted_slang(t):
    t[0] = '__**' + t[0].strip().capitalize() + '**__\n\n'
    t[1] =  t[1].strip() +'\n'
    t[2] = '_```' +t[2].strip() + '```_\n'
    t[3] = '_' + t[3].strip() + '_'
    return ' '.join(s for s in t)
# TODO stoixish aristera


@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready for action')



@bot.command()
async def hello(ctx):
    await ctx.send(f'hello there, {ctx.author.mention}')


@bot.command(name='slang', description='!slang or !slang random or !slang [word]', aliases=['σλανγ'])
async def slang(ctx,*args):

    x = ' '.join(x for x in args)
    if x=='random' or x=='':
        while True:
            url = 'https://www.slang.gr/definition/' + str(random.randint(1,max_number()))
            try:
                req = requests.get(url)
                slang = BeautifulSoup(req.text, 'lxml')
                titlos = slang.find('span', itemprop='headline')
                orismos = slang.find('div', class_='definition')
                example = slang.find('div', class_='example')
                paragrafoi = orismos.find_all('p')
                break
            except Exception as e:
                print(e)

        for p in paragrafoi:
            if p.text in example.text or p.find('a', class_='thumbnail'):
                paragrafoi.remove(p)
        x = [titlos.text, ' '.join(s.text for s in paragrafoi), example.text, url]
        await ctx.send(formatted_slang(x))
    else:
        url = 'https://www.slang.gr/lemmas?q=' + x
        req = requests.get(url)
        lemmas = BeautifulSoup(req.text, 'lxml')
        links = lemmas.find_all('a', class_='list-group-item')



        for link in links:

            if remove_accents(link.text.strip(string.digits).strip()) == remove_accents(x) or remove_accents(x) in remove_accents(link.text.strip(string.digits).strip()) :
                try:
                    new_url = 'https://www.slang.gr' + link.get('href')
                    req = requests.get(new_url)
                    slang = BeautifulSoup(req.text, 'lxml')
                    titlos = slang.find('span', itemprop='headline')
                    orismos = slang.find('div', class_='definition')
                    example = slang.find('div', class_='example')
                    paragrafoi = orismos.find_all('p')
                    for p in paragrafoi:
                        if p.text in example.text or p.find('a', class_='thumbnail'):
                            paragrafoi.remove(p)
                    re = [titlos.text, ' '.join(s.text for s in paragrafoi), example.text, new_url]
                    await ctx.send(formatted_slang(re))
                    break
                except Exception as e:
                    print(e)
                    pass



@bot.command(name='roll', description='rolls 1-100')
async def roll(ctx):
    x = random.randint(1,100)
    if x == 0:
        await ctx.send(f':zero:)/100 ')
    elif x == 100:
        await ctx.send(f':100:/:100:')
    else:
        await ctx.send(f'{x}/100')



@bot.command(name='yt', descriptpion='first youtube result',
             aliases = ['youtube'], pass_context = True)
async def youtube(ctx,*args):
    x = ' '.join(x for x in args)
    youtube = build('youtube', 'v3', developerKey=api_key)
    req = youtube.search().list(order='relevance', q=x, part='snippet')
    res = req.execute()
    await ctx.send('https://www.youtube.com/watch?v='+ res['items'][0]['id']['videoId'])





@bot.command(name='8ball', description = 'Answers a yes/no question',
             brief = ' Answers from the beyond.',
             aliases = ['eight_ball', 'eightball', '8-ball', '8mpalo'],
             pass_context = True)
async def eight_ball(ctx,*args):
    possible_responses = [ 'nai', 'oxi', 'ante gamisou', 'skase', 'mporei']

    if args[-1].endswith('?') or args[-1].endswith(';'):
        await ctx.send(random.choice(possible_responses) + ' ' + ctx.message.author.mention)
    else:
        await ctx.send('rwta kati pousth')

#@bot.command(name='flip', description='flips a coin')
#async def flip(ctx):
#    result = ['<:tails:515707401291300864>', '<:heads:515707373596442624>']
#    await ctx.send(random.choice(result))

@bot.command(name='eqtelestis', aliases=['εκτελεστης', 'τετελην', 'τετελιν', 'τετ', 'ektelestis', 'tetelin', 'tete', 'tet'])
async def eqtelestis(ctx):
    await ctx.send('MOUNOPANO')

TOKEN = os.environ['token']
api_key = os.environ['googleapi']

bot.run(TOKEN)
