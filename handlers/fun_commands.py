import discord
from discord.ext import commands
import random
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
        emoji = '👑' if result == 'Heads' else '🪙'

        embed = create_embed(
            title="🪙 Coin Flip",
            description=f"{emoji} **{result}!**",
            color="info"
        )

        await ctx.send(embed=embed)

    @bot.command(name='8ball')
    async def magic_8ball(ctx, *, question=None):
        """Magic 8-ball"""
        if not question:
            embed = create_embed(
                title="❌ No Question",
                description="Please ask a question!\nExample: `!8ball Will it rain today?`",
                color="error"
            )
            await ctx.send(embed=embed)
            return

        responses = [
            "Yes", "No", "Maybe", "Definitely", "Absolutely not",
            "Ask again later", "Very likely", "Unlikely", "Certainly",
            "Don't count on it", "Signs point to yes", "My sources say no"
        ]

        answer = random.choice(responses)

        embed = create_embed(
            title="🎱 Magic 8-Ball",
            description=f"**Question:** {question}\n**Answer:** {answer}",
            color="info"
        )

        await ctx.send(embed=embed)

    print("🎮 Fun commands loaded")