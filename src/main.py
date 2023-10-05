# Import necessary modules
from agents.weather.weather import agent as weather_agent
from agents.user.users import agent as user_agent
from uagents import Bureau

if __name__ == "__main__":
    # Create a Bureau instance with the specified endpoint and port
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)

    # Add the weather agent to the bureau
    print(f"Adding weather agent to bureau: {weather_agent.address}")
    bureau.add(weather_agent)

    # Add the user agent to the bureau
    print(f"Adding user agent to bureau: {user_agent.address}")
    bureau.add(user_agent)

    # Run the bureau, which will manage the agents
    bureau.run()
