import disnake
from disnake.ext import commands

def custom_cooldown(message: disnake.ApplicationCommandInteraction):
    if message.author.id == 756496844867108937:
        return None
    else:
        return commands.Cooldown(10,60)