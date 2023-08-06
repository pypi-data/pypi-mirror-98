
# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import random
import secrets
import asyncio
from urllib.parse import quote as urlquote
from textwrap import dedent
# * Third Party Imports --------------------------------------------------------------------------------->
from discord.ext import commands
from discord import AllowedMentions
from pyfiglet import Figlet
import discord
# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog
# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.utility.misc import is_even, make_config_name
from antipetros_discordbot.utility.checks import command_enabled_checker, allowed_requester, allowed_channel_and_allowed_role_2
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.discord_markdown_helper.the_dragon import THE_DRAGON
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ZERO_WIDTH
from antipetros_discordbot.utility.poor_mans_abc import attribute_checker
from antipetros_discordbot.utility.enums import RequestStatus, CogState
from antipetros_discordbot.utility.replacements.command_replacement import auto_meta_info_command
# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]

# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

COG_NAME = "KlimBimCog"

CONFIG_NAME = make_config_name(COG_NAME)

get_command_enabled = command_enabled_checker(CONFIG_NAME)

# endregion[Constants]


class KlimBimCog(commands.Cog, command_attrs={'hidden': False, "name": COG_NAME}):
    """
    Collection of small commands that either don't fit anywhere else or are just for fun.
    """
    # region [ClassAttributes]
    config_name = CONFIG_NAME

    docattrs = {'show_in_readme': True,
                'is_ready': (CogState.WORKING,
                             "2021-02-06 03:32:39",
                             "05703df4faf098a7f3f5cea49c51374b3225162318b081075eb0745cc36ddea6ff11d2f4afae1ac706191e8db881e005104ddabe5ba80687ac239ede160c3178")}

    required_config_data = dedent("""
                                        coin_image_heads = https://i.postimg.cc/XY4fhCf5/antipetros-coin-head.png,
                                        coin_image_tails = https://i.postimg.cc/HsQ0B2yH/antipetros-coin-tails.png""")

    # endregion [ClassAttributes]

    # region [Init]

    def __init__(self, bot):
        self.bot = bot
        self.support = self.bot.support
        self.allowed_channels = allowed_requester(self, 'channels')
        self.allowed_roles = allowed_requester(self, 'roles')
        self.allowed_dm_ids = allowed_requester(self, 'dm_ids')
        glog.class_init_notification(log, self)

# endregion [Init]

# region [Properties]


# endregion [Properties]

# region [Setup]


    async def on_ready_setup(self):

        log.debug('setup for cog "%s" finished', str(self))

    async def update(self, typus):
        return
        log.debug('cog "%s" was updated', str(self))


# endregion [Setup]

# region [Loops]


# endregion [Loops]

# region [Listener]


# endregion [Listener]

# region [Commands]


    @ auto_meta_info_command(enabled=get_command_enabled('the_dragon'))
    @ allowed_channel_and_allowed_role_2()
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def the_dragon(self, ctx):
        """
        Posts and awesome ASCII Art Dragon!

        Example:
            @AntiPetros the_dragon

        """
        suprise_dragon_check = secrets.randbelow(100) + 1
        if suprise_dragon_check == 1:
            await ctx.send('https://i.redd.it/073kp5pr5ev11.jpg')
        elif suprise_dragon_check == 2:
            await ctx.send('https://www.sciencenewsforstudents.org/wp-content/uploads/2019/11/860-dragon-header-iStock-494839519.gif')
        else:
            await ctx.send(THE_DRAGON)

    @ auto_meta_info_command(enabled=get_command_enabled('flip_coin'))
    @allowed_channel_and_allowed_role_2()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def flip_coin(self, ctx: commands.Context):
        """
        Simulates a coin flip and posts the result as an image of a Petros Dollar.

        Example:
            @AntiPetros flip_coin

        """
        with ctx.typing():

            result = (secrets.randbelow(2) + 1)
            coin = "heads" if is_even(result) is True else 'tails'

            await asyncio.sleep(random.random() * random.randint(1, 2))

            coin_image = COGS_CONFIG.retrieve(self.config_name, f"coin_image_{coin}", typus=str)
            nato_check_num = secrets.randbelow(100) + 1
            if nato_check_num <= 1:
                coin = 'nato, you lose!'
                coin_image = "https://i.postimg.cc/cdL5Z0BH/nato-coin.png"
            embed = await self.bot.make_generic_embed(title=coin.title(), description=ZERO_WIDTH, image=coin_image, thumbnail='no_thumbnail')

            await ctx.reply(**embed, allowed_mentions=AllowedMentions.none())
            return coin

    @ auto_meta_info_command(enabled=get_command_enabled('urban_dictionary'))
    @allowed_channel_and_allowed_role_2()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def urban_dictionary(self, ctx, term: str, entries: int = 1):
        """
        Searches Urbandictionary for the search term and post the answer as embed

        Args:

            term (str): the search term
            entries (int, optional): How many UD entries for that term it should post, max is 5. Defaults to 1.

        Example:
            @AntiPetros urban_dictionary Petros 2

        """
        if entries > 5:
            await ctx.send('To many requested entries,max allowed return entries is 5')
            return

        urban_request_url = "https://api.urbandictionary.com/v0/define?term="
        full_url = urban_request_url + urlquote(term)
        async with self.bot.aio_request_session.get(full_url) as _response:
            if RequestStatus(_response.status) is RequestStatus.Ok:
                json_content = await _response.json()
                content_list = sorted(json_content.get('list'), key=lambda x: x.get('thumbs_up') + x.get('thumbs_down'), reverse=True)

                for index, item in enumerate(content_list):
                    if index <= entries - 1:
                        _embed_data = await self.bot.make_generic_embed(title=f"Definition for '{item.get('word')}'",
                                                                        description=item.get('definition').replace('[', '*').replace(']', '*'),
                                                                        fields=[self.bot.field_item(name='EXAMPLE:', value=item.get('example').replace('[', '*').replace(']', '*'), inline=False),
                                                                                self.bot.field_item(name='LINK:', value=item.get('permalink'), inline=False)],
                                                                        thumbnail="https://gamers-palace.de/wordpress/wp-content/uploads/2019/10/Urban-Dictionary-e1574592239378-820x410.jpg")
                        await ctx.send(**_embed_data)
                        await asyncio.sleep(1)

    @ auto_meta_info_command(enabled=get_command_enabled('make_figlet'))
    @ allowed_channel_and_allowed_role_2()
    @ commands.cooldown(1, 60, commands.BucketType.channel)
    async def make_figlet(self, ctx, *, text: str):
        """
        Posts an ASCII Art version of the input text.

        **Warning, your invoking message gets deleted!**

        Args:
            text (str): text you want to see as ASCII Art.

        Example:
            @AntiPetros make_figlet The text to figlet
        """
        figlet = Figlet(font='gothic', width=300)
        new_text = figlet.renderText(text.upper())

        await ctx.send(f"```fix\n{new_text}\n```")
        await ctx.message.delete()

    @auto_meta_info_command(enabled=get_command_enabled("show_user_info"))
    @allowed_channel_and_allowed_role_2(False)
    async def show_user_info(self, ctx, user: discord.Member = None):
        user = ctx.author if user is None else user
        embed_data = await self._user_info_to_embed(user)
        await ctx.reply(**embed_data, allowed_mentions=discord.AllowedMentions.none())


# endregion [Commands]

# region [DataStorage]


# endregion [DataStorage]

# region [Embeds]


# endregion [Embeds]

# region [HelperMethods]

    async def _user_info_to_embed(self, user: discord.Member):
        # seperator = '⸻⸻⸻⸻⸻'
        master_sort_table = {"id": 0, 'top_role': 4, 'roles': 5, 'premium_since': 3, 'created_at': 1, 'joined_at': 2, 'raw_status': 6, 'activity': 7, "guild_permissions": 8}
        seperator = ''
        fields = []
        for attr in sorted(self.user_info_to_show, key=master_sort_table.get):
            name = '__**' + attr.replace('_', ' ').title() + f'**__'
            value = self.user_info_transform_table.get(attr)(getattr(user, attr))
            if attr in ["joined_at", 'activity', 'top_role', "created_at", 'activity', "raw_status"]:
                in_line = True
            else:
                in_line = False
            if attr in ["created_at", "joined_at", "guild_permissions", 'premium_since', 'raw_status', 'activity']:
                sep = ''
            else:
                sep = seperator
            fields.append(self.bot.field_item(name=name, value=f"{value}\n{sep}", inline=in_line))
        fields.append(self.bot.field_item(name='On Mobile?', value='📱' if user.is_on_mobile() is True else '💻'))
        return await self.bot.make_generic_embed(title=ZERO_WIDTH,
                                                 thumbnail=user.avatar_url,
                                                 author={"name": user.display_name, 'icon_url': user.avatar_url},
                                                 fields=fields,
                                                 footer={'text': 'You want the bot to fetch more or other data? Contact Giddi!'})


# endregion [HelperMethods]

# region [SpecialMethods]


    def cog_check(self, ctx):
        return True

    async def cog_command_error(self, ctx, error):
        pass

    async def cog_before_invoke(self, ctx):
        pass

    async def cog_after_invoke(self, ctx):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.__class__.__name__})"

    def __str__(self):
        return self.__class__.__name__

    def cog_unload(self):
        log.debug("Cog '%s' UNLOADED!", str(self))

# endregion [SpecialMethods]


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(attribute_checker(KlimBimCog(bot)))
