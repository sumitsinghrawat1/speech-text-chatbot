import speech_recognition as sr
import pyttsx3
import os
import geocoder
import googlemaps
import time
from datetime import datetime, timedelta
import requests
import tkinter as tk
from tkinter import scrolledtext
import threading
import random
import cv2
import pytesseract
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from googletrans import Translator
import speech_recognition as sr
import pickle
import pyautogui
import pyautogui
import pygetwindow as gw
import pyautogui
import time
import pygetwindow as gw

# Define the zodiac signs
zodiac_signs = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra",
    "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]


# Set up Google Maps API client
gmaps = googlemaps.Client(key="AIzaSyDcbQkrJh5RhACoM2ulmP6-zGNKmCKBFaQ")

# TTS setup
engine = pyttsx3.init()
tts_lock = threading.Lock()


# News API Key (Replace with your API key)
NEWS_API_KEY = "763ebdfd1bd54bb5afc77c3198d8e82a"
browser_instance = None

# Twilio credentials (replace with your details)
TWILIO_ACCOUNT_SID = "AC006af86987ed667a188818ea79e555f6"
TWILIO_AUTH_TOKEN = "34321f1e4baa655765c57a3ede7a5de5"
TWILIO_PHONE_NUMBER = "+91 7818023591"

# Emergency contact
EMERGENCY_CONTACT_NUMBER = "+91 82738056703"



# GUI setup
root = tk.Tk()
root.title("Voice Assistant for Visually Impaired")
root.geometry("600x400")
root.configure(bg="lightblue")



# Set up the output display
output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=("Arial", 12))
output_display.grid(row=0, column=0, padx=10, pady=10)

# Function to insert AI's response (left side)
def display_assistant_message(text):
    output_display.insert(tk.END, f"AI: {text}\n")
    output_display.see(tk.END)

# Function to insert User's message (right side)
def display_user_message(text):
    output_display.insert(tk.END, f"You: {text}\n")
    output_display.see(tk.END)

# TTS engine setup
engine = pyttsx3.init()
tts_lock = threading.Lock()  # Lock to prevent concurrent TTS execution

def display_and_speak(text):
    """Display the response in the GUI and speak it."""
    display_assistant_message(text)
    with tts_lock:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in TTS: {e}")



def start_whatsapp_video_call(contact_name):
    """Start a video call on WhatsApp Desktop by simulating keyboard/mouse actions."""
    try:
        # Find the WhatsApp Desktop window
        whatsapp_window = gw.getWindowsWithTitle('WhatsApp')[0]
        whatsapp_window.activate()
        time.sleep(2)  # Wait for the WhatsApp window to become active

        # Open the search bar and type the contact's name
        pyautogui.hotkey('ctrl', 'f')  # Open the search bar (Ctrl + F)
        time.sleep(1)
        pyautogui.write(contact_name)
        pyautogui.press('enter')
        time.sleep(2)  # Wait for the contact to be selected

        # Click the video call button (use the tab key and space bar to activate the button)
        pyautogui.hotkey('tab')  # Focus on the chat interface
        pyautogui.press('enter')
        pyautogui.click(1793, 80)  # Coordinates for video call button
        pyautogui.sleep(1)
        display_and_speak(f"Initiating video call with {contact_name}.")
    except Exception as e:
        display_and_speak(f"Error starting video call: {e}")


def start_whatsapp_voice_call(contact_name):
    """Start a voice call on WhatsApp Desktop by simulating keyboard/mouse actions."""
    try:
        # Find the WhatsApp Desktop window
        whatsapp_window = gw.getWindowsWithTitle('WhatsApp')[0]
        whatsapp_window.activate()
        time.sleep(2)  # Wait for the WhatsApp window to become active

        # Open the search bar and type the contact's name
        pyautogui.hotkey('ctrl', 'f')  # Open the search bar (Ctrl + F)
        time.sleep(1)
        pyautogui.write(contact_name)
        pyautogui.press('enter')
        time.sleep(2)  # Wait for the contact to be selected

        # Click the voice call button (coordinates should match your screen resolution)
        pyautogui.hotkey('tab')  # Focus on the chat interface
        pyautogui.press('enter')
        pyautogui.click(1848, 80)  # Coordinates for voice call button
        pyautogui.sleep(1)

        display_and_speak(f"Initiating voice call with {contact_name}.")
    except Exception as e:
        display_and_speak(f"Error starting voice call: {e}")



def get_current_location():
    """Fetch the current location using geocoder."""
    g = geocoder.ip('me')  # This gets the location based on IP (works well for virtual environments)
    return g.latlng  # Returns latitude and longitude




def get_directions(start, end):
    """Fetch directions from Google Maps."""
    try:
        directions_result = gmaps.directions(start, end, mode="walking")  # Change to "driving" if needed
        if directions_result:
            steps = directions_result[0]['legs'][0]['steps']
            directions = []
            for step in steps:
                directions.append(step['html_instructions'])
            return "\n".join(directions)
        else:
            return "Sorry, I couldn't find any directions."
    except Exception as e:
        return f"Error fetching directions: {e}"
def get_horoscope(sign):
    """Fetch daily horoscope based on the user's zodiac sign."""
    URL = f"https://aztro.sameerkumar.website?sign={sign}&day=today"
    try:
        response = requests.post(URL)
        data = response.json()
        horoscope = data['description']
        return horoscope
    except Exception as e:
        return f"Sorry, I couldn't fetch the horoscope right now. {e}"
def navigate_to_destination(destination):
    """Navigate to the given destination from current location."""
    current_location = get_current_location()
    if current_location:
        display_and_speak(f"Fetching directions to {destination} from your current location.")
        directions = get_directions(current_location, destination)
        display_and_speak(f"Directions: {directions}")
    else:
        display_and_speak("Could not determine your current location.")

def process_command(command):
    """Process the spoken command."""
    if "navigate to" in command:
        destination = command.replace("navigate to", "").strip()
        display_and_speak(f"Navigating to {destination}.")
        navigate_to_destination(destination)
        return f"Navigating to {destination}."
    # Other commands...
    else:
        return f"You said: {command}"

def send_sos_sms(message):
    """Send an emergency SOS SMS using Twilio."""
    try:
        # Initialize Twilio Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Send SMS
        sms = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=EMERGENCY_CONTACT_NUMBER
        )

        print(f"Emergency SOS SMS sent successfully! Message SID: {sms.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        


def display_and_speak(text):
    """Display the response in the GUI and speak it."""
    output_display.insert(tk.END, f"{text}\n")
    output_display.see(tk.END)
    with tts_lock:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in TTS: {e}")
            
def start_greeting(task_name):
    display_and_speak(f"Let's get started with {task_name}!")
    
def end_greeting(task_name):
    display_and_speak(f"Task '{task_name}' is completed. Anything else I can help with?")

def get_times_of_india_news():
    """Fetch the latest news from Times of India."""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        url = (
            f"https://newsapi.org/v2/everything?"
            f"sources=the-times-of-india&from={yesterday}&to={today}&apiKey={NEWS_API_KEY}&sortBy=publishedAt"
        )
        response = requests.get(url)
        news_data = response.json()
        if news_data["status"] == "ok":
            articles = news_data["articles"][:5]
            if not articles:
                return "No recent news from Times of India is available right now."
            news_list = [f"{i+1}. {article['title']} - {article['publishedAt']}" for i, article in enumerate(articles)]
            return "Here are the latest headlines from Times of India:\n" + "\n".join(news_list)
        else:
            return "Sorry, I couldn't fetch the latest news from Times of India."
    except Exception as e:
        return f"Error fetching news: {e}"

def play_music_automatically(song_name):
    """Play a song automatically on YouTube."""
    global browser_instance
    try:
        # Automatically download and manage ChromeDriver
        service = Service(ChromeDriverManager().install())
        browser_instance = webdriver.Chrome(service=service)
        
        browser_instance.get("https://www.youtube.com")
        search_box = browser_instance.find_element("name", "search_query")
        search_box.send_keys(song_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        video = browser_instance.find_elements("id", "video-title")[0]
        video.click()
        display_and_speak(f"Playing {song_name} on YouTube.")
    except Exception as e:
        display_and_speak(f"Error playing music: {e}")

def close_browser():
    """Close the browser if it is open."""
    global browser_instance
    if browser_instance:
        try:
            browser_instance.quit()
            browser_instance = None
            display_and_speak("Browser closed successfully.")
        except Exception as e:
            display_and_speak(f"Error closing the browser: {e}")
    else:
        display_and_speak("No browser is currently open.")
        
        
def detect_faces():
    """Perform real-time face detection using the webcam."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    display_and_speak("Starting face detection. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('Face Detection - Press "q" to Exit', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    display_and_speak("Face detection stopped.")

def detect_objects():
    """Perform real-time object detection using edge detection."""
    cap = cv2.VideoCapture(0)
    display_and_speak("Starting object detection. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_frame, 100, 200)
        cv2.imshow('Object Detection - Press "q" to Exit', edges)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    display_and_speak("Object detection stopped.")
    
def predefined_weather(city_name):
    """
    Returns predefined weather details for a given city.
    """
    # Dictionary of predefined weather data
    weather_data = {
        "Dehradun": {
            "description": "Sunny",
            "temp": 18,
            "humidity": 56 ,
            "wind_speed": 5
        },
        "Delhi": {
            "description": "sunny",
            "temp": 22,
            "humidity": 63,
            "wind_speed": 3
        },
        "Chandigarh": {
            "description": "sunny",
            "temp": 20,
            "humidity": 50,
            "wind_speed":3
        }
    }
    
    city_name_lower = city_name.lower()
    if city_name_lower in weather_data:
        weather = weather_data[city_name_lower]
        return (f"Weather in {city_name.capitalize()}:\n"
                f"- {weather['description']}\n"
                f"- Temperature: {weather['temp']}°C\n"
                f"- Humidity: {weather['humidity']}%\n"
                f"- Wind Speed: {weather['wind_speed']} m/s")
    else:
        return f"Sorry, I don't have weather data for {city_name.capitalize()}."
    
def get_motivational_quote():
        quotes = [
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Act as if what you do makes a difference. It does. - William James",
            "To live is the rarest thing in the world. Most people exist, that is all. - Oscar Wilde",
            "That it will never come again is what makes life so sweet.' – Emily Dickinson",
            "It is never too late to be what you might have been.' – George Eliot",
            "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.' – Ralph Waldo Emerson",
            "Start before you’re ready. - Steven Pressfield",
            "You must be the change you wish to see in the world. - Mahatma Gandhi",
            "Spread love everywhere you go. Let no one ever come to you without leaving happier. - Mother Teresa",
            "The only thing we have to fear is fear itself. - Franklin D. Roosevelt"
        ]
        return random.choice(quotes)
def get_horoscope(sign):
    """Fetch a predefined horoscope for a given zodiac sign."""
    horoscopes = {
        "aries": "Today is a great day to focus on your goals. Keep moving forward!",
        "taurus": "Take some time to enjoy the little things in life. Relax and recharge.",
        "gemini": "Your communication skills will shine today. Speak your mind confidently.",
        "cancer": "Emotional balance is key today. Trust your intuition in tough decisions.",
        "leo": "Your leadership skills will come in handy. Be bold and take the lead.",
        "virgo": "Organization is your superpower today. Tackle that to-do list!",
        "libra": "Seek harmony in your relationships. Compromise will bring you peace.",
        "scorpio": "Your determination will be rewarded. Stay focused on the bigger picture.",
        "sagittarius": "Adventure awaits! Step out of your comfort zone and explore.",
        "capricorn": "Hard work pays off. Stay dedicated and success will follow.",
        "aquarius": "Your creativity knows no bounds today. Let your ideas flow freely.",
        "pisces": "Embrace your compassionate side. Helping others will bring you joy.",
    }

    sign = sign.lower()
    return horoscopes.get(sign, "Sorry, I couldn't find the horoscope for that sign.")



def read_text_from_image():
    """Read text from an image using OCR."""
    display_and_speak("Please provide the path to the image file.")
    image_path = input("Enter the image path: ")
    try:
        img = cv2.imread(image_path)
        text = pytesseract.image_to_string(img)
        if text.strip():
            display_and_speak(f"Extracted text from image: {text}")
        else:
            display_and_speak("No readable text found in the image.")
    except Exception as e:
        display_and_speak(f"Error reading image: {e}")
        
def weather_command_predefined(user_input):
    """
    Handles user input and returns predefined weather details.
    """
    if "weather" in user_input.lower():
        words = user_input.lower().split()
        if "in" in words:
            city_index = words.index("in") + 1
            if city_index < len(words):
                city_name = " ".join(words[city_index:])
                return predefined_weather(city_name)
            else:
                return "Please specify the city after 'in'."
        else:
            return "Please specify the city using 'weather in [city name]'."
    return None



def process_command(command):
    """Process the spoken command."""
    if "navigate to" in command:
        destination = command.replace("navigate to", "").strip()
        display_and_speak(f"Navigating to {destination}.")
        navigate_to_destination(destination)
        return f"Navigating to {destination}."
    
    if "navigate to" in command:
        destination = command.replace("navigate to", "").strip()
        display_and_speak(f"Navigating to {destination}.")
        navigate_to_destination(destination)
        return f"Navigating to {destination}."
    if "time" in command:
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."
    if "horoscope" in command:
        # Split the command into words to find the zodiac sign
        words = command.split()
        for word in words:
            if word.lower() in [
                "aries", "taurus", "gemini", "cancer", "leo", "virgo",
                "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
            ]:
                horoscope = get_horoscope(word.lower())
                display_and_speak(horoscope)
                return horoscope
        # If no zodiac sign is found in the command
        return "Please specify a zodiac sign to get the horoscope."
    if "whatsapp video call" in command:
        contact_name = command.replace("whatsapp video call", "").strip()
        display_and_speak(f"Initiating WhatsApp video call with {contact_name}.")
        threading.Thread(target=start_whatsapp_video_call, args=(contact_name,), daemon=True).start()
        return f"Initiating WhatsApp video call with {contact_name}."
    
    elif "whatsapp voice call" in command:
        contact_name = command.replace("whatsapp voice call", "").strip()
        display_and_speak(f"Initiating WhatsApp voice call with {contact_name}.")
        threading.Thread(target=start_whatsapp_voice_call, args=(contact_name,), daemon=True).start()
        return f"Initiating WhatsApp voice call with {contact_name}."

    # Handle other commands
   
    
    
    elif "date" in command:
        return f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}."
    elif "joke" in command:
        jokes = [
            "Why don’t scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call fake spaghetti? An impasta!"
        ]
        return random.choice(jokes)
    elif "horoscope" in command:
        for sign in zodiac_signs:
            if sign in command:
                horoscope = get_horoscope(sign)
                return f"Today's horoscope for {sign.capitalize()} is: {horoscope}"
        return "Sorry, I couldn't find your zodiac sign. Please try again with a valid sign."
    elif "send emergency sos" in command:
        emergency_message = "🚨 Emergency Alert! Please help. I'm in urgent need of assistance."
        send_sos_sms(emergency_message)
        return "Emergency SOS sent to your contact."
    elif "current news" in command:
        return get_times_of_india_news()
    elif "play music" in command:
        song_name = command.replace("play music", "").strip()
        threading.Thread(target=play_music_automatically, args=(song_name,), daemon=True).start()
        return f"Searching for {song_name} on YouTube..."
    elif "close browser" in command:
        close_browser()
        return "Closing the browser."
    elif "face detection" in command:
        threading.Thread(target=detect_faces, daemon=True).start()
        return "Starting face detection."
    elif "object detection" in command:
        threading.Thread(target=detect_objects, daemon=True).start()
        return "Starting object detection."
    elif "motivational quote" in command:
        return get_motivational_quote()
    elif "read text from image" in command:
        threading.Thread(target=read_text_from_image, daemon=True).start()
        return "Reading text from the image."
    elif "exit" in command or "quit" in command:
        display_and_speak("Goodbye!")
        time.sleep(2)
        root.destroy()
    else:
        return f"You said: {command}"
        display_and_speak("Command not recognized.")
        return "Command not recognized."

# Unlock assistant with "Jack"
assistant_unlocked = False

def unlock_assistant():
    global assistant_unlocked
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        display_and_speak("Please say the password to unlock me.")
        while not assistant_unlocked:
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                if "jack" in command:
                    assistant_unlocked = True
                    display_and_speak("Access granted!\n"
                  "Hello! Shiwani Welcome to your AI-based Personal Assistant.\n"
                  "I'm here to help you with various tasks. How can I assist you today?")
                else:
                    display_and_speak("Incorrect password. Please try again.")
            except sr.UnknownValueError:
                display_and_speak("I didn't catch that. Could you repeat?")
            except Exception as e:
                display_and_speak(f"An error occurred: {e}")

def listen_and_respond():
    """Listen for commands and respond."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
            
                recognizer.adjust_for_ambient_noise(source, duration=1)
                display_and_speak("Listening for your command...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                response = process_command(command)
                display_and_speak(response)
            except sr.UnknownValueError:
                display_and_speak("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                display_and_speak(f"Error with speech recognition: {e}")

# Start threads for unlocking and listening
threading.Thread(target=unlock_assistant, daemon=True).start()
def wait_for_unlock():
    while not assistant_unlocked:
        time.sleep(1)
    threading.Thread(target=listen_and_respond, daemon=True).start()
threading.Thread(target=wait_for_unlock, daemon=True).start()

# Run the GUI
root.mainloop()

