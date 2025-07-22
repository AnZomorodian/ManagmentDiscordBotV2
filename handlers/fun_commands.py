
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
import discord
import random
import asyncio
from utils.helpers import create_embed
from utils.database import get_user_stats

def setup_fun_commands(bot):
    """Setup fun and entertainment commands"""
    
    @bot.command(name='ping')
    async def ping_command(ctx):
        """Check bot responsiveness and latency"""
        embed = create_embed(
            title="🏓 Pong!",
            description=f"Bot latency: **{round(bot.latency * 1000)}ms**\n🚀 Amazing Management Bot v3.0 is online!",
            color="success"
        )
        embed.add_field(name="📊 Status", value="✅ All systems operational", inline=True)
        embed.add_field(name="🌐 Servers", value=f"{len(bot.guilds)}", inline=True)
        embed.add_field(name="👥 Users", value=f"{sum(guild.member_count for guild in bot.guilds):,}", inline=True)
        
        await ctx.send(embed=embed)

    @bot.command(name='roll', aliases=['dice'])
    async def roll_dice(ctx, dice_input="6"):
        """Roll dice with various formats (6, 2d6, 3d20+5)"""
        try:
            # Parse different dice formats
            if 'd' in dice_input.lower():
                # Format: 2d6 or 2d6+3
                parts = dice_input.lower().split('d')
                num_dice = int(parts[0]) if parts[0] else 1
                
                # Check for modifiers (+3, -2, etc.)
                modifier = 0
                if '+' in parts[1]:
                    sides, mod = parts[1].split('+')
                    modifier = int(mod)
                elif '-' in parts[1]:
                    sides, mod = parts[1].split('-')
                    modifier = -int(mod)
                else:
                    sides = parts[1]
                
                sides = int(sides)
                
                # Limits for sanity
                if num_dice > 10:
                    num_dice = 10
                if sides > 100:
                    sides = 100
                    
                rolls = [random.randint(1, sides) for _ in range(num_dice)]
                total = sum(rolls) + modifier
                
                embed = create_embed(
                    title="🎲 Dice Roll Results",
                    description=f"**{dice_input}**",
                    color="info"
                )
                
                if num_dice == 1:
                    embed.add_field(name="Result", value=f"🎯 **{total}**", inline=False)
                else:
                    rolls_text = " + ".join(map(str, rolls))
                    if modifier != 0:
                        rolls_text += f" {'+' if modifier > 0 else ''}{modifier}"
                    
                    embed.add_field(name="Individual Rolls", value=rolls_text, inline=False)
                    embed.add_field(name="Total", value=f"🎯 **{total}**", inline=False)
                    
            else:
                # Simple format: just a number (sides of die)
                sides = int(dice_input)
                if sides > 100:
                    sides = 100
                result = random.randint(1, sides)
                
                embed = create_embed(
                    title="🎲 Dice Roll",
                    description=f"Rolling a **d{sides}**",
                    color="info"
                )
                embed.add_field(name="Result", value=f"🎯 **{result}**", inline=False)
                
            await ctx.send(embed=embed)
            
        except ValueError:
            embed = create_embed(
                title="❌ Invalid Dice Format",
                description="Use formats like: `6`, `2d6`, `3d20+5`, `1d100-10`",
                color="error"
            )
            await ctx.send(embed=embed)

    @bot.command(name='8ball', aliases=['eightball'])
    async def magic_8ball(ctx, *, question=None):
        """Ask the magic 8-ball a question"""
        if not question:
            embed = create_embed(
                title="🔮 Magic 8-Ball",
                description="You need to ask a question!\nExample: `!8ball Will it rain today?`",
                color="warning"
            )
            await ctx.send(embed=embed)
            return
            
        responses = [
            # Positive
            "🟢 It is certain", "🟢 Without a doubt", "🟢 Yes definitely",
            "🟢 You may rely on it", "🟢 As I see it, yes", "🟢 Most likely",
            "🟢 Outlook good", "🟢 Yes", "🟢 Signs point to yes",
            
            # Neutral/Uncertain  
            "🟡 Reply hazy, try again", "🟡 Ask again later", "🟡 Better not tell you now",
            "🟡 Cannot predict now", "🟡 Concentrate and ask again",
            
            # Negative
            "🔴 Don't count on it", "🔴 My reply is no", "🔴 My sources say no",
            "🔴 Outlook not so good", "🔴 Very doubtful"
        ]
        
        response = random.choice(responses)
        
        embed = create_embed(
            title="🔮 Magic 8-Ball",
            description=f"**Question:** {question}",
            color="info"
        )
        embed.add_field(name="Answer", value=response, inline=False)
        embed.set_footer(text=f"Asked by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)

    @bot.command(name='flip', aliases=['coin'])
    async def flip_coin(ctx):
        """Flip a coin"""
        result = random.choice(['Heads', 'Tails'])
        emoji = '👑' if result == 'Heads' else '⚡'
        
        embed = create_embed(
            title="🪙 Coin Flip",
            description=f"{emoji} **{result}**!",
            color="info"
        )
        embed.set_footer(text=f"Flipped by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)

    @bot.command(name='mystats', aliases=['stats', 'me'])
    async def user_stats(ctx):
        """Show your personal bot statistics"""
        user_stats = get_user_stats(ctx.author.id)
        
        embed = create_embed(
            title=f"📊 {ctx.author.display_name}'s Statistics",
            description="Your Amazing Management Bot activity",
            color="info",
            thumbnail=ctx.author.display_avatar.url
        )
        
        embed.add_field(name="🎵 Channels Created", value=f"{user_stats['channels_created']:,}", inline=True)
        embed.add_field(name="⌚ Total Voice Time", value=f"{user_stats['total_time']} min", inline=True)
        embed.add_field(name="⚡ Commands Used", value=f"{user_stats['commands_used']:,}", inline=True)
        
        # Achievements system
        achievements = []
        if user_stats['channels_created'] >= 10:
            achievements.append("🏠 Channel Builder")
        if user_stats['channels_created'] >= 50:
            achievements.append("🏗️ Architect")  
        if user_stats['commands_used'] >= 100:
            achievements.append("⚡ Power User")
        if user_stats['total_time'] >= 1440:  # 24 hours
            achievements.append("🎵 Voice Champion")
            
        if achievements:
            embed.add_field(name="🏆 Achievements", value="\n".join(achievements), inline=False)
        else:
            embed.add_field(name="🏆 Achievements", value="Keep using the bot to unlock achievements!", inline=False)
            
        embed.set_footer(text=f"Member since: {ctx.author.joined_at.strftime('%B %Y') if ctx.author.joined_at else 'Unknown'}")
        
        await ctx.send(embed=embed)

    @bot.command(name='choose', aliases=['pick'])
    async def choose_option(ctx, *, choices):
        """Choose between multiple options (separate with commas)"""
        if not choices:
            embed = create_embed(
                title="🤔 Choice Maker",
                description="Provide options separated by commas!\nExample: `!choose pizza, burgers, tacos`",
                color="warning"
            )
            await ctx.send(embed=embed)
            return
            
        options = [choice.strip() for choice in choices.split(',')]
        if len(options) < 2:
            embed = create_embed(
                title="❌ Need More Options",
                description="Please provide at least 2 choices separated by commas!",
                color="error"
            )
            await ctx.send(embed=embed)
            return
            
        choice = random.choice(options)
        
        embed = create_embed(
            title="🎯 Choice Made!",
            description=f"I choose: **{choice}**",
            color="success"
        )
        embed.add_field(name="Options were:", value=", ".join(options), inline=False)
        embed.set_footer(text=f"Choice made for {ctx.author.display_name}")
        
        await ctx.send(embed=embed)
