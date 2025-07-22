
import discord
from discord.ext import commands
import random
from utils.helpers import create_embed

def setup_fun_commands(bot):
    """Setup fun and entertainment commands"""

    @bot.command(name='ping')
    async def ping(ctx):
        """Check bot latency and status"""
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
            description=f"**Bot Latency:** {latency}ms\n**Status:** {status}\n**Response Time:** ⚡ Fast",
            color=color
        )

        await ctx.send(embed=embed)

    @bot.command(name='roll')
    async def roll_dice(ctx, dice="6"):
        """Roll dice with customizable sides"""
        try:
            # Handle multiple dice (e.g., 2d6)
            if 'd' in dice.lower():
                parts = dice.lower().split('d')
                if len(parts) == 2:
                    num_dice = int(parts[0]) if parts[0] else 1
                    sides = int(parts[1])
                    
                    if num_dice > 10:
                        num_dice = 10
                    if sides > 100:
                        sides = 100
                    
                    results = [random.randint(1, sides) for _ in range(num_dice)]
                    total = sum(results)
                    
                    embed = create_embed(
                        title="🎲 Dice Roll",
                        description=f"**Rolled:** {num_dice}d{sides}\n**Results:** {', '.join(map(str, results))}\n**Total:** {total}",
                        color="info"
                    )
                else:
                    raise ValueError
            else:
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
                description="**Examples:**\n`!roll 20` - Roll 1d20\n`!roll 3d6` - Roll 3d6\n`!roll` - Roll 1d6",
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
            description=f"🎯 **Result:** {result}\n🎰 **Chance:** 50/50",
            color="info"
        )
        
        await ctx.send(embed=embed)

    @bot.command(name='8ball', aliases=['eightball', 'magic8'])
    async def magic_8ball(ctx, *, question=None):
        """Ask the magic 8-ball a question"""
        if not question:
            embed = create_embed(
                title="❌ No Question",
                description="Please ask a question!\n**Example:** `!8ball Will it rain today?`",
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
            "🔴 Don't count on it", "🔴 My reply is no", "🔴 Outlook not so good",
            "🔴 Very doubtful", "🔴 My sources say no"
        ]

        response = random.choice(responses)
        
        embed = create_embed(
            title="🎱 Magic 8-Ball",
            description=f"**Question:** {question}\n**Answer:** {response}",
            color="info"
        )
        
        await ctx.send(embed=embed)

    @bot.command(name='choose', aliases=['pick', 'select'])
    async def choose_option(ctx, *options):
        """Choose randomly from given options"""
        if len(options) < 2:
            embed = create_embed(
                title="❌ Not Enough Options",
                description="Please provide at least 2 options!\n**Example:** `!choose pizza pasta salad`",
                color="error"
            )
            await ctx.send(embed=embed)
            return

        choice = random.choice(options)
        
        embed = create_embed(
            title="🎯 Random Choice",
            description=f"**Options:** {', '.join(options)}\n**I choose:** **{choice}**",
            color="success"
        )
        
        await ctx.send(embed=embed)

    @bot.command(name='joke')
    async def random_joke(ctx):
        """Tell a random programming joke"""
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, it's a hardware problem!",
            "Why do Java developers wear glasses? Because they can't C#!",
            "A SQL query goes into a bar, walks up to two tables and asks... 'Can I join you?'",
            "Why did the programmer quit his job? He didn't get arrays!",
            "What's a programmer's favorite hangout place? Foo Bar!",
            "Why don't programmers like nature? It has too many bugs!",
            "How do you comfort a JavaScript bug? You console it!"
        ]
        
        joke = random.choice(jokes)
        
        embed = create_embed(
            title="😂 Random Joke",
            description=joke,
            color="success"
        )
        
        await ctx.send(embed=embed)

    print("🎪 Fun commands loaded successfully")
