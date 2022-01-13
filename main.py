import os
import discord
import nltk
import re
from discord import Embed
from discord.ext import commands
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from urllib.request import urlopen
from bs4 import BeautifulSoup
from keep_alive import keep_alive

client = discord.Client()
client = commands.Bot(command_prefix='!', help_command=None)

nltk.download('stopwords')
nltk.download('punkt')
stopwords = set(stopwords.words("english"))

def summarizer(text):
    words = word_tokenize(text)
    freqTable = dict()

    for word in words:
        word in word.lower()
        if word in stopwords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for (word, freq) in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue))

    summary = ''
    for sentence in sentences:
        if sentence in sentenceValue and sentenceValue[sentence] > 1.2 * average:
            if not summary:
                summary = sentence
            else:
                summary += ' ' + sentence
    return summary

def soup(url):
    source = urlopen(url).read()
    soup = BeautifulSoup(source,'html.parser')

    text = ""
    for paragraph in soup.find_all('p'):
        text += paragraph.text

    text = re.sub(r'\[[0-9]*\]', ' ',text)
    text = re.sub(r'\s+', ' ',text)

    return text

@client.event
async def on_ready():
    print('We have logged in as {0.user}'
    .format(client))

@client.group(name='help')
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Use !help <command> for instructions", color = ctx.author.color)
    em.add_field(name = "Commands",value='!summarize, !website')
    await ctx.send(embed = em)

@help.command()
async def summarize(ctx):
    em = discord.Embed(title = "Summarize", description = "Summarizes text given by user", color = ctx.author.color)
    em.add_field(name = "Syntax", value = '!summarize <text>')
    await ctx.send(embed = em)

@help.command()
async def website(ctx):
    em = discord.Embed(title = "Website", description = "Uses <p> tags to scrape then summarizes the website given by user. Designed for Wikipedia.", color = ctx.author.color)
    em.add_field(name = "Syntax", value = '!website <url>')
    await ctx.send(embed = em)

@client.command(name='summarize')
async def summarize(ctx, text):
    summary = summarizer(text)
    if len(summary) >= 2000:
        with open("summary.txt","w") as file:
            file.write(summary)
        with open("summary.txt","rb") as file:
            await ctx.send("Your summary is:", file=discord.File(file,"summary.txt"))
            return
    if not summary:
        await ctx.send("Input is too short.")
        return
    await ctx.send(summary)

@client.command(name='website')
async def website(ctx, url):
    text = soup(url)
    summary = summarizer(text)
    if len(summary) >= 2000:
        with open("summary.txt","w") as file:
            file.write(summary)
        with open("summary.txt","rb") as file:
            await ctx.send("Your summary is:", file=discord.File(file,"summary.txt"))
            os.remove("summary.txt")
            return
    if not summary:
        await ctx.send("Input is too short.")
        return
    await ctx.send(summary)

keep_alive()
client.run(os.getenv('TOKEN'))
