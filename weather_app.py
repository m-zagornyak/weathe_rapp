import requests
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import threading
import time
import config  


def get_weather(city_name=config.DEFAULT_CITY):

    info_label.config(text="Loading", font=("Arial", 14, "bold"), fg="#000000")
    app.update()  

    time.sleep(3)  

    try:

        complete_url = f"{config.BASE_URL}q={city_name}&appid={config.API_KEY}&units=metric"
        response = requests.get(complete_url)
        data = response.json()

        if data.get("cod") != 404:

            main = data.get("main", {})
            wind = data.get("wind", {})
            weather_desc = data["weather"][0]["description"] if data["weather"] else "N/A"
            temp = main.get("temp", "N/A")
            pressure = main.get("pressure", "N/A")
            humidity = main.get("humidity", "N/A")
            wind_speed = wind.get("speed", "N/A")
            city = data.get("name", "N/A")
            country = data["sys"].get("country", "N/A")
            sunrise = datetime.fromtimestamp(data["sys"].get("sunrise", 0)).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(data["sys"].get("sunset", 0)).strftime('%H:%M:%S')


            city_entry.delete(0, tk.END) 
            city_entry.insert(0, city)  

            info_label.config(
                text=f"Місто: {city}, {country}\nТемпература: {temp}°C\n"
                     f"Погода: {weather_desc.capitalize()}\n"
                     f"Тиск: {pressure} hPa\nHumidity: {humidity}%\n"
                     f"Швидкість вітру: {wind_speed} m/s\nСвітанок: {sunrise}\nЗахід: {sunset}",
                font=("Arial", 12), fg=config.INFO_TEXT_COLOR  
            )


            search_button.config(state="normal", text="Search", image=search_icon, compound="left")
        else:

            info_label.config(text="Not Found. Please provide a valid city name.", fg="#000000", font=("Arial", 12, "bold"))
            search_button.config(state="normal", text="Search", image=search_icon, compound="left")
    except Exception as e:

        info_label.config(text="Provide a valid city name to get info", fg="#000000", font=("Arial", 12, "bold"))
        search_button.config(state="normal", text="Search", image=search_icon, compound="left")


def search_city():
    city_name = city_entry.get()  
    if city_name:
        search_button.config(state="disabled", text="Searching", image=None, fg="#FFFFFF")
        threading.Thread(target=get_weather, args=(city_name,)).start()
    else:

        info_label.config(text="Enter city name to get weather info", fg="#000000", font=("Arial", 12, "bold"))


def on_enter_press(event):
    search_city()


# def resize_bg(event):
#     new_bg = bg_image.resize((event.width, event.height), Image.LANCZOS)
#     bg_photo = ImageTk.PhotoImage(new_bg)
#     bg_label.config(image=bg_photo)
#     bg_label.image = bg_photo  


# def set_background(image_path):
#     try:
#         global bg_image
#         bg_image = Image.open(image_path)
#         bg_photo = ImageTk.PhotoImage(bg_image.resize((500, 400), Image.LANCZOS))
#         bg_label.config(image=bg_photo)
#         bg_label.image = bg_photo
#     except FileNotFoundError:
#         messagebox.showerror("Error", "Background image not found!")


def show_default_info():
    get_weather(config.DEFAULT_CITY)


app = tk.Tk()  
app.title("Weather Info") 
app.geometry("500x400")
app.iconbitmap("assets/weather.ico")


bg_label = tk.Label(app)
bg_label.place(relwidth=1, relheight=1)


# set_background(config.DEFAULT_BACKGROUND_IMAGE)


title_label = tk.Label(app, text="☂ Weather Info ☂", font=("Arial", config.HEADER_TOP_TEXT_SIZE, "bold"),
                       fg=config.HEADER_TOP_TEXT_COLOR, relief="solid", bd=config.HEADER_TEXT_TOP_BORDER_THICKNESS, padx=10, pady=5)
title_label.place(relx=0.5, rely=0.06, anchor="n")


city_entry = tk.Entry(app, font=("Arial", 14), width=30, bd=2, relief="solid", 
                      highlightbackground=config.SEARCH_BAR_BORDER_COLOR,
                      highlightcolor=config.SEARCH_BAR_BORDER_COLOR,
                      justify="center")
city_entry.place(relx=0.5, rely=0.2, anchor="n")
city_entry.insert(0, "Enter city name here")
city_entry.bind("<Return>", on_enter_press)

search_icon = ImageTk.PhotoImage(Image.open(config.SEARCH_ICON_IMAGE).resize((20, 20)))
search_button = tk.Button(app, text="Search", command=search_city, font=("Arial", 12, "bold"), image=search_icon,
                          compound="left", bg=config.SEARCH_BUTTON_COLOR, fg=config.SEARCH_BUTTON_TEXT_COLOR, padx=10)
search_button.place(relx=0.5, rely=0.3, anchor="n")


info_label = tk.Label(app, text="Weather info will appear here", font=("Arial", 12), fg=config.INFO_TEXT_COLOR, relief="solid", bd=config.INFO_BORDER_THICKNESS)
info_label.place(relx=0.5, rely=0.43, anchor="n", width=370)  


footer_label = tk.Label(app, text="Code With ♥ By Vishal Sharma", font=("Arial", 10, "italic"), fg="#000000", anchor="center")
footer_label.place(x=0, y=375, relwidth=1, height=25)


show_default_info()

app.mainloop()
