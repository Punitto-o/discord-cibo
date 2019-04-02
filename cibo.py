# Work with Python 3.6
import discord, requests, bs4, re

TOKEN = '' #insert bot token here

client = discord.Client()

@client.event
async def on_message(message):
    print('New message.')
    print('Message author is: ' + str(message.author))

    if message.author.bot: # we do not want the bot to reply to itself
        return

    if message.content.startswith('!hello'): ##simple hello command
        await message.channel.send('Hello, ' + str(message.author))
        print(message.content.split()[1:])

    if message.content.startswith('!tweets'):
        print('Got tweet command.')
        try:
            userpage = str(message.content.split()[1]) ##store which twitter user the bot will scrape
            amount = int(message.content.split()[2]) ##store how many tweets the bot will scrape
            twpage = requests.get('https://twitter.com/' + userpage) ## request the user profile page
            twpage.raise_for_status() ##checks if the request was ok
            soup = bs4.BeautifulSoup(twpage.text, 'html.parser') ## create the soup object w the requests object text attribute
            alltweets = soup.findAll('div', {'class': 'js-actionable-tweet'}) ## parse the proper tweet class
            for i in range(amount): ## now loop thru only the amount of tweets the user asked
                link = alltweets[i].attrs['data-permalink-path'] #store the tweet link
                await message.channel.send("Tweet " + str(i+1) + "\):\n" + "https://twitter.com" + str(link)) #send the formatted msg
        except:
            await message.channel.send("Something went wrong.\nExample input: !tweets elonmusk 4") ##error handling


@client.event
async def on_ready():
    print('\nLogged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
