from time import strftime
from discord.ext import commands
from cogs.country import data
from datetime import date
import requests, re
import discord



class covid(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print('covid succesfully loaded')
    @commands.command()
    async def covid(self, ctx,* , country=None):
        day = date.today()
        day = strftime('%b %d %Y')
        try:
            if country is None:
                    day = date.today()
                    day = strftime('%b %d %Y')
                    url = 'https://coronavirus-19-api.herokuapp.com/all'
                    stats = requests.get(url)
                    embed2 = discord.Embed(title=f'Total cases of covid worldwide as of {day}', color=0xf50000)
                    json = stats.json()
                    cases = json['cases']
                    deaths = json['deaths']
                    recovered = json['recovered']
                    embed2.add_field(name=':nauseated_face: Cases', value=f'{cases:,}')
                    embed2.add_field(name=':skull_crossbones: Deaths', value=f'{deaths:,}')
                    embed2.add_field(name=':smiley: recovered', value=f'{recovered:,}')
                    embed2.set_footer(text='stay safe against covid 19')

               
                        
                    await ctx.send(embed=embed2)
            if country is not None:
                for i in data:
                
                    if i['Slug'] == country:
                        global nation
                        print(i['ISO2'])
                        cd = (i['ISO2'])
                        nation=(i['Country'])
                    # unstable block, overriding  settings in for loop
                    if country == 'south korea':
                        country = 's. korea'
                        cd = 'KR'
                        nation = 'Republic of Korea'

                        

                    
                  
                    
            
        
                land = re.sub('\s', '%20', country)
                print(land)
                url = f'https://coronavirus-19-api.herokuapp.com/countries/{land}'
                stats = requests.get(url)
                json = stats.json()
                #json parsing
                cases = json['cases']
                deaths= json['deaths']
                total_tests = json['totalTests']
                recovered=json['recovered']
                #getting the flag of country
                
                # template for the embed message
                embed2 = discord.Embed(title=nation, description=f'as of {day}',color=0xf50000)
                embed2.set_thumbnail(url=f"https://www.countryflags.io/{cd}/flat/64.png")
                embed2.add_field(name=':nauseated_face: Cases', value=f'{cases:,}')
                embed2.add_field(name=':skull_crossbones: Deaths', value=f'{deaths:,}')
                embed2.add_field(name=':test_tube: Total tests', value=f'{total_tests:,}')
                embed2.add_field(name=':smiley: Recovered ', value=f'{recovered:,}')
                embed2.set_footer(text='stay safe against covid 19')
                await ctx.send(embed=embed2)
        except Exception as e:
            print(e)
            await ctx.send('error occured during the process.')
            


                
  




        
    
def setup(client):
    client.add_cog(covid(client))
