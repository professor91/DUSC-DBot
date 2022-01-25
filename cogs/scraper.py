# web scraper modules
import requests
import bs4

# database modules
import json

# discord modules
import discord
from discord.ext import commands
from discord.ext import tasks

# other modules
import os
from datetime import datetime

import time

# class for handeling Database 
class jsdb:
    #0. constructor
    def __init__(self):
        self._cacheddata= {}
        self.reload()
    
    #1. dump data in json file
    def dumpdata(self):
        with open("cogs/_cache/news_cache.json", "w") as wf:
            json.dump(self._cacheddata, wf, indent=6)
            print("log: Wrote data in json file")
        self.reload()

    #2. reload data from json file
    def reload(self):
        with open("cogs/_cache/news_cache.json", "r") as rf:
            self._cacheddata= json.load(rf)
            print("log: Reloaded the database into dictionary")

    #3. add new item to database
    def additem(self, key, val):
        self._cacheddata[key]= val
        print("Added new item to the dictionary", "\nkey: ", key, " val: ", val)
        self.dumpdata()


# class for handeling Web Scraper
class duscraper():
    #0. constructor
    def __init__(self):
        # fetching html page
        getPage = requests.get('http://www.du.ac.in/')
        getPage.raise_for_status() #if error it will stop the program
        # Parse text for news
        self._soup = bs4.BeautifulSoup(getPage.text, 'html.parser')
        # Fetching data from soup
        self._spotlight_box_div= self._soup.find_all('div', attrs={'id':'pills-spotlight'})[0]
        self._spotlight_news_li= self._spotlight_box_div.find_all('li', attrs={'class':'ma_news'})
        # for storing fetched data
        self._day_month_year= ""
        # database handler class object
        self._jsdb_class= jsdb()

    #1. load news from website
    def load_news(self):
        for news in self._spotlight_news_li[::-1]:
            self.addnew_news(news, news.find_all('a')[0]['title'])

        print("log: Fetched news from the website")

    #2. add new news to the database
    def addnew_news(self, news_li, news_title):
        self._day_month_year += str(news_li.find('span', attrs={'class':'day'}).text) + "-"
        self._day_month_year += str(news_li.find('span', attrs={'class':'month'}).text) + "-"
        self._day_month_year += str(datetime.now().date().strftime("%Y"))
        
        # adding item to the database
        self._jsdb_class.additem(self._day_month_year, news_title)
        self._day_month_year= ""

    #3. check for update
    def checkupdate(self):
        keys= list(self._jsdb_class._cacheddata.keys())
        temp_li= self._spotlight_box_div.find_all('li', attrs={'class':'ma_news'})[0]
        temp_title= temp_li.find_all('a')[0]['title']

        # check if the the top notif on website is in the database
        if temp_title == self._jsdb_class._cacheddata[keys[len(keys)-1]]:
            print('no latest update against', keys[len(keys)-1], " @ ", datetime.now())
            return [False]
        else:
            self.addnew_news(temp_li, temp_title)
            return [True, temp_li, temp_title]


class scraper(commands.Cog):
    #0. constructor
    def __init__(self, client):
        self.client= client
        # objects of scraper and jsdb class
        self._duscraper_class= duscraper()
        self._jsdb_class= jsdb()
        # discord text channel to send news
        if self._jsdb_class._cacheddata['newschannelId'] == 0:
            print('channel id not found')
        else:
            self._channel = client.get_channel(
                self._jsdb_class._cacheddata['newschannelId'])

    @commands.Cog.listener()
    async def on_ready(self):
        # starting loop to check for new update every 24 hours
        # self.checkup.start()
        await self.checkup()

    #1. command for loading news from website
    @commands.command()
    async def loadnews(self, ctx):
        self._duscraper_class.load_news()
        await ctx.message.reply("Fetched news from website")

    #2. set text channel for sending updates
    @commands.command()
    async def setch(self, ctx, channel : discord.TextChannel):
        self._channel= channel.id
        await ctx.message.reply(f"New updates now will be sent in <#{self._channel}>")

    #3. dump database on discord
    @commands.command()
    async def dumpdb(self, ctx):
        # db_dump= ""
        # for key in self._jsdb_class._cacheddata.keys():
        #     db_dump += str(key) + str(self._jsdb_class._cacheddata[key]) + "\n"

        await ctx.message.reply(
            f"{ctx.author.mention}Database dump, coming right up\n", 
            self._jsdb_class._cacheddata
        )

    #2. function to check for update
    # @tasks.loop(hours=12)
    async def checkup(self):
        new_update= self._duscraper_class.checkupdate()
        if new_update[0]:
            temp= new_update[0]
            dateandtime = str()
            # fetch date of announcement
            dateandtime += str(new_update[1].find('span', attrs={'class':'day'}).text) + "-"
            dateandtime += str(new_update[1].find('span', attrs={'class':'month'}).text) + "-"
            dateandtime += str(datetime.now().date().strftime("%Y"))

            embd_desc= str(new_update[2])
            # embed initialized
            announcement_embed= discord.Embed(
                title="New announcement posted on DU Spotlight section",
                description= embd_desc,
                color=discord.Color.green()
            )
            # author
            announcement_embed.set_author(
                name="Akhbaar wale bhayia"
                # icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png"
            )
            # footer
            announcement_embed.set_footer(
                text= dateandtime
                # icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png"
                )

            # post announcement
            await self.client.get_channel(
                self._jsdb_class._cacheddata['newschannelId']).send(
                    "everyone", embed= announcement_embed)
        
        return

def setup(client):
    client.add_cog(scraper(client))