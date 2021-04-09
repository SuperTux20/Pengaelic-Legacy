import discord
from pengaelicutils import options
from subprocess import check_output
from discord.ext import commands
from asyncio import sleep
from random import randint
from json import dumps

class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cyan = 32639
    nukeconfirm = False
    name = "tools"
    name_typable = name
    description = "Various tools and info."
    description_long = description

    @commands.command(name="os", help="Read what OS I'm running on!", aliases=["getos"])
    async def showOS(self, ctx):
        os = check_output(
            'neofetch | grep OS | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g"',
            shell=True
        ).decode().split(':')[1][1:-2].split("x86")[0][:-1]
        kernel = check_output(
            'neofetch | grep Kernel | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g"',
            shell=True
        ).decode().split(':')[1][1:-2]
        await ctx.send(f"I'm running on {os}, kernel version {kernel}.")

    @commands.command(name="ping", help="How slow am I to respond?", aliases=["ng"])
    async def ping(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title=":ping_pong: Pong!",
                description=f"{round(self.client.latency * 1000)} ms",
                color=32639
            ).set_image(url="https://supertux20.github.io/Pengaelic-Bot/images/gifs/pingpong.gif")
        )

    @commands.command(name="test", help="Am I online? I'm not sure.")
    async def test(self, ctx):
        await ctx.send("Yep, I'm alive :sunglasses:")

    @commands.command(name="avatar", help="Get someone's avatar.", usage="[username or nickname or @mention]", aliases=["pfp", "profilepic"])
    async def get_avatar(self, ctx, *, member: discord.Member = None):
        avatar2get = ctx.author
        embed = discord.Embed(
            title="Here's your avatar!",
            color=32639
        )
        if member:
            avatar2get = member
            if member.id == 736720500285505596:
                embed = discord.Embed(
                    title="Here's my avatar!",
                    color=32639
                )
            else:
                embed = discord.Embed(
                    title=f"Here's {member.display_name}'s avatar!",
                    color=32639
                )
        embed.set_image(url=avatar2get.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="icon", help="Get the icon for the server.", aliases=["servericon"])
    async def get_icon(self, ctx):
        try:
            await ctx.send(
                embed=discord.Embed(
                    title="Here's the server icon!",
                    color=32639
                ).set_image(
                    url=ctx.guild.icon_url
                )
            )
        except:
            await ctx.send(
                "This server doesn't have an icon... :pensive:"
            )

    @commands.command(name="emoji", help="Get the specified (server-specific) emoji.", usage="[:emoji:]", aliases=["emote"])
    async def get_emoji(self, ctx, emoji=None):
        emojis = [
            f"<:{em.name}:{em.id}>" for em in ctx.guild.emojis
        ]
        emojiurls = [
            f"https://cdn.discordapp.com/emojis/{em.id}.png" for em in ctx.guild.emojis
        ]
        if emoji == None:
            await ctx.send("Here's all the emojis on this server.\n" + str(emojis)[1:-1].replace("'", "").replace(", ", ""))
        else:
            if emoji in emojis:
                await ctx.send(
                    embed=discord.Embed(
                        title="Here's your emoji!",
                        color=32639
                    ).set_image(
                        url=emojiurls[emojis.index(emoji)]
                    )
                )
            else:
                await ctx.send("Invalid emoji specified!")

    @commands.command(name="poll", help="Send a poll!", aliases=["suggest"], usage='"<poll name>" <poll content>')
    async def poll(self, ctx, title=None, *, arg=None):
        if title == None:
            await ctx.send("You didn't specify a name for the poll!")
        if arg == None:
            await ctx.send("You didn't specify anything to make a poll for!")
        else:
            the_poll = await ctx.send(
                embed=discord.Embed(
                    color=randint(0, 16777215),
                    title=title,
                    description=arg
                ).set_author(
                    name=ctx.author.name,
                    icon_url=ctx.author.avatar_url
                )
            )
            await the_poll.add_reaction("✅")
            await the_poll.add_reaction("❌")
            try:
                await ctx.message.delete()
            except:
                pass

    @commands.command(name="clear", help="Clear some messages away.", aliases=["delmsgs", "purge"], usage="[number of messages to delete (5)]")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, msgcount: int = 5):
        await ctx.channel.purge(limit=msgcount + 1)
        report = await ctx.send(f"{msgcount} (probably) messages deleted.")
        await sleep(3)
        try:
            await report.delete()
        except:
            pass

    @commands.command(name="nuke", help="Purge a channel of EVERYTHING.", aliases=["wipe", "wipechannel"])
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        if not self.nukeconfirm:
            await ctx.send(f"Are you **really** sure you want to wipe this channel? Type the command again to confirm. This will expire in 10 seconds.")
            self.nukeconfirm = True
            await sleep(10)
            if self.nukeconfirm:
                self.nukeconfirm = False
                await ctx.send("Pending nuke expired.")
        elif self.nukeconfirm:
            newchannel = await ctx.channel.clone(reason=f"Nuking #{ctx.channel.name}")
            await newchannel.edit(position=ctx.channel.position, reason=f"Nuking #{ctx.channel.name}")
            await ctx.channel.delete(reason=f"Nuked #{ctx.channel.name}")
            self.nukeconfirm = False

    @commands.command(name="server", help="See a bunch of data about the server at a glance.", aliases=["info"])
    @commands.has_permissions(manage_messages=True)
    async def get_server_info(self, ctx):
        guild = ctx.guild
        owner = guild.owner
        if guild.owner.nick == None:
            owner.nick = owner.name
        creation = guild.created_at
        jsoninfo = str(
            dumps(
                {
                    "basic info": {
                        "server name": guild.name,
                        "server owner": f"{owner.nick} ({owner.name}#{owner.discriminator})",
                        "server id": guild.id,
                        "two-factor authentication": bool(guild.mfa_level),
                        "creation date": f"{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} UTC/GMT"
                    },
                    "levels": {
                        "verification level": f"{guild.verification_level[0]} (level {guild.verification_level[1]+1})",
                        "notification level": f"{guild.default_notifications[0].replace('_',' ')} (level {guild.default_notifications[1]+1})",
                        "content filter": f"{guild.explicit_content_filter[0].replace('_',' ')} (level {guild.explicit_content_filter[1]+1})"
                    },
                    "counts": {
                        "members": guild.member_count,
                        "boosters": guild.premium_subscription_count,
                        "text channels": len(guild.text_channels),
                        "voice channels": len(guild.voice_channels),
                        "channel categories": len(guild.categories),
                        "emojis": len(guild.emojis)
                    }
                },
                indent=4
            )
        )
        embedinfo = discord.Embed(
            title="Server Details",
            color=self.cyan
        ).add_field(
            name="Basic Info",
            value=f"""Server Name: {guild.name}
                Server Owner: "{owner.nick}" (`{owner.name}#{owner.discriminator}`)
                Server ID: `{guild.id}`
                Two-Factor Authentication: {bool(guild.mfa_level)}
                Creation Date: `{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} UTC/GMT`""".replace("True", "Enabled").replace("False", "Disabled"),
            inline=False
        ).add_field(
            name="Levels",
            value=f"""Verification Level: {guild.verification_level[0]} (level {guild.verification_level[1]+1}),
                Notification Level: {guild.default_notifications[0].replace('_',' ')} (level {guild.default_notifications[1]+1}),
                Content Filter: {guild.explicit_content_filter[0].replace('_',' ')} (level {guild.explicit_content_filter[1]+1})""",
            inline=False
        ).add_field(
            name="Counts",
            value=f"""Members: {guild.member_count}
                Boosters: {guild.premium_subscription_count}
                Text Channels: {len(guild.text_channels)}
                Voice Channels: {len(guild.voice_channels)}
                Channel Categories: {len(guild.categories)}
                Emojis: {len(guild.emojis)}""",
            inline=False
        )
        if options(guild.id, "jsonMenus"):
            await ctx.send(f'```json\n"server information": {jsoninfo}```')
        else:
            await ctx.send(embed=embedinfo)

    @clear.error
    async def clearError(self, ctx, error):
        if str(error) == "You are missing Manage Messages permission(s) to run this command.":
            await ctx.send(
                f"{ctx.author.mention}, you have insufficient permissions (Manage Messages)"
            )
        else:
            await ctx.send(f"Unhandled error occurred:\n```{error}```If my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!")

    @nuke.error
    async def nukeError(self, ctx, error):
        if str(error) == "You are missing Manage Channels permission(s) to run this command.":
            await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Channels)")
        else:
            await ctx.send(f"Unhandled error occurred:\n```{error}```\nIf my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!")

    @get_avatar.error
    async def avatarError(self, ctx, error):
        await ctx.send("Invalid user specified!")

def setup(client):
    client.add_cog(Tools(client))