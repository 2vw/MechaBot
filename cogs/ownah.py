import voltage, asyncio, json, datetime, time
from voltage.ext import commands


class owner(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.name = "Owner"
        self.description = "For the cool kids only! (just to test commands ignore most of these u probably cant use them)"

    @commands.command(description="Change the presence or status of Mecha!")
    async def status(self, ctx, *, status, presence=None):
        if ctx.author.id in [
            "01FZB2QAPRVT8PVMF11480GRCD",
            "01FZBQCQPT53YTAD86T28WV69X",
        ]:
            if not presence:
                await self.client.set_status(status, voltage.PresenceType.online)
                return await ctx.send(f"Changed status to `{status}`")
            else:
                if presence.lower() == "online":
                    await self.client.set_status(status, voltage.PresenceType.online)
                    return await ctx.send(
                        f"Changed status to `{status}` and a presence of `Online!`"
                    )
                elif presence.lower() == "idle":
                    await self.client.set_status(status, voltage.PresenceType.idle)
                    return await ctx.send(
                        f"Changed status to `{status}` and a presence of `Idle`!"
                    )
                elif presence.lower() == "dnd" or "busy":
                    await self.client.set_status(status, voltage.PresenceType.busy)
                    return await ctx.send(
                        f"Changed status to `{status}` and a presence of `Do Not Disturb`!"
                    )
        else:
            return await ctx.send("You aren't an owner of this bot!")

    @commands.command()
    async def test(self, ctx):
        embed = voltage.ImageEmbed(url="https://i.imgur.com/2LNlDQW.jpg")
        await ctx.send(content="[]()", embed=embed)

    @commands.command(description="Test our command")
    async def register(self, ctx):

        with open("json/users.json", "r") as f:
            data = json.load(f)
        if ctx.author.id in data:
            return await ctx.send("You're already registered!")
        with open("json/users.json", "w") as f:
            data[ctx.author.id] = {
                "username": ctx.author.name,
                "id": ctx.author.id,
                "bio": "User has no bio set!",
                "beta": "False",
                "ff": "False",
                "notifications": []
            }
            json.dump(data, f, indent=2)
        embed = voltage.SendableEmbed(description="## You're registered!")
        await ctx.send(content="[]()", embed=embed)

    @commands.command(description="Send a notification to every user registered!")
    async def notify(self, ctx, *, message):
        if ctx.author.id == "01FZB2QAPRVT8PVMF11480GRCD":
            with open("json/users.json", "r") as f:
                data = json.load(f)
            date = datetime.datetime.now()
            starttime = time.time()
            format = f"{date.strftime('%b %d')} | {message}"
            with open("json/users.json", "w") as f:
                for id in data:
                    data[id]["notifications"].append(format)
                json.dump(data, f, indent=2)
            await ctx.send(f"Notified `{len(data)}` users in {round(time.time() - starttime, 5)}s")
        else:
            return await ctx.send("You aren't an owner! You can't use this command!")

    @commands.command(description="Use this after registering")
    async def ar(self, ctx):
        with open("json/users.json", "r") as f:
            data = json.load(f)
        embed = voltage.SendableEmbed(
            description=f"{data[ctx.author.id]['username']}'s profile:\n\n**Bio:**\n{data[ctx.author.id]['bio']}\n\n**User's settings:**\n\nBeta: `{data[ctx.author.id]['beta']}`\nFamily Friendly Mode: `{data[ctx.author.id]['ff']}`"
        )
        await ctx.send(content="[]()", embed=embed)

def setup(client) -> commands.Cog:
  return owner(client)