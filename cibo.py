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

    if message.content.startswith('!hello'):
        await message.channel.send('Hello, ' + str(message.author))
        print(message.content.split()[1:])
        print(type(message.content))

    if message.content.startswith('!tweets'):
        print('Got tweet command.')
        try:
            userpage = str(message.content.split()[1])
            amount = int(message.content.split()[2])
            twpage = requests.get('https://twitter.com/' + userpage) ##Get the userpage content
            twpage.raise_for_status()
            soup = bs4.BeautifulSoup(twpage.text, 'html.parser')
            alltweets = soup.findAll('p', {'class': 'js-tweet-text'})
            for i in range(amount):
                link = re.search('https://twitter.com/\S+', str(alltweets[i].get_text())) ## Checking if it the tweet is a reply
                if link is None: ## if it is not
                    await message.channel.send("Tweet " + str(i+1) + "\):\n" + str(alltweets[i].get_text()))
                else:
                    msgs = [] ##If it is, separate the tweet in two parts, text and link
                    linkpart = re.search('https://twitter.com/\S+', str(alltweets[i].get_text())).group()
                    textpart = re.sub(linkpart, "", alltweets[i].get_text())
                    await message.channel.send("Tweet " + str(i+1) + "\):\n" + textpart)
                    await message.channel.send(linkpart)
        except:
            await message.channel.send("Something went wrong.\nExample input: !tweets elonmusk 4")


@client.event
async def on_ready():
    print('\nLogged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
