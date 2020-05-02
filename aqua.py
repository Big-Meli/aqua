import discord
from discord.ext import commands
import random
import re 
import asyncio
import json
import requests
from termcolor import colored

class runtime:
    class utils:
        developers = ["685384266736992256", "405065319887929354", "386913021488005120"]

        class text:
            def grey(this_text):
                return colored(this_text, "grey")
            def red(this_text):
                return colored(this_text, "red")
            def green(this_text):
                return colored(this_text, "green")
            def yellow(this_text):
                return colored(this_text, "yellow")
            def blue(this_text):
                return colored(this_text, "blue")
            def magenta(this_text):
                return colored(this_text, "magenta")
            def cyan(this_text):
                return colored(this_text, "cyan")
            def white(this_text):
                return colored(this_text, "white")
        class json:
            json_curr = {}

            api_key = "$2b$10$aUDCMcYIOhBMIJNklayjV.cnQHgCQ9kuk9hw0Y/ny.BG7jKZkGkoa"
            
            async def dump():
                with open("jsons/main.json",  "w") as file:
                    json.dump(runtime.utils.json.json_curr, file, sort_keys=True, indent=4, separators=(',', ': '))

            async def load():
                with open("jsons/main.json", "r") as file:
                    runtime.utils.json.json_curr = json.load(file)

            async def new_user(user_id):
                runtime.utils.json.json_curr["global"]["users"][user_id] = {}

                runtime.utils.json.json_curr["global"]["users"][user_id]["good_karma"] = 0
                runtime.utils.json.json_curr["global"]["users"][user_id]["bad_karma"] = 0
                runtime.utils.json.json_curr["global"]["users"][user_id]["friends"] = []
                runtime.utils.json.json_curr["global"]["users"][user_id]["friend_invites"] = []

                runtime.utils.json.json_curr["global"]["users"][user_id]["xp"] = []
                runtime.utils.json.json_curr["global"]["users"][user_id]["level"] = []
                runtime.utils.json.json_curr["global"]["users"][user_id]["inventory"] = []

                await runtime.utils.json.dump()

    class bot:
        class command:
            class error:
                async def syntax(ctx, correct_syntax):
                    print(runtime.utils.text.cyan("_________________"))
                    print("Trigger:", runtime.utils.text.cyan("Command send"))
                    print("Trigger Author Name:", runtime.utils.text.cyan(ctx.message.author.name))
                    print("Trigger Author Id:", runtime.utils.text.cyan(ctx.message.author.id))
                    print("Trigger Text:", runtime.utils.text.cyan(ctx.message.content))
                    print("Trigger Status:", runtime.utils.text.red("Bad"))
                    print(runtime.utils.text.cyan("_________________"))

                    embed = discord.Embed(title="Command Error", colour=discord.Colour(0x00FFFF))
                    embed.add_field(name="An error occured which could only mean you have used the **incorrect** syntax!", value="This is the syntax you should be using!: `%s`"%correct_syntax)

                    await ctx.send(embed=embed)
            class success:
                async def send(ctx, embed_title, embed_fields):
                    print(runtime.utils.text.cyan("_________________"))
                    print("Trigger:", runtime.utils.text.cyan("Command send"))
                    print("Trigger Author Name:", runtime.utils.text.cyan(ctx.message.author.name))
                    print("Trigger Author Id:", runtime.utils.text.cyan(ctx.message.author.id))
                    print("Trigger Text:", runtime.utils.text.cyan(ctx.message.content))
                    print("Trigger Status:", runtime.utils.text.green("Good"))
                    print(runtime.utils.text.cyan("_________________"))

                    embed = discord.Embed(title=embed_title, colour=discord.Colour(0x00FFFF))
                    for field in embed_fields:
                        embed.add_field(name=field["name"], value=field["value"])

                    await ctx.send(embed=embed)
        
        uptime = 0
        token = "token" # Redacted for personal reasons
            
aqua = commands.Bot(command_prefix="aq:", description="AquaBot, a useless bot for a useless waifu?")

@aqua.event
async def on_ready():
    print(runtime.utils.text.cyan("_________________"))
    print("Username:", runtime.utils.text.cyan(aqua.user.name))
    print("Id:", runtime.utils.text.cyan(aqua.user.id))
    print("Token:", runtime.utils.text.cyan(runtime.bot.token))
    print("Up:", runtime.utils.text.green("Yes"))
    print(runtime.utils.text.cyan("_________________"))
    
    await runtime.utils.json.load()
    await runtime.utils.json.users.update()
    print("First Json Load Ok:", runtime.utils.text.green("Yes"))
    print(runtime.utils.text.cyan("_________________"))

    while True:
        runtime.bot.uptime += 1
        await asyncio.sleep(0.001)

@aqua.command()
async def dev(ctx, *null_args):
    dev_args = " ".join(null_args)
    if str(ctx.author.id) in runtime.utils.developers:
        if null_args in ["karma", "bellow", "quit"]:
            if null_args == "quit":
                await runtime.bot.command.success.send(ctx=ctx, embed_title="Time to Head Out!", embed_fields=[{"name": "The bot will shut down when", "value": "**-** Final Json Dump finishes\n**-** Version Updates\n"}])
                runtime.utils.json.json_curr["dev"]["version"] += 1
                runtime.utils.json.dump()

                quit()
        else:
            await runtime.bot.command.error.syntax(ctx=ctx, correct_syntax="aq:dev (karma|bellow|quit)")

    else:
        await runtime.bot.command.error.syntax(ctx=ctx, correct_syntax="aq:dev (karma|bellow|quit)")

@aqua.command()
async def calculate(ctx, calculation:str):
    if re.match(r"[0-9\*\-\+\(\)\/\.]+", calculation):
        try:
            await runtime.bot.command.success.send(ctx=ctx, embed_title="Calculation!", embed_fields=[{"name": "The result of your calculation is", "value": eval(calculation)}])

        except:
            await runtime.bot.command.error.syntax(ctx=ctx, correct_syntax="aq:calculate ([0-9\*\-\+\(\)\/\.]+)")
    else:
        await runtime.bot.command.error.syntax(ctx=ctx, correct_syntax="aq:calculate ([0-9\*\-\+\(\)\/\.]+)")

@aqua.command()
async def roll(ctx, *dice_args:str):
    dice_args = " ".join(dice_args)
    try:
        if re.match(r"^([1-9][0-9]*)\s*([1-9][0-9]*)", dice_args):
            tmp = re.findall(r"^([1-9][0-9]*)\s*([1-9][0-9]*)", dice_args)[0]
            dice_number = int(tmp[1])
            roll_amount = int(tmp[0])

            await runtime.bot.command.success.send(ctx=ctx, embed_title="Roll That Dice!", embed_fields=[{"name": "The result of dice roll number **%i** is"%(roll+1), "value": random.randint(1, dice_number)} for roll in range(roll_amount)])
        
        else:
            await runtime.bot.command.error.syntax(ctx=ctx, correct_syntax="aq:roll (([1-9][0-9]*)|Amount of rolls)\s*(([1-9][0-9]*)|Sides amount)")

    except Exception as e:
        print(runtime.utils.text.cyan("_________________"))
        print("Exception Occured:", runtime.utils.text.green("Yes"))
        print("Exception:", runtime.utils.text.red(e))
        print(runtime.utils.text.cyan("_________________"))

        await runtime.bot.command.error.syntax(ctx=ctx, correct_syntax="aq:roll (([1-9][0-9]*)|Amount of rolls)\s*(([1-9][0-9]*)|Sides amount)")

@aqua.command()
async def uptime(ctx, *null_args):
    await runtime.bot.command.success.send(ctx=ctx, embed_title="Uptime!", embed_fields=[{"name": "The total uptime since the last update is", "value":"In ms: {}\nIn seconds: {}\nIn minutes: {}\nIn hours: {}".format(runtime.bot.uptime, runtime.bot.uptime/1000, runtime.bot.uptime/60000, runtime.bot.uptime/3600000)}])

@aqua.command()
async def invite(ctx, *null_args):
    await runtime.bot.command.success.send(ctx=ctx, embed_title="Invite me!", embed_fields=[{"name": "You can use the link below to invite me to your server!", "value": "**__https://discordapp.com/api/oauth2/authorize?client_id=705026806230810685&permissions=0&scope=bot__**"}])

@aqua.command()
async def karma(ctx, *null_args):
    if str(ctx.author.id) not in runtime.utils.json.json_curr["global"]["users"]:
        await runtime.utils.json.new_user(str(ctx.author.id))

    await runtime.bot.command.success.send(ctx=ctx, embed_title="The good and bad", embed_fields=[{"name": "Let's take a look at your karma entries shall we?", "value": "Good Karma: **{}**\nBad Karma: **{}**\nOverall Karma: **{}**".format(runtime.utils.json.json_curr["global"]["users"][str(ctx.author.id)]["good_karma"], runtime.utils.json.json_curr["global"]["users"][str(ctx.author.id)]["bad_karma"], (runtime.utils.json.json_curr["global"]["users"][str(ctx.author.id)]["good_karma"] - runtime.utils.json.json_curr["global"]["users"][str(ctx.author.id)]["bad_karma"]))}])

@aqua.event
async def on_reaction_add(reaction, user):
    if str(reaction.message.author.id) not in runtime.utils.json.json_curr["global"]["users"]:
            runtime.utils.json.new_user(str(reaction.message.author.id))

    if reaction.emoji == "⬇":
        runtime.utils.json.json_curr["global"]["users"][str(reaction.message.author.id)]["bad_karma"] += 1
    
    elif reaction.emoji == "⬆":

        runtime.utils.json.json_curr["global"]["users"][str(reaction.message.author.id)]["good_karma"] += 1

    await runtime.utils.json.dump()

@aqua.event
async def on_reaction_remove(reaction, user):
    if str(reaction.message.author.id) not in runtime.utils.json.json_curr["global"]["users"]:
            runtime.utils.json.new_user(str(reaction.message.author.id))

    if reaction.emoji == "⬇":

        runtime.utils.json.json_curr["global"]["users"][str(reaction.message.author.id)]["bad_karma"] -= 1
            
    elif reaction.emoji == "⬆":
        runtime.utils.json.json_curr["global"]["users"][str(reaction.message.author.id)]["good_karma"] -= 1

    await runtime.utils.json.dump()

@aqua.event
async def on_message(ctx):
    if str(ctx.author.id) not in runtime.utils.json.json_curr["global"]["users"]:
        await runtime.utils.json.new_user(str(ctx.author.id))

    await ctx.add_reaction("⬆")
    await ctx.add_reaction("⬇")
    runtime.utils.json.json_curr["global"]["users"][str(ctx.author.id)]["good_karma"] -= 1
    runtime.utils.json.json_curr["global"]["users"][str(ctx.author.id)]["bad_karma"] -= 1
    await aqua.process_commands(ctx)


aqua.run(runtime.bot.token)
#aqua.run("")
#tmux ls
#tmux a -t {id}
