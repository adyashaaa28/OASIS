import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import speech_recognition as sr
from datetime import datetime
import webbrowser
import requests

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adyasha's Voice Assistant App")
        self.root.geometry("600x500")  # Set a larger size for the window

        # Set a pastel yellow background
        self.root.configure(bg="#fff8dc")

        # Create and pack the main heading label
        self.label = ttk.Label(root, text="Voice Assistant App", font=("Helvetica", 24, "bold"), foreground="blue4", background="#fff8dc")
        self.label.pack(pady=15)

        # Create and pack the additional heading label
        self.additional_label = ttk.Label(root, text="Adyasha's Voice Assistant App", font=("Helvetica", 18, "italic"), foreground="green4", background="#fff8dc")
        self.additional_label.pack(pady=10)

        # Create and pack the microphone on/off button with "TButton" style
        self.microphone_button = ttk.Button(root, text="Microphone On", command=self.toggle_microphone, style="TButton")
        self.microphone_button.pack(pady=10)

        # Create and pack the clear button with "TButton" style
        self.clear_button = ttk.Button(root, text="Clear", command=self.clear_text, style="TButton")
        self.clear_button.pack(pady=10)

        # Create the scrolled text widget
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, font=("Helvetica", 12), background="#f0e68c")
        self.text_area.pack(pady=10)

        # Initialize microphone state
        self.microphone_on = False

    def toggle_microphone(self):
        self.microphone_on = not self.microphone_on

        if self.microphone_on:
            self.microphone_button.config(text="Microphone Off")
            self.listen_command()
        else:
            self.microphone_button.config(text="Microphone On")

    def listen_command(self):
        # Initialize the recognizer
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            # Use Google Web Speech API to recognize speech
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)

            # Process the command and update the text area
            self.process_command(command)

        except sr.UnknownValueError:
            print("Could not understand audio")

    def process_command(self, command):
        if "hello" in command:
            self.respond("Hello! How can I assist you today?")
        elif "time" in command:
            self.respond("The current time is " + self.get_current_time())
        elif "date" in command:
            self.respond("Today's date is " + self.get_current_date())
        elif "search" in command:
            query = command.replace("search", "").strip()
            self.search_web(query)
        elif "weather" in command:
            self.get_weather()
        elif "reminder" in command:
            self.set_reminder(command)
        else:
            self.respond("I'm sorry, I didn't understand that.")

    def respond(self, response):
        # Update the main heading label with the response
        self.label.config(text=response, foreground="green4")

        # Append the response to the text area
        self.text_area.insert(tk.END, f"{response}\n")
        self.text_area.see(tk.END)  # Scroll to the end

    def get_current_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def get_current_date(self):
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        return current_date

    def search_web(self, query):
        url = "https://www.google.com/search?q=" + query
        webbrowser.open(url)

    def get_weather(self):
        # Get weather information using a sample API (replace with a real API key and endpoint)
        api_key = "YOUR_API_KEY"  # Replace with a real API key
        endpoint = "https://api.weatherapi.com/v1/current.json"
        city = "New York"  # Replace with the desired city

        params = {"key": api_key, "q": city}
        response = requests.get(endpoint, params=params)
        data = response.json()

        # Parse and display weather information
        try:
            temperature = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            weather_message = f"The current weather in {city} is {temperature}°C with {condition}."
            self.respond(weather_message)
        except KeyError:
            self.respond("Unable to fetch weather information.")

    def set_reminder(self, command):
        # Extract reminder details from the command
        reminder_text = command.replace("reminder", "").strip()
        current_time = self.get_current_time()

        # Display the reminder message
        reminder_message = f"Reminder set for {current_time}: {reminder_text}"
        self.respond(reminder_message)

    def clear_text(self):
        # Clear the text area
        self.text_area.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
