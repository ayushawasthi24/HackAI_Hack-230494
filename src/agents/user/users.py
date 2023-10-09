# Import necessary modules
import os
import uuid
import requests
from dotenv import load_dotenv
from uagents import Agent, Context, Protocol
from messages import UAgentResponse, WeatherRequest
from agents.weather.weather import agent as weather_agent
from uagents.setup import fund_agent_if_low
from pyfiglet import figlet_format
from colorama import Fore, Style

# Load environment variables from .env file
load_dotenv()

# Get the USER_SEED from environment or use a default value
USER_SEED = os.getenv("USER_SEED", "user agent secret phrase")

# Initialize a user agent with a name and seed
agent = Agent(name="user_agent", seed=USER_SEED)

# Define a custom protocol for user-related messages
user_protocol = Protocol("User")

# Fund the user agent's wallet if it's low on funds
fund_agent_if_low(agent.wallet.address())

# Get the GEOAPIFY_API_KEY from environment
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY", "")

# Ensure that GEOAPIFY_API_KEY is provided
assert GEOAPIFY_API_KEY, "GEOAPIFY_API_KEY environment variable is missing from .env"

# Define the Geoapify API URL
GEOAPIFY_URL = "https://api.geoapify.com/v1/geocode/search?text="

# Get the address of the weather agent
weather_agent_address = weather_agent.address

# Create a stylized title for the application
title = figlet_format("Welcome to MystiWeather", font="standard")


# Function to get latitude and longitude coordinates for a given city
def get_lat_lon(city_name: str):
    city_name = city_name.replace(" ", "%20")
    try:
        response = requests.get(
            url=f"{GEOAPIFY_URL}{city_name}&format=json&apiKey={GEOAPIFY_API_KEY}"
        ).json()
        latitude = response["results"][0]["lat"]
        longitude = response["results"][0]["lon"]
        return (latitude, longitude)
    except Exception as exc:
        print("Error: " + str(exc))
        return ()


# Define a startup event handler for the user agent
@agent.on_event("startup")
async def start(ctx: Context):
    print(Fore.BLUE + title + Style.RESET_ALL)
    location = input("Kindly reveal your mystical whereabouts: (Enter your location:) ")
    max_temp = float(
        input("Enter the maximum temperature for mystical alerts (in degree celsius) ")
    )
    min_temp = float(
        input("Enter the minimum temperature for mystical alerts (in degree celsius) ")
    )
    ctx.storage.set("location", location)
    ctx.storage.set("max_temp", max_temp)
    ctx.storage.set("min_temp", min_temp)


# Define an interval-based message handler to request weather information periodically
@user_protocol.on_interval(period=20)
async def get_temp(ctx: Context):
    (lat, lon) = get_lat_lon(ctx.storage.get("location"))
    await ctx.send(weather_agent_address, WeatherRequest(latitude=lat, longitude=lon))


# Define a message handler for receiving temperature alerts
@user_protocol.on_message(model=UAgentResponse)
async def alert(ctx: Context, sender: str, msg: UAgentResponse):
    if msg.message == "Rain":
        ctx.logger.info(
            "The sky weeps, enchanting raindrops dance, for the elves rejoice. (Rainfall predicted)"
        )
    elif msg.message == "Snow":
        ctx.logger.info(
            "A white blanket descends, as if the witches have cast their icy spell. (Snow predicted)"
        )
    elif msg.message == "Clouds":
        ctx.logger.info(
            "Mystical clouds gather, concealing secrets only the forest spirits know. (Cloudy weather)"
        )
    elif msg.message == "Drizzle":
        ctx.logger.info(
            "Soft drizzle, like faerie kisses, graces your mystical land. (Drizzle)"
        )
    elif msg.message == "Thunderstorm":
        ctx.logger.info(
            "Thunderous roar, a clash of titans, the storm giants awaken! (Thunderstorm)"
        )
    elif msg.message == "Clear":
        ctx.logger.info(
            "The realm basks in crystal clarity, as if gnomes polished the skies. (Clear weather)"
        )
    elif msg.message == "Atmosphere":
        ctx.logger.info(
            "The mystical atmosphere stirs with unseen energies, the creatures of the unseen realm are afoot. (Atmosphere)"
        )

    if msg.temperature < ctx.storage.get("min_temp"):
        ctx.logger.info("Alert!!!!!")
        ctx.logger.info(
            f'Behold!!! The temperature in your realm {ctx.storage.get("location")} has descended below {ctx.storage.get("min_temp")}. The current temperature is {round(msg.temperature, 2)} degrees celsius.'
        )
    elif msg.temperature > ctx.storage.get("max_temp"):
        ctx.logger.info("Alert!!!!!")
        ctx.logger.info(
            f'Behold!!! The temperature in your realm {ctx.storage.get("location")} has ascended above {ctx.storage.get("max_temp")}. The current temperature is {round(msg.temperature, 2)} degrees celsius.'
        )
    else:
        ctx.logger.info(
            "Thankfully, the temperature in your realm holds steady within the ordained limits you entered."
        )


# Include the user protocol in the user agent
agent.include(user_protocol)
