import discord
import random
import requests
from saucenao_api import SauceNao, VideoSauce, BookSauce


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
	
	# bot will parse each message and respond if the keyword "!sauce" is present
    if message.content.startswith('!sauce'):
		
        sauce = SauceNao()
        try:
            results = sauce.from_url(message.attachments[0].url)  # if the message provided has an attachment, parse it for the URL
        except:
            results = sauce.from_url(message.content[7:]) # otherwise the message itself contains a URL

        best = results[0]  # get the best result based off of similarity
        result = best.title + "\nSimilarity: " + str(best.similarity) + "%" + "\nSource URL: " + str(best.urls) # get the numeric percentage of similarity and original source URL
		
		# additionally, if the source is from a video clip, add in the episode it is from and the time
        if isinstance(best, VideoSauce):
            result = result + "\nEpisode: " + str(best.part) + "\nTime: " + best.est_time
        await message.channel.send(result)
        
    
    elif message.content.startswith('!courses'):
        url_planet = "https://api.planetterp.com/v1/courses?department=" + message.content[9:13]
        courses = requests.get(url_planet).json()
        output = ""
        for j in courses:
            output = output + ", " + message.content[9:13] + j['course_number']
        await message.channel.send(output)
    
    
    



