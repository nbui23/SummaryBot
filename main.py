import os
import discord
import nltk
from discord import Embed
from discord.ext import commands
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from keep_alive import keep_alive

client = discord.Client()
client = commands.Bot(command_prefix='!', help_command=None)

nltk.download('stopwords')
nltk.download('punkt')
stopwords = set(stopwords.words("english"))

def summarizer(text):
  words = word_tokenize(text) # array of words
  freqTable = dict()

  for word in words:
    word in word.lower()
    if word in stopwords:
        continue
    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1

  sentences = sent_tokenize(text) # array of sentences
  sentenceValue = dict()

  for sentence in sentences:
    for word, freq in freqTable.items():
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
    if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
        summary += " " + sentence
  return summary

@client.event
async def on_ready():
  print('We have logged in as {0.user}'
  .format(client))

@client.command(name='help')
async def help(ctx):
  em = discord.Embed(title = "SummaryBot", description = "Summarizes text using extractive text summarization", color = ctx.author.color)
  em.add_field(name = "Syntax",value='!summarize "<text>"')
  await ctx.send(embed = em)

@client.command(name='summarize')
async def summarize(ctx, text):
  summary = summarizer(text)
  if not summary:
    await ctx.send("Input is too short.")
    return
  await ctx.send(summary)

keep_alive()
client.run(os.getenv('TOKEN'))
