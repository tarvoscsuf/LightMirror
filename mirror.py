import tkinter as tk
import time
import requests
import json
import openai

# Backdrop, main window
window = tk.Tk()
window.configure(bg='black')  # Set the window background color to black
window.attributes('-fullscreen', True)  # Set the window to fullscreen

# Time label
time_label = tk.Label(window, font=('Tahoma Bold', 100, 'bold'), fg='white', bg='black')
time_label.pack(expand=True)

# Weather label
weather_label = tk.Label(window, font=('Tahoma', 48), fg='white', bg='black')
weather_label.pack(expand=True)

# Greetings label
greetings_label = tk.Label(window, font=('Tahoma', 36), fg='white', bg='black')
greetings_label.pack(side=tk.TOP)  # Changed side parameter

# RSS feed label
news_label = tk.Label(window, font=('Tahoma', 36), fg='white', bg='black')
news_label.pack(side=tk.BOTTOM, pady=40)

# New York Times RSS API URL
rss_url = "KEY"

# OpenWeatherMap API
weather_key = "KEY"

# OpenAI Token
openai.api_key = "KEY"

# Time updater
def update_time():
    # Get the current time
    current_time = time.strftime('%H:%M:%S')
    time_label.config(text=current_time)

    # Schedule the next time update after 1 second (1000 milliseconds)
    window.after(1000, update_time)

# Weather updater
def update_weather():
    try:
        # Get the local weather from OpenWeatherMap API
        # Enter your city name and country code below
        city = "CITY"
        country_code = "US"

        # Send a request to OpenWeatherMap API with units=imperial for Fahrenheit
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={weather_key}&units=imperial"
        response = requests.get(url)
        data = json.loads(response.text)

        # Extract relevant weather information
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]

        # Update the weather label
        weather_text = f"feels like {temperature}°F\nlooks like {weather_description}"
        weather_label.config(text=weather_text)
    except Exception as e:
        print("Error:", str(e))
        weather_label.config(text="Failed to fetch weather data.")

    # Schedule the next weather update after 30 minutes (1800000 milliseconds)
    window.after(1800000, update_weather)

# Greetings updater
def update_greeting():
    try:
        # Get the current time
        current_time = time.strftime('%H:%M:%S')
	# Generate OpenAI response
        openai_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"tell me a greeting, it is currently {current_time} o'clock",
            max_tokens=100,
            temperature=0.5,
        )
	# Format and display greeting
        greeting_text = openai_response.choices[0].text.strip()
        greetings_label.config(text=greeting_text)
    except Exception as e:
        print("Error:", str(e))
        greetings_label.config(text="Failed to generate greeting.")

    # Schedule the next greetings update after 30 seconds (30000 milliseconds)
    window.after(30000, update_greeting)

# RSS updater
def update_news():
    try:
        # Fetch the news headlines from the New York Times RSS API
        response = requests.get(rss_url)
        data = response.text

        # Parse the XML data
        from xml.etree import ElementTree as ET
        root = ET.fromstring(data)

        # Extract the headlines from the XML
        headlines = [item.find("title").text for item in root.iter("item")]

        # Update the news label with the next headline
        if hasattr(update_news, 'headline_index'):
            update_news.headline_index += 1
        else:
            update_news.headline_index = 0
        if update_news.headline_index >= len(headlines):
            update_news.headline_index = 0

        news_label.config(text=headlines[update_news.headline_index])
    except Exception as e:
        print("Error:", str(e))
        news_label.config(text="Failed to fetch news headlines.")

    # Schedule the next news update after 30 seconds (30000 milliseconds)
    window.after(30000, update_news)

# Function calls
update_time()
update_weather()
update_greeting()
update_news()

# Main
window.mainloop()
