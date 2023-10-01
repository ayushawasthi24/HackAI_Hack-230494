import os
import uuid
import requests
from dotenv import load_dotenv
from messages import WeatherRequest, UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low

load_dotenv()

WEATHER_SEED = os.getenv("WEATHER_SEED", "weather service secret phrase")

agent = Agent(name="weather_agent", seed=WEATHER_SEED)

fund_agent_if_low(agent.wallet.address())

OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "")

assert (
    OPENWEATHERMAP_API_KEY
), "OPENWEATHERMAP_API_KEY environment variable is missing from .env"

OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/weather?"


def get_current_weather(lat: float, lon: float):
    response = requests.get(
        url=OPENWEATHERMAP_API_URL
        + f"lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}",
        timeout=5,
    )
    if response.status_code == 200:
        return response.json()
    return []


weather_protocol = Protocol("Weather")


@weather_protocol.on_message(model=WeatherRequest, replies=UAgentResponse)
async def weather(ctx: Context, sender: str, msg: WeatherRequest):
    # ctx.logger.info(f"Received Message from sender {sender}")
    try:
        weather = get_current_weather(msg.latitude, msg.longitude)
        request_id = str(uuid.uuid4())
        temperature = weather["main"]["temp"] - 273
        await ctx.send(
            sender,
            UAgentResponse(
                temperature=temperature,
                type=UAgentResponseType.TEMPERATURE,
                request_id=request_id,
            ),
        )

    except Exception as exc:
        ctx.logger.error(exc)
        await ctx.send(sender, UAgentResponseType.ERROR)


agent.include(weather_protocol)
