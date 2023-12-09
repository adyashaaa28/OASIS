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
        self.root.geometry("600x500")  
        
      
        self.root.configure(bg="#fff8dc")
        self.label = ttk.Label(root, text="Voice Assistant App", font=("Helvetica", 24, "bold"), foreground="blue4", background="#fff8dc")
        self.label.pack(pady=15)

       
        self.additional_label = ttk.Label(root, text="Adyasha's Voice Assistant App", font=("Helvetica", 18, "italic"), foreground="green4", background="#fff8dc")
        self.additional_label.pack(pady=10)

       
        self.microphone_button = ttk.Button(root, text="Microphone On", command=self.toggle_microphone, style="TButton")
        self.microphone_button.pack(pady=10)

        
        self.clear_button = ttk.Button(root, text="Clear", command=self.clear_text, style="TButton")
        self.clear_button.pack(pady=10)

       
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, font=("Helvetica", 12), background="#f0e68c")
        self.text_area.pack(pady=10)

        
        self.microphone_on = False

    def toggle_microphone(self):
        self.microphone_on = not self.microphone_on

        if self.microphone_on:
            self.microphone_button.config(text="Microphone Off")
            self.listen_command()
        else:
            self.microphone_button.config(text="Microphone On")

    def listen_command(self):
       
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
          
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)

           
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
      
        self.label.config(text=response, foreground="green4")

       
        self.text_area.insert(tk.END, f"{response}\n")
        self.text_area.see(tk.END) 

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
       
        api_key = "YOUR_API_KEY"  
        endpoint = "https://api.weatherapi.com/v1/current.json"
        city = "New York"  
        params = {"key": api_key, "q": city}
        response = requests.get(endpoint, params=params)
        data = response.json()

      
        try:
            temperature = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            weather_message = f"The current weather in {city} is {temperature}°C with {condition}."
            self.respond(weather_message)
        except KeyError:
            self.respond("Unable to fetch weather information.")

    def set_reminder(self, command):
       
        reminder_text = command.replace("reminder", "").strip()
        current_time = self.get_current_time()

        
        reminder_message = f"Reminder set for {current_time}: {reminder_text}"
        self.respond(reminder_message)

    def clear_text(self):
        
        self.text_area.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
