import discord
from discord.ext import commands
from discord import app_commands

IAWRBot = commands.Bot(command_prefix="'", intents = discord.Intents.all())


from IAWRtypes._QueueManager import QueueManager
#types
from IAWRtypes.OutputEditor import OutputEditorEntry
from IAWRtypes.ManagePlayer import ManagePlayerEntry
from IAWRtypes.SpawnPart import SpawnPartEntry

from queue_manager import queue_manager  #importa a instância compartilhada

@IAWRBot.event
async def on_ready():
    print(f'{IAWRBot.user.name} has connected to Discord!')
    commands = await IAWRBot.tree.sync()
    print(f'Synced {len(commands)} commands')
    for command in commands:
        print(f'    {command.name}')

@IAWRBot.tree.command(name="hello_world")
async def hello_world(interaction: discord.Interaction):
    queue_manager.add_to_queue(OutputEditorEntry(str(interaction.channel_id))
            .withType("addLine")
            .withValue("Hello World!")
    )
    
    await interaction.response.send_message("'Hello, World' has sent!")

@IAWRBot.tree.command(name="spawn_part")
@app_commands.describe(position="0, 0, 0",
                       size="1x1x1",
                       color="Red",
                       name="Connection Part Vermelhao",
                       texture="http://example.com/texture.png",
                       anchored="true",
                       transparency="0",
                       can_collide="true",
                       can_touch="true")
async def spawnPart(interaction: discord.Interaction, position: str, size: str, color: str = "white", name: str = "ConnectionPart", 
                    texture: str = "", anchored: bool = True, transparency: float = 0.0, can_collide: bool = True, can_touch: bool = True):
    
    queue_manager.add_to_queue(SpawnPartEntry(str(interaction.channel_id))
        .withPosition(position).withColor(color)
        .withSize(size).withName(name)
        .withTexture(texture).isAnchored(anchored)
        .withTransparency(transparency)
        .canCollide(can_collide).canTouch(can_touch)
    )
    
    await interaction.response.send_message("'SpawnPart' action has queued! position: {queue_manager.count()}")
