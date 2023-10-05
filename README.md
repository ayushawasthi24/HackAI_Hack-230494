# 🌦️ Alertify

## Overview

This Weather Alert Application is a Python project that allows users to input their location and set maximum and minimum temperature thresholds. The application then retrieves the current temperature at the user's location using the OpenWeatherMap API and compares it to the specified thresholds. If the temperature falls outside the specified range, the user receives an alert. ⚠️

## Description

This app uses [uAgents](https://docs.fetch.ai/uAgents/) library to build agents for all kinds of decentralised use cases. In this app we have created two agents namely "weather_agent" and "user_agent" (in the `src/agents` directory). 

- The "weather_agent" primarily focusses on getting the weather information of the location by using the OpenWeatherMap API. It uses the on_message protocol in such a way that whenever the user agent messages this weather agent with the location information (basically latitude and longitude), it fetches the weather data and responds to the user agent.

- The "user_agent" has the tasks that pertain to the user management, like asking the user for the required inputs and sending the data to the weather agent. It also takes location input in the form of a string and fetches the latitudes and longitudes of the location by using the "Geoapify API".

- The "messages" folder contains the data models that are used in this project. They are WeatherRequest Model, UAgentResponseType Model and UAgentResponse Model.

- The data inputs by the user is stored in the storage of the user_agent by using the storage functions of the uAgents library.

## Prerequisites

Before running this application, you need to perform the following steps:

1. **Cloning the Project:**

   - Clone this repository using the following commands:
   ```
   git clone https://github.com/ayushawasthi24/alertify
   cd alertify
   ```

1. **Get API Keys:**

   - Obtain API keys for the OpenWeatherMap and Geoapify APIs. You can sign up for free developer accounts on their respective websites:
     - [OpenWeatherMap](https://openweathermap.org/api)
     - [Geoapify](https://www.geoapify.com/)

2. **Create a .env file:**
   - Navigate to the "src" folder:
   ```
   cd src
   ```

   - Create a `.env` file in the "src" folder of the project directory to store your API keys. The file should look like this:

   ```
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
   GEOAPIFY_API_KEY=your_geoapify_api_key
   ```

3. **Install Dependencies:**

   - Ensure you have [Poetry](https://python-poetry.org/) installed. Poetry is used to manage dependencies and virtual environments.
   - Use Poetry to install project dependencies. Run the following command in the project directory:

   ```
   poetry install
   ```

4. **Activate the Virtual Environment:**

   - Activate the virtual environment using Poetry. Run the following command in the project directory:

   ```
   poetry shell
   ```

5. **Run the Application:**
   - After activating the virtual environment, you can run the main application script using the following command:
   ```
   python main.py
   ```

## Usage

1. When you run the application, it will prompt you to enter your location. 🌍

2. Next, you will be asked to set the maximum and minimum temperature thresholds. ☀️❄️

3. The application will then retrieve the current temperature at your location using the OpenWeatherMap API and check if it falls outside the specified range.

4. If the temperature is higher or lower than the specified thresholds, you will receive an alert. 🚨

5. You can exit the application by pressing Ctrl+C on your keyboard. 📴

Enjoy using this Alertify app!! ☔🌈🌞
