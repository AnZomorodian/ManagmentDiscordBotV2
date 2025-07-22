
import discord
import random
from discord.ext import commands
from utils.helpers import create_embed
from config.settings import EIGHT_BALL_RESPONSES

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

    @bot.command(name='coinflip', aliases=['flip', 'coin'])
    async def coinflip(ctx):
        """Flip a coin"""
        result = random.choice(['Heads', 'Tails'])
        emoji = '🪙' if result == 'Heads' else '🔘'
        
        embed = create_embed(
            title=f"{emoji} Coin Flip Result",
            description=f"The coin landed on **{result}**!",
            color="fun"
        )
        await ctx.send(embed=embed)

    @bot.command(name='roll', aliases=['dice'])
    async def roll_dice(ctx, sides: int = 100):
        """Roll a dice"""
        if sides < 2: 
            sides = 6
        if sides > 1000: 
            sides = 1000
            
        result = random.randint(1, sides)
        
        embed = create_embed(
            title="🎲 Dice Roll",
            description=f"You rolled a **{result}** out of {sides}!",
            color="fun"
        )
        await ctx.send(embed=embed)

    @bot.command(name='8ball', aliases=['eightball'])
    async def magic_8ball(ctx, *, question):
        """Ask the magic 8-ball a question"""
        response = random.choice(EIGHT_BALL_RESPONSES)
        
        embed = create_embed(
            title="🎱 Magic 8-Ball",
            description=f"**Question:** {question}\n**Answer:** {response}",
            color="fun"
        )
        await ctx.send(embed=embed)

    @bot.command(name='choose', aliases=['pick'])
    async def choose_option(ctx, *choices):
        """Choose between multiple options"""
        if len(choices) < 2:
            return await ctx.send("❌ Please provide at least 2 choices!")
        
        choice = random.choice(choices)
        
        embed = create_embed(
            title="🎯 Choice Made!",
            description=f"I choose: **{choice}**",
            color="fun"
        )
        embed.add_field(name="Options", value=" • ".join(choices), inline=False)
        await ctx.send(embed=embed)

    @bot.command(name='uptime')
    async def uptime(ctx):
        """Show bot uptime"""
        embed = create_embed(
            title="⏰ Bot Uptime v3.0",
            description="🚀 Management Bot v3.0 running with modular architecture!\n⚡ All systems operational",
            color="info"
        )
        await ctx.send(embed=embed)

    print("🎮 Fun commands loaded")
