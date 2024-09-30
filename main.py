#Import packages
import discord
from discord import app_commands
from discord.ui import Button, View
from datetime import datetime
from shoe_scrape import ShoeData


# Discord Bot code begins
BOT_TOKEN = 'Your Discord Bot Token Goes Here'

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


# Buttons for iteration through pages of Shoes
class ShoeView(View):
    def __init__(self, pages:list):
        super().__init__(timeout=None)
        self.pages = pages
        self.currentPage = 0
    @discord.ui.button(label='|<', style=discord.ButtonStyle.primary)
    async def first(self, interaction:discord.Interaction, button:Button):
            self.currentPage = 1
            await interaction.response.edit_message(embed=self.pages[self.currentPage])
    @discord.ui.button(label='<', style=discord.ButtonStyle.primary)
    async def previous(self, interaction:discord.Interaction, button:Button):
        if self.currentPage == 0:
            self.currentPage = len(self.pages)-1
            await interaction.response.edit_message(embed=self.pages[self.currentPage])
        else:
            self.currentPage-= 1
            await interaction.response.edit_message(embed=self.pages[self.currentPage])
    @discord.ui.button(label='>', style=discord.ButtonStyle.primary)
    async def next(self, interaction:discord.Interaction, button:Button):
        if self.currentPage == len(self.pages)-1:
            self.currentPage = 0
            await interaction.response.edit_message(embed=self.pages[self.currentPage])
        else:
            self.currentPage += 1
            await interaction.response.edit_message(embed=self.pages[self.currentPage])
    @discord.ui.button(label='>|', style=discord.ButtonStyle.primary)
    async def last(self, interaction:discord.Interaction, button:Button):
            self.currentPage = len(self.pages)-1
            await interaction.response.edit_message(embed=self.pages[self.currentPage])


         




@bot.event
async def on_ready():
    tree.clear_commands(guild=discord.Object(id=1205979767128596540))
    await tree.sync(guild=discord.Object(id=1205979767128596540))
    print('Bot is Ready')


@tree.command(name='nikeupdate', description='Gives Nike SNKRS Update')
async def nikeupdate(interaction: discord.Interaction):
    shoesNike = []
    ShoeData.nikeData(shoesNike)
    embeds = [discord.Embed(title=datetime.now().strftime('%B %d, %Y'), description = 'Nike Drops Update').set_image(url='https://highxtar.com/wp-content/uploads/2023/12/thumb-nike-snkrs-2023-top-5-1440x1080.jpg')]
    for shoe in shoesNike: 
        embed = discord.Embed(title=shoe.style, url='https://www.nike.com/launch/t/'+shoe.link)
        embed.set_image(url=shoe.image)
        embed.add_field(name='Release Date:', value='`'+shoe.time+'`', inline=False)
        embed.add_field(name='Price:', value='`$'+str(shoe.price)+'`', inline=False)
        embed.add_field(name='Size Availability Levels', value='', inline=False)
        if len(shoe.sizes) <= 22:
            for size in shoe.sizes:
                    embed.add_field(name='', value=f'`[{size.size}: {size.avail}]`', inline=True)
        elif len(shoe.sizes) > 22:
            N = len(shoe.sizes)-21
            badSizes = ''
            for size in shoe.sizes[-N:]:
                badSizes += f' `[{size.size}: {size.avail}]` '
            N = len(shoe.sizes)-N
            for size in shoe.sizes[:N]:
                embed.add_field(name='', value=f'`[{size.size}: {size.avail}]`', inline=True)     
            embed.add_field(name='', value=badSizes, inline=True)     
        embeds.append(embed)
    view = ShoeView(embeds)
    await interaction.response.send_message(embed=embeds[0], view=view, ephemeral=True)


#Run client
bot.run(BOT_TOKEN)