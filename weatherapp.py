import tkinter as tk
import requests

#define weather app class

class WeatherApp:
    def __init__(self, root):
        
        # set up weather app canvas (aka root window)
        self.root = root
        self.root.geometry("600x500")
        self.root.title("Weather App")
        self.name = ""

        # call intro method to set up personalized UI 
        
        self.set_up_intro()
        
    def set_up_intro(self):

        #create intro frame
        self.intro_frame = tk.Frame(self.root)
        self.intro_frame.pack()

        #label asking for user name
        self.user_entry_label = tk.Label(master=self.intro_frame, text="Hello, welcome to your Personal Weather App.\n Enter a location or zipcode below:")
        self.user_entry_label.pack()

        #text box for user to enter name 
        self.user_entry = tk.Entry(self.intro_frame)
        self.user_entry.focus_set()
        self.user_entry.pack(pady=20)

        #create button for user to apply changes (hit enter) 

        button_frame = tk.Frame(self.intro_frame)
        self.button = tk.Button(button_frame, text="Enter")
        self.button.pack(side=tk.RIGHT)
        button_frame.pack()

        #verify if location is real or not
        self.user_entry.delete(0, tk.END)
        self.button.configure(command=self.verify_weather)

    def verify_weather(self):

        #retrieve user input for location
        location = self.user_entry.get()

        #access location's forcast by requesting info through weather api
        api = f"http://api.weatherapi.com/v1/forecast.json?key=d03d7e34fb96427e8d924739231308&q={location}&days=1&aqi=no"

        #store information as json file
        json_data = requests.get(api).json()
        self.user_entry.delete(0, tk.END)

        #check for http request error and repeat request for location until location is verified

        if json_data.get('error'):
            
            #throw out the error message through entry label
            self.user_entry_label.config(text=f"{location} is not a valid location. Please enter another location.")
        else:

            # store the location found in the json file generated as an attribute for later access
            self.location = json_data["location"]["name"] + ", " + json_data["location"]["region"] + ", " + json_data["location"]["country"]

            self.user_entry_label.config(text=f"Location successfully found!\n Here is the weather for {self.location}:")
            
            #store the json data as an instance for later parsing
            self.json_data = json_data

            self.user_entry.destroy()

            self.button.configure(text="Get Weather Report")
            
            self.button.configure(command=self.parse_json)

    def parse_json(self):
        # JSON parsing

        # Create a frame for weather information
        self.weather_info_frame = tk.Frame(self.root)
        self.weather_info_frame.pack()

        # retrieve what time it is currently
        self.current_time = self.json_data["location"]["localtime"]
        
        #retrieve what is the current temp
        self.current_temp = self.json_data["current"]["temp_f"]

        #retrieve what is the current condition
        self.current_condition = self.json_data["current"]["condition"]["text"]

        # display the info
        self.display_info()


    def display_info(self):

        # print all the parsed info
        self.title = tk.Label(master=self.weather_info_frame, text=f"{self.location} as of {self.current_time}")
        self.title.pack()
        self.temp = tk.Label(master=self.weather_info_frame, text=f"{self.current_temp}")
        self.temp.pack()
        self.condition = tk.Label(master=self.weather_info_frame, text=f"{self.current_condition}")
        self.condition.pack()


        # Create a frame for next actions
        self.next_actions_frame = tk.Frame(self.root)
        self.next_actions_frame.pack()

        #ask the user for next action
        self.next_action()

        
    def next_action(self):
        
        #ask the user if they want the weather for another location
        self.next_title = tk.Label(master=self.next_actions_frame, text="Want the weather for another location?")
        self.next_title.pack()

        #if user clicks yes, will reset the window
        self.next_action_button = tk.Button(self.next_actions_frame, text="Yes!")
        self.next_action_button.pack()
        self.next_action_button.configure(command=self.reset)

    def reset(self):

        #resets existing frames and takes user back to intro frame
        self.intro_frame.destroy()
        self.weather_info_frame.destroy()
        self.next_actions_frame.destroy()
        self.set_up_intro()
        
        
def main():

    #create root window
    root = tk.Tk()

    #create instance of weather app class
    app = WeatherApp(root)

    #main loop
    root.mainloop()

if __name__ == "__main__":
    main()
