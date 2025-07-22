
import discord
from discord.ext import commands
import random
import asyncio
from utils.helpers import create_embed

def setup_fun_commands(bot):
    """Setup fun commands"""

    @bot.command(name='ping')
    async def ping(ctx):
        """Check bot latency"""
        latency = round(bot.latency * 1000)

        if latency < 100:
            status = "🟢 Excellent"
            color = "success"
        elif latency < 200:
            status = "🟡 Good"
            color = "warning"
        else:
            status = "🔴 Poor"
            color = "error"

        embed = create_embed(
            title="🏓 Pong!",
            description=f"Bot latency: **{latency}ms**\n{status}",
            color=color
        )

        await ctx.send(embed=embed)

    @bot.command(name='roll')
    async def roll_dice(ctx, dice="6"):
        """Roll dice"""
        try:
            sides = int(dice)
            if sides < 2:
                sides = 6
            if sides > 100:
                sides = 100

            result = random.randint(1, sides)

            embed = create_embed(
                title="🎲 Dice Roll",
                description=f"🎯 **You rolled:** {result}\n📊 **Range:** 1-{sides}",
                color="info"
            )

        except ValueError:
            embed = create_embed(
                title="❌ Invalid Input",
                description="Please provide a valid number!\nExample: `!roll 20`",
                color="error"
            )

        await ctx.send(embed=embed)

    @bot.command(name='flip', aliases=['coin'])
    async def flip_coin(ctx):
        """Flip a coin"""
        result = random.choice(['Heads', 'Tails'])
        emoji = "🪙" if result == "Heads" else "🔄"
        
        embed = create_embed(
            title=f"{emoji} Coin Flip",
            description=f"🎯 **Result:** {result}",
            color="info"
        )
        
        await ctx.send(embed=embed)

    @bot.command(name='8ball', aliases=['eightball', 'magic8'])
    async def magic_8ball(ctx, *, question=None):
        """Ask the magic 8-ball a question"""
        if not question:
            embed = create_embed(
                title="❌ No Question",
                description="Please ask a question!\nExample: `!8ball Will it rain today?`",
                color="error"
            )
            await ctx.send(embed=embed)
            return

        responses = [
            "🟢 It is certain", "🟢 Without a doubt", "🟢 Yes definitely",
            "🟢 You may rely on it", "🟢 As I see it, yes", "🟢 Most likely",
            "🟢 Outlook good", "🟢 Yes", "🟢 Signs point to yes",
            "🟡 Reply hazy, try again", "🟡 Ask again later", "🟡 Better not tell you now",
            "🟡 Cannot predict now", "🟡 Concentrate and ask again",
            "🔴 Don't count on it", "🔴 My reply is no", "🔴 My sources say no",
            "🔴 Outlook not so good", "🔴 Very doubtful"
        ]

        answer = random.choice(responses)
        
        embed = create_embed(
            title="🎱 Magic 8-Ball",
            description=f"**Question:** {question}\n**Answer:** {answer}",
            color="info"
        )
        
        await ctx.send(embed=embed)

    @bot.command(name='say', aliases=['echo'])
    @commands.has_permissions(manage_messages=True)
    async def say_command(ctx, *, message):
        """Make the bot say something"""
        try:
            await ctx.message.delete()
            await ctx.send(message)
        except discord.Forbidden:
            embed = create_embed(
                title="❌ Missing Permissions",
                description="I don't have permission to delete messages!",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='embed')
    @commands.has_permissions(manage_messages=True)
    async def embed_command(ctx, *, content):
        """Send a message in an embed"""
        embed = create_embed(
            title="📝 Message",
            description=content,
            color="info"
        )
        
        try:
            await ctx.message.delete()
        except:
            pass
            
        await ctx.send(embed=embed)

    print("🎪 Fun commands loaded successfully")
