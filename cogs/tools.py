#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import discord
import speedtest
import time
from asyncio import sleep
from asyncio.events import get_event_loop
from discord.ext import commands
from discord.utils import get
from concurrent.futures import ThreadPoolExecutor
from json import dumps
from os import environ
from pengaelicutils import getops, updop, list2str, unhandling, Stopwatch
from re import search
from subprocess import check_output as shell
from tinydb import TinyDB
from dotenv import load_dotenv as dotenv


class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client

    teal = 0x007F7F
    nukeconfirm = False
    testing = False
    db = TinyDB("config.json")
    name = "tools"
    name_typable = name
    description = "Various tools and info."
    description_long = description

    def UpdateTime(self, speed=False):
        global CurrentTime
        global SpeedPerformTime
        CurrentTime = time.strftime("%a/%b %d/%Y %l:%M:%S %p %Z", time.localtime())
        if speed:  # record this as the time the speedtest was done
            SpeedPerformTime = CurrentTime

    def TestSpeed(self):
        global results
        self.UpdateTime(True)
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download(threads=None)
        s.upload(threads=None)
        s.results.share()
        results = s.results.dict()
        return results

    @commands.command(
        name="os",
        help="Read what OS I'm running on!",
        aliases=["getos"],
        usage="no args",
    )
    async def showOS(self, ctx):
        def uname(item):
            return shell(f"uname -{item}", shell=True).decode()[:-1]

        async with ctx.typing():
            system = (
                shell(
                    'neofetch | grep OS | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g"',
                    shell=True,
                )
                .decode()
                .split(":")[1][1:-2]
                .split("x86")[0][:-1]
            )
            kernel = uname("r")
            os = uname("o")
        if os == "Android":
            emoji = "<:os_android:855493322591830016>"
        elif os == "GNU/Linux":
            try:
                if environ["WSL_DISTRO_NAME"]:
                    emoji = "<:os_windows:855493279797084200>"
            except KeyError:
                emoji = "<:os_linux:855493980267479080>"
        await ctx.send(
            f"<:winxp_information:869760946808180747>I'm running on {system}, kernel version {kernel}{emoji}"
        )

    @commands.command(name="test", help="Am I online? I'm not sure.", usage="no args")
    async def test(self, ctx):
        await ctx.send("Yep, I'm alive :sunglasses:")

    @commands.command(
        name="poll",
        help="Send a poll!",
        aliases=["suggest"],
        usage="'<poll name>' <poll content>",
    )
    async def poll(self, ctx, title=None, *, arg=None):
        if title == None:
            await ctx.send(
                "<:winxp_warning:869760947114348604>You didn't specify a name for the poll!"
            )
        if arg == None:
            await ctx.send(
                "<:winxp_warning:869760947114348604>You didn't specify anything to make a poll for!"
            )
        else:
            the_poll = await ctx.send(
                embed=discord.Embed(
                    color=self.teal, title=title, description=arg
                ).set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            )
            try:
                await ctx.message.delete()
            except:
                pass
            await the_poll.add_reaction("✅")
            await the_poll.add_reaction("🤷")
            await the_poll.add_reaction("❌")

    @commands.command(
        name="clear",
        help="Clear some messages away.",
        aliases=["delmsgs", "purge"],
        usage="[number of messages to delete (5)]",
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, msgcount: int = 5):
        await ctx.channel.purge(limit=msgcount + 1)
        report = await ctx.send(
            f"<:winxp_information:869760946808180747>{msgcount} (probably) messages deleted."
        )
        await sleep(3)
        try:
            await report.delete()
        except:
            pass

    @commands.command(
        name="nuke",
        help="Purge a channel of EVERYTHING.",
        aliases=["wipe", "wipechannel"],
        usage="no args",
    )
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        if not self.nukeconfirm:
            await ctx.send(
                f"<:winxp_question:869760946904645643>Are you **really** sure you want to wipe this channel? Type the command again to confirm. This will expire in 10 seconds."
            )
            self.nukeconfirm = True
            await sleep(10)
            if self.nukeconfirm:
                self.nukeconfirm = False
                await ctx.send(
                    "<:winxp_information:869760946808180747>Pending nuke expired."
                )
        elif self.nukeconfirm:
            newchannel = await ctx.channel.clone(reason=f"Nuking #{ctx.channel.name}")
            await newchannel.edit(
                position=ctx.channel.position, reason=f"Nuking #{ctx.channel.name}"
            )
            await ctx.channel.delete(reason=f"Nuked #{ctx.channel.name}")
            self.nukeconfirm = False

    @commands.command(name="mute", help="Mute a member.", usage="<member>")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.add_roles(
                get(ctx.guild.roles, id=getops(ctx.guild.id, "roles", "muteRole")),
                reason=reason,
            )
            await ctx.send(f"Muted {member} for reason `{reason}`.")
        except:
            await ctx.send(
                f"<:winxp_warning:869760947114348604>There is no set mute role. To set a mute role, type `{self.client.command_prefix}options set muteRole <mute role>`."
            )

    @commands.command(name="kick", help="Kick a member.", usage="<member>")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(
            f"<:winxp_information:869760946808180747>Kicked {member} for reason `{reason}`."
        )

    @commands.command(name="ban", help="Ban a member.", usage="<member>")
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(
            f"<:winxp_information:869760946808180747>Banned {member} for reason `{reason}`."
        )

    @commands.group(name="info", help="See a bunch of data!")
    async def info(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send(
                embed=discord.Embed(
                    title="Information",
                    description="See a bunch of data!",
                    color=self.teal,
                )
                .add_field(
                    name="emoji", value="Fetch the specified (server-specific) emoji."
                )
                .add_field(
                    name="server", value="See information about the server at a glance."
                )
                .add_field(name="user", value="Get info for the specified user.")
            )

    @info.command(
        name="emoji",
        help="Fetch the specified (server-specific) emoji.",
        aliases=["emote"],
        usage="[:emoji:]",
    )
    async def get_emoji(self, ctx, emoji=None):
        emojis = [f"<:{em.name}:{em.id}>" for em in ctx.guild.emojis if not em.animated]
        animojis = [f"<a:{em.name}:{em.id}>" for em in ctx.guild.emojis if em.animated]
        emojiurls = [
            f"https://cdn.discordapp.com/emojis/{em.id}.png"
            for em in ctx.guild.emojis
            if not em.animated
        ] + [
            f"https://cdn.discordapp.com/emojis/{em.id}.gif"
            for em in ctx.guild.emojis
            if em.animated
        ]
        if emoji == None:
            await ctx.send(
                "<:winxp_information:869760946808180747>Here's all the emojis on this server, sorted by ID."
                + "\n__Normal__\n"
                + str(emojis)[1:-1].replace("'", "").replace(", ", "")
                + "\n__Animated__\n"
                + str(animojis)[1:-1].replace("'", "").replace(", ", "")
            )
        else:
            emojis += animojis
            if emoji in emojis:
                emname = emoji.split(":")[:-1]
                if emname[0] == "<a":
                    emname = emname[1] + ".gif"
                else:
                    emname = emname[1] + ".png"
                await ctx.send(
                    embed=discord.Embed(
                        title=emname,
                        color=self.teal,
                    ).set_image(url=emojiurls[emojis.index(emoji)])
                )
            else:
                await ctx.send(
                    "<:winxp_warning:869760947114348604>Invalid emoji specified!"
                )

    @info.command(
        name="server",
        help="See information about the server at a glance.",
        usage="no args",
    )
    async def get_server_info(self, ctx):
        guild = ctx.guild
        owner = guild.owner
        if owner.nick == None:
            owner.nick = owner.name
        creation = guild.created_at
        jsoninfo = str(
            dumps(
                {
                    "basic info": {
                        "server name": guild.name,
                        "server owner": f"{owner.display_name} ({owner.name}#{owner.discriminator})",
                        "server id": guild.id,
                        "server icon": str(guild.icon_url).split("?")[0],
                        "two-factor authentication": bool(guild.mfa_level),
                        "creation date": f"{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} UTC/GMT",
                    },
                    "levels": {
                        "verification level": f"{guild.verification_level[0]} (level {guild.verification_level[1]+1})",
                        "notification level": f"{guild.default_notifications[0].replace('_',' ')} (level {guild.default_notifications[1]+1})",
                        "content filter": f"{guild.explicit_content_filter[0].replace('_',' ')} (level {guild.explicit_content_filter[1]+1})",
                    },
                    "counts": {
                        "members": guild.member_count,
                        "boosters": guild.premium_subscription_count,
                        "text channels": len(guild.text_channels),
                        "voice channels": len(guild.voice_channels),
                        "channel categories": len(guild.categories),
                        "emojis": len(guild.emojis),
                        "roles": len(guild.roles) - 1,
                    },
                },
                indent=4,
            )
        )
        embedinfo = (
            discord.Embed(title=guild.name, color=self.teal)
            .add_field(
                name="Basic Info",
                value=f"Owner: {owner.mention}\n"
                + f"ID: `{guild.id}`\n"
                + f"Two-Factor Authentication: {bool(guild.mfa_level)}\n"
                + f"Creation Date: `{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} UTC/GMT`".replace(
                    "True", "Enabled"
                ).replace(
                    "False", "Disabled"
                ),
                inline=False,
            )
            .add_field(
                name="Levels",
                value=f"Verification Level: {guild.verification_level[0]} (level {guild.verification_level[1]+1})\n"
                + f"Notification Level: {guild.default_notifications[0].replace('_',' ')} (level {guild.default_notifications[1]+1})\n"
                + f"Content Filter: {guild.explicit_content_filter[0].replace('_',' ')} (level {guild.explicit_content_filter[1]+1}",
                inline=False,
            )
            .add_field(
                name="Counts",
                value=f"Members: {guild.member_count}\n"
                + f"Boosters: {guild.premium_subscription_count}\n"
                + f"Text Channels: {len(guild.text_channels)}\n"
                + f"Voice Channels: {len(guild.voice_channels)}\n"
                + f"Channel Categories: {len(guild.categories)}\n"
                + f"Emojis: {len(guild.emojis)}\n"
                + f"Roles: {len(guild.roles)-1}",
                inline=False,
            )
            .set_thumbnail(url=guild.icon_url)
        )
        if getops(guild.id, "toggles", "jsonMenus"):
            await ctx.send(f'```json\n"server information": {jsoninfo}```')
        else:
            await ctx.send(embed=embedinfo)

    @info.command(
        name="user",
        help="Get info for the specified user.",
        aliases=["member"],
        usage="no args",
    )
    async def get_user_info(self, ctx, *, user: discord.Member = None):
        if user == None:
            user = ctx.author
        roles = user.roles[1:]
        roles.reverse()
        creation = user.created_at
        jsoninfo = str(
            dumps(
                {
                    "name": f"{user.display_name} ({user.name}#{user.discriminator})",
                    "id": user.id,
                    "avatar": str(user.avatar_url).split("?")[0],
                    "account creation date": f"{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} UTC/GMT",
                    "animated avatar": user.is_avatar_animated(),
                    "bot": user.bot,
                    "roles": [role.name for role in roles],
                },
                indent=4,
            )
        )
        embedinfo = discord.Embed(
            title=user.display_name,
            color=self.teal,
            description=f"Discriminator: {user.discriminator}\n"
            + f"ID: `{user.id}`\n"
            + f"Creation Date: `{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} UTC/GMT`\n"
            + f"Animated Avatar: {user.is_avatar_animated()}\n"
            + f"Bot: {user.bot}\n"
            + f'Roles: {list2str([f"<@&{role.id}>" for role in roles], 2)}'.replace(
                "True", "Yes"
            ).replace("False", "No"),
            inline=False,
        ).set_thumbnail(url=user.avatar_url)
        if user.nickname == user.display_name:
            embedinfo.description = f"Real Name: {user.name}\n" + embedinfo.description
        if getops(ctx.guild.id, "toggles", "jsonMenus"):
            await ctx.send(f'```json\n"user information": {jsoninfo}```')
        else:
            await ctx.send(embed=embedinfo)

    # Thanks to https://github.com/iwa for helping Hy out with the custom roles, and thanks to Hy for letting me reuse and adapt their code to Pengaelic Bot's systems
    @commands.command(name="speedtest", aliases=["st", "ping", "ng"], usage="no args")
    async def speedtest(self, ctx):
        if self.testing == False:
            self.testing = True
            async with ctx.typing():
                await get_event_loop().run_in_executor(
                    ThreadPoolExecutor(), self.TestSpeed
                )
            await ctx.channel.send(
                embed=discord.Embed(
                    title="Speedtest Results",
                    description=f'Server: {results["server"]["sponsor"]} {results["server"]["name"]}\n'
                    + 'Ping: {results["ping"]} ms\n'
                    + 'Download: {round(float((results["download"])/1000000), 2)} Mbps\n'
                    + 'Upload: {round(float((results["upload"])/1000000), 2)} Mbps\n\n'
                    + "*Conducted using Ookla's Speedtest CLI: https://speedtest.net*",
                    color=0x007F7F,
                ).set_footer(text=SpeedPerformTime)
            )
            self.testing = False
        else:
            await ctx.send(
                "<:winxp_information:869760946808180747>A test is already in progress. Please wait..."
            )

    @commands.command(name="role", usage="<hex code>\n<role name>")
    async def role(self, ctx, color, *, role_name):
        member = ctx.author
        role_lock = get(
            ctx.guild.roles, id=getops(ctx.guild.id, "roles", "customRoleLock")
        )
        if role_lock in member.roles or role_lock == None:
            try:
                result = getops(ctx.guild.id, "customRoles", str(member.id))
            except KeyError:
                result = None
            hex_code_match = search(r"(?:[0-9a-fA-F]{3}){1,2}$", color)
            if result and ctx.guild.get_role(int(result)):
                if hex_code_match:
                    role = ctx.guild.get_role(int(result))
                    await role.edit(name=role_name, color=discord.Color(int(color, 16)))
                    await member.add_roles(role)
                    await ctx.send(
                        f"<:winxp_information:869760946808180747>Role {role.mention} edited."
                    )
                else:
                    await ctx.send(
                        f"<:winxp_critical_error:869760946816553020>Invalid hex code `{color}`."
                    )
            else:
                if hex_code_match:
                    role_color = discord.Color(int(color, 16))
                    role = await ctx.guild.create_role(name=role_name, color=role_color)
                    await member.add_roles(role)
                    updop(ctx.guild.id, "customRoles", str(member.id), str(role.id))
                    await ctx.send(
                        f"<:winxp_information:869760946808180747>Role {role.mention} created and given."
                    )
                else:
                    await ctx.send(
                        f"<:winxp_critical_error:869760946816553020>Invalid hex code `{color}`."
                    )
        else:
            await ctx.send(
                f"{member.mention}, this is only for users with the {role_lock} role."
            )

    @commands.command(name="delrole", usage="no args")
    async def delrole(self, ctx):
        member = ctx.author
        role_lock = get(
            ctx.guild.roles, id=getops(ctx.guild.id, "roles", "customRoleLock")
        )
        if role_lock in member.roles or role_lock == None:
            result = getops(ctx.guild.id, "customRoles", str(member.id))
            if result:
                await member.remove_roles(ctx.guild.get_role(int(result)))
                await ctx.channel.send(f"Removed custom role.")
            else:
                await ctx.channel.send(
                    f"{member.mention}, you don't have a custom role to remove!"
                )
        else:
            await ctx.channel.send(
                f"{member.mention}, this is only for users with the {role_lock} role."
            )

    @commands.group(
        name="stopwatch", help="Track how long something goes.", usage="<start, stop>"
    )
    async def stopwatch(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send(
                embed=discord.Embed(
                    title="Stopwatch",
                    description="Track how long something goes.",
                    color=self.teal,
                )
                .add_field(name="(start/begin)", value="Start the stopwatch.")
                .add_field(name="(stop/end)", value="Stop the stopwatch.")
            )

    @stopwatch.command(
        name="start", help="Start the stopwatch.", aliases=["begin"], usage="no args"
    )
    async def stopwatch_start(self, ctx):
        Stopwatch.start(self)
        await ctx.send("Started the stopwatch.")

    @stopwatch.command(
        name="stop", help="Stop the stopwatch.", aliases=["end"], usage="no args"
    )
    async def stopwatch_end(self, ctx):
        await ctx.send(Stopwatch.end(self))

    @clear.error
    async def clearError(self, ctx, error):
        error = str(error)
        if (
            error
            == "You are missing Manage Messages permission(s) to run this command."
        ):
            await ctx.send(
                f"<:winxp_information:869760946808180747>{ctx.author.mention}, you have insufficient permissions (Manage Messages)"
            )
        else:
            await ctx.send(unhandling(error))

    @nuke.error
    async def nukeError(self, ctx, error):
        error = str(error)
        if (
            error
            == "You are missing Manage Channels permission(s) to run this command."
        ):
            await ctx.send(
                f"<:winxp_information:869760946808180747>{ctx.author.mention}, you have insufficient permissions (Manage Channels)"
            )
        else:
            await ctx.send(unhandling(error))

    @get_user_info.error
    async def getUserError(self, ctx, error):
        await ctx.send(
            unhandling(error)
        )  # await ctx.send("<:winxp_warning:869760947114348604>Invalid user specified!")


def setup(client):
    client.add_cog(Tools(client))
