# Import necessary modules
import os
import uuid
import requests
from dotenv import load_dotenv
from messages import WeatherRequest, UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low

# Load environment variables from .env file
load_dotenv()

# Get the WEATHER_SEED from environment or use a default value
WEATHER_SEED = os.getenv("WEATHER_SEED", "weather service secret phrase")

# Initialize an Agent with a name and seed
agent = Agent(name="weather_agent", seed=WEATHER_SEED)

# Fund the agent's wallet if it's low on funds
fund_agent_if_low(agent.wallet.address())

# Get the OPENWEATHERMAP_API_KEY from environment
OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "")

# Ensure that OPENWEATHERMAP_API_KEY is provided
assert (
    OPENWEATHERMAP_API_KEY
), "OPENWEATHERMAP_API_KEY environment variable is missing from .env"

# Define the OpenWeatherMap API URL
OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/weather?"


# Function to get current weather based on latitude and longitude
def get_current_weather(lat: float, lon: float):
    response = requests.get(
        url=OPENWEATHERMAP_API_URL
        + f"lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}",
        timeout=5,
    )
    if response.status_code == 200:
        return response.json()
    return []


# Define a custom protocol for defining handlers
weather_protocol = Protocol("Weather")


# Define a message handler for weather requests
@weather_protocol.on_message(model=WeatherRequest, replies=UAgentResponse)
async def weather(ctx: Context, sender: str, msg: WeatherRequest):
    # ctx.logger.info(f"Received Message from sender {sender}")
    try:
        # Get current weather data
        weather = get_current_weather(msg.latitude, msg.longitude)
        request_id = str(uuid.uuid4())
        temperature = weather["main"]["temp"] - 273  # Convert temperature to Celsius
        message = weather["weather"][0]["main"]
        await ctx.send(
            sender,
            UAgentResponse(
                temperature=temperature,
                message=message,
                type=UAgentResponseType.TEMPERATURE,
                request_id=request_id,
            ),
        )

    except Exception as exc:
        ctx.logger.error(exc)
        await ctx.send(sender, UAgentResponseType.ERROR)


# Include the weather protocol in the agent
agent.include(weather_protocol)
