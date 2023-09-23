import os
import discord
import random
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta
from messages import GREETINGS, RANDOM_QUOTES, GOOD_THINGS_MESSAGES, QUESTIONS, CC_QUESTIONS

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID'))
VERIFIED_ROLE_ID = int(os.getenv('VERIFIED_ROLE_ID'))
ERROR_CHANNEL_ID = int(os.getenv('ERROR_CHANNEL_ID'))
GOOD_THINGS_CHANNEL_ID = int(os.getenv('GOOD_THINGS_CHANNEL_ID'))
OFF_TOPIC_CHANNEL_ID = int(os.getenv('OFF_TOPIC_CHANNEL_ID'))
CC_CHAT_CHANNEL_ID = int(os.getenv('CC_CHAT_CHANNEL_ID'))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    random_quote.start()
    post_good_things.start()
    post_question.start()
    post_cc_chat_question.start()

@tasks.loop(hours=168)  # Loop every 168 hours (1 week)
async def random_quote():
    # Load values from .env file
    TOKEN = os.getenv('DISCORD_TOKEN')
    COMMUNITY_HALL_CHANNEL_ID = int(os.getenv('COMMUNITY_HALL_CHANNEL_ID'))

    # Get the current day of the week (0=Monday, 6=Sunday)
    current_day = datetime.utcnow().weekday()

    # Check if it's Monday and the time is 8:00am GMT
    if current_day == 0 and datetime.utcnow().time() == datetime.time(8, 0):
        # Select a random quote of the week
        selected_quote = random.choice(RANDOM_QUOTES)

        try:
            # Send random quote to the specified channel
            community_hall_channel = bot.get_channel(COMMUNITY_HALL_CHANNEL_ID)
            if community_hall_channel:
                await community_hall_channel.send(selected_quote)
        except Exception as e:
        # Log the error in the specified error channel
            error_channel = bot.get_channel(ERROR_CHANNEL_ID)
            if error_channel:
                await error_channel.send(f'Error in random_quote: {e}')

@random_quote.before_loop
async def before_random_quote():
    # Calculate the delay until the next Monday at 8:00am GMT
    now = datetime.utcnow()
    next_monday = now + timedelta(days=(0 - now.weekday()) % 7, hours=-now.hour, minutes=-now.minute, seconds=-now.second)
    target_time = next_monday.replace(hour=8, minute=0, second=0, microsecond=0)

    # Calculate the delay in seconds
    delay = (target_time - now).total_seconds()
    if delay < 0:
        delay += 7 * 24 * 60 * 60  # Add a week if the target time has passed this week

    await discord.utils.sleep_until(target_time)
    random_quote.start()

@tasks.loop(hours=168)  # Loop every 168 hours (1 week)
async def post_cc_chat_question():
    # Load values from .env file
    TOKEN = os.getenv('DISCORD_TOKEN')
    CC_CHAT_CHANNEL_ID = int(os.getenv('CC_CHAT_CHANNEL_ID'))

    # Get the current day of the week (0=Monday, 6=Sunday)
    current_day = datetime.utcnow().weekday()

    # Check if it's Tuesday and the time is 12:30 GMT
    if current_day == 1 and datetime.utcnow().time() == datetime.time(12, 30):
        # Select a random question for cc-chat
        selected_question = random.choice(CC_QUESTIONS)

        try:
            # Send the question to the "cc-chat" channel
            cc_chat_channel = bot.get_channel(CC_CHAT_CHANNEL_ID)
            if cc_chat_channel:
                await cc_chat_channel.send(f"{selected_question}")
        except Exception as e:
        # Log the error in the specified error channel
            error_channel = bot.get_channel(ERROR_CHANNEL_ID)
            if error_channel:
                await error_channel.send(f'Error in cc_chat_question: {e}')

@post_cc_chat_question.before_loop
async def before_post_cc_chat_question():
    # Calculate the delay until the next Tuesday at 12:30 GMT
    now = datetime.utcnow()
    days_until_tuesday = (1 - now.weekday()) % 7  # Calculate days until next Tuesday
    target_time = (now + timedelta(days=days_until_tuesday)).replace(hour=12, minute=30, second=0, microsecond=0)

    # Calculate the delay in seconds
    delay = (target_time - now).total_seconds()
    if delay < 0:
        delay += 7 * 24 * 60 * 60  # Add a week if the target time has passed this week

    await discord.utils.sleep_until(target_time)
    post_cc_chat_question.start()

@tasks.loop(hours=168)  # Loop every 168 hours (1 week)
async def post_good_things():
    # Load values from .env file
    TOKEN = os.getenv('DISCORD_TOKEN')
    GOOD_THINGS_CHANNEL_ID = int(os.getenv('GOOD_THINGS_CHANNEL_ID'))

    # Get the current day of the week (0=Monday, 6=Sunday)
    current_day = datetime.utcnow().weekday()

    # Check if it's Friday and the time is 12:00 midday GMT
    if current_day == 4 and datetime.utcnow().time() == datetime.time(12, 0):
        # Select a random good things message
        selected_message = random.choice(GOOD_THINGS_MESSAGES)

        try:
            # Send the message to the "3goodthings" channel
            good_things_channel = bot.get_channel(GOOD_THINGS_CHANNEL_ID)
            if good_things_channel:
                await good_things_channel.send(selected_message)
        except Exception as e:
        # Log the error in the specified error channel
            error_channel = bot.get_channel(ERROR_CHANNEL_ID)
            if error_channel:
                await error_channel.send(f'Error in good_things: {e}')

@post_good_things.before_loop
async def before_post_good_things():
    # Calculate the delay until the next Friday at 12:00 midday GMT
    now = datetime.utcnow()
    days_until_friday = (4 - now.weekday()) % 7  # Calculate days until next Friday
    target_time = (now + timedelta(days=days_until_friday)).replace(hour=12, minute=0, second=0, microsecond=0)

    # Calculate the delay in seconds
    delay = (target_time - now).total_seconds()
    if delay < 0:
        delay += 7 * 24 * 60 * 60  # Add a week if the target time has passed this week

    await discord.utils.sleep_until(target_time)
    post_good_things.start()

@tasks.loop(hours=168)  # Loop every 168 hours (1 week)
async def post_question():
    # Load values from .env file
    TOKEN = os.getenv('DISCORD_TOKEN')
    OFF_TOPIC_CHANNEL_ID = int(os.getenv('OFF_TOPIC_CHANNEL_ID'))

    # Get the current day of the week (0=Monday, 6=Sunday)
    current_day = datetime.utcnow().weekday()

    # Check if it's Wednesday and the time is 16:00 GMT
    if current_day == 2 and datetime.utcnow().time() == datetime.time(16, 0):
        # Select a random question
        selected_question = random.choice(QUESTIONS)

        try:
            # Send the question to the "off-topic" channel
            off_topic_channel = bot.get_channel(OFF_TOPIC_CHANNEL_ID)
            if off_topic_channel:
                await off_topic_channel.send(f"Question of the week:\n{selected_question}")
        except Exception as e:
        # Log the error in the specified error channel
            error_channel = bot.get_channel(ERROR_CHANNEL_ID)
            if error_channel:
                await error_channel.send(f'Error in 0ff_topic_question: {e}')

@post_question.before_loop
async def before_post_question():
    # Calculate the delay until the next Wednesday at 16:00 GMT
    now = datetime.utcnow()
    days_until_wednesday = (2 - now.weekday()) % 7  # Calculate days until next Wednesday
    target_time = (now + timedelta(days=days_until_wednesday)).replace(hour=16, minute=0, second=0, microsecond=0)

    # Calculate the delay in seconds
    delay = (target_time - now).total_seconds()
    if delay < 0:
        delay += 7 * 24 * 60 * 60  # Add a week if the target time has passed this week

    await discord.utils.sleep_until(target_time)
    post_question.start()

@bot.event
async def on_member_update(before, after):
    # Load values from .env file
    TOKEN = os.getenv('DISCORD_TOKEN')
    COMMUNITY_HALL_CHANNEL_ID = int(os.getenv('COMMUNITY_HALL_CHANNEL_ID'))
    VERIFIED_ROLE_ID = int(os.getenv('VERIFIED_ROLE_ID'))

    # Check if the user gained the "Verified" role and has a verified email
    if (VERIFIED_ROLE_ID in [role.id for role in after.roles] and
            VERIFIED_ROLE_ID not in [role.id for role in before.roles] and
            after.email):
        # Select a random greeting
        selected_greeting = random.choice(GREETINGS)

        try:
            # Send welcome message to the specified channel
            welcome_channel = bot.get_channel(COMMUNITY_HALL_CHANNEL_ID)
            if welcome_channel:
                await welcome_channel.send(selected_greeting.replace("{member.mention}", after.mention))
        except Exception as e:
        # Log the error in the specified error channel
            error_channel = bot.get_channel(ERROR_CHANNEL_ID)
            if error_channel:
                await error_channel.send(f'Error in community_channel_message: {e}')

# Start the bot
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("DISCORD_TOKEN not found in .env file.")