# INVITE LINK: https://discord.com/oauth2/authorize?client_id=1256566625805668362&permissions=67584&integration_type=0&scope=bot+applications.commands

import discord, ollama, dotenv, os

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

prompt_override = 'off'
current_model = 'testmodel-5'

valid_models = [
    'llama2-uncensored',
    'testmodel-1',
    'testmodel-2',
    'testmodel-3',
    'testmodel-4',
    'testmodel-5',
    'testmodel-6',
    'testmodel-7',
    'testmodel-8'
]

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.event
async def on_message(message):
    global prompt_override
    global current_model

    if message.author != bot.user:
        async with message.channel.typing():
            if prompt_override != 'off':
                response = ollama.chat(model=current_model, messages=[
                    {
                        'role': 'user',
                        'content': "User" + " " + message.author.display_name + " asks: " + prompt_override,
                    },
                ])
                if 'message' in response and 'content' in response['message']:
                    print(response['message']['content'])
                    await message.channel.send(response['message']['content'][0:1999])
                else:
                    await message.channel.send("Error in response from model.")
            else:
                response = ollama.chat(model=current_model, messages=[
                    {
                        'role': 'user',
                        'content': "User" + " " + message.author.display_name + " asks: " + message.content,
                    },
                ])
                if 'message' in response and 'content' in response['message']:
                    await message.channel.send(response['message']['content'][0:1999])
                else:
                    await message.channel.send("Error in response from model.")

@bot.slash_command(name="change_model", description="Change the model")
@discord.option("text", description="Model to use", required=True)
async def change_model(ctx: discord.ApplicationContext, text: str):
    global current_model
    global valid_models

    if text in valid_models:
        current_model = text
        await ctx.respond(f"Model changed to `{text}`.", ephemeral=True)
        print(f"User {ctx.author} changed model to `{text}`.")
    else:
        print(f"User {ctx.author} FAILED to change model to `{text}`.")
        await ctx.respond(f"Model `{text}` is not valid.", ephemeral=True)

@bot.slash_command(name="override", description="Override prompt")
@discord.option("text", description="Text to override with", required=True)
async def override(ctx: discord.ApplicationContext, text: str):
    global prompt_override
    prompt_override = text
    print(f"User {ctx.author} set prompt override to `{text}`.")
    await ctx.respond(f"Prompt override set to `{text}`.", ephemeral=True)


bot.run(str(os.getenv("TOKEN"))) 