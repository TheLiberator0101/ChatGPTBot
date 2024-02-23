import discord
import openai
import requests
import io
from discord.ext import commands

# Your OpenAI API key
openai.api_key = 'OPENAI_API_KEY'

# Your Discord bot token
TOKEN = 'DISCORD_TOKEN'

# Define the intents
intents = discord.Intents.default()
# Enable the message content intent
intents.message_content = True

# Create a bot instance with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)


# Define a command to answer questions
@bot.command(name='ask', help='Asks GPT-4 a question and returns an answer.')
async def ask(ctx, *, question: str):
    try:
        # Generate a response using OpenAI's GPT-4 with the updated API method
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Replace with the appropriate GPT-4 model once available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        # Send the response back to the Discord channel
        await ctx.send(response.choices[0].message['content'])
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


@bot.command(name='createimage', help='Generates an image based on the provided prompt.')
async def create_image(ctx, *, prompt: str):
    try:
        # Generate an image using OpenAI's DALL·E with the updated API method
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=1,  # Generate 1 image
            size="1024x1024"  # Specify the image size
        )
        # The API returns a list of generated images, we take the first
        image_data = response.data[0].url
        # Download the image data in memory
        image_bytes = requests.get(image_data).content
        # Create a file-like object from the downloaded bytes
        with io.BytesIO(image_bytes) as image_file:
            # Send the image back to the Discord channel
            await ctx.send(file=discord.File(image_file, 'image.png'))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


# Command to analyze file content
@bot.command(name='analyze', help='Analyzes the content of a text file.')
async def analyze(ctx):
    # Check if there are any attachments in the message
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]  # Get the first attachment
        if attachment.filename.endswith('.txt'):  # Ensure it's a text file
            file_content = await attachment.read()  # Read the file content
            # Convert the content to a string
            text_content = file_content.decode('utf-8')

            try:
                # Use the chat completion endpoint for analysis
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Specify the chat model you're using
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": text_content}
                    ]
                )
                # Reply with the GPT-generated response
                await ctx.send(response.choices[0].message['content'])
            except Exception as e:
                await ctx.send(f"An error occurred: {str(e)}")
        else:
            await ctx.send("Please upload a '.txt' file.")
    else:
        await ctx.send("No file detected. Please attach a '.txt' file.")


# Run the bot
bot.run(TOKEN)
