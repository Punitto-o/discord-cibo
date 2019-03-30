# Work with Python 3.6
import discord, requests, bs4

TOKEN = 'NTYxNTc3NzEwODEyNTI4NjQw.XJ-Tvg.idgxKToBfmeNF9lzideh81IKuFc'

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
                await message.channel.send(str(alltweets[i].get_text()))
        except:
            await message.channel.send("Something went wrong.\nExample input: !tweets elonmusk 4")


@client.event
async def on_ready():
    print('\nLogged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
