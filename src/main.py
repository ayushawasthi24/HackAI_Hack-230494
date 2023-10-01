from agents.weather.weather import agent as weather_agent
from agents.user.users import agent as user_agent
from uagents import Bureau

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    print(f"Adding weather agent to bureau: {weather_agent.address}")
    bureau.add(weather_agent)
    print(f"Adding user agent to bureau: {user_agent.address}")
    bureau.add(user_agent)
    bureau.run()
