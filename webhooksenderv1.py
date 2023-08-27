import tkinter as tk
from tkinter import messagebox
import requests
import time
import io
from urllib.request import urlopen
from PIL import Image, ImageTk




def send_message():
    webhook_url = webhook_entry.get()
    webhook_username = webhook_username_entry.get()
    message = message_entry.get()
    embed_title = embed_title_entry.get()
    embed_message = embed_message_entry.get()
    times_to_send_text = times_to_send_entry.get()
    fast_send = fast_send_checkbox_var.get()
    embed_color = embed_color_var.get()
    embed_image_url = embed_image_entry.get()
    embed_bottom_text = embed_bottom_text_entry.get()
    webhook_pfp_url = webhook_pfp_entry.get()

    if times_to_send_text.strip():
        times_to_send = int(times_to_send_text)
    else:
        times_to_send = 0

    embed = {
        "title": embed_title,
        "description": embed_message,
        "color": int(embed_color),
    }

    if embed_image_url.strip():
        embed["image"] = {"url": embed_image_url}
    
    if embed_bottom_text.strip():
        embed["footer"] = {"text": embed_bottom_text}

    if webhook_pfp_url.strip():
        set_webhook_pfp(webhook_url, webhook_pfp_url)

    if embed_checkbox_var.get():
        formatted_message = {
            "content": message,
            "username": webhook_username,
            "embeds": [embed]
        }
    else:
        formatted_message = {"content": message, "username": webhook_username}

    delay = 0.5 if fast_send else 2.0

    for _ in range(times_to_send):
        response = requests.post(webhook_url, json=formatted_message)
        
        if response.status_code == 204:
            print("Message sent successfully")
        elif response.status_code == 429:
            print("Rate limit exceeded. Skipping this iteration.")
            continue
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
        
        if not fast_send:
            time.sleep(delay)

    messagebox.showinfo("Message Sent", f"Message sent {times_to_send} times.")


def set_webhook_pfp(webhook_url, image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = response.content
            headers = {
                "Content-Type": "application/json",
            }
            data = {
                "avatar": image_url
            }
            requests.patch(webhook_url, json=data, headers=headers)
        else:
            print("Failed to fetch image from URL.")
    except requests.exceptions.RequestException:
        print("Failed to fetch image from URL.")

root = tk.Tk()
root.title("Discord Webhook Sender")

image_url = "https://assets-prd.ignimgs.com/2022/08/17/top25animecharacters-blogroll-1660777571580.jpg"
response = requests.get(image_url)
image_data = response.content
image = Image.open(io.BytesIO(image_data))
image = image.resize((300, 150))
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.pack()

custom_image_url = "https://i.ytimg.com/vi/7AjqNI5Ojao/hqdefault.jpg"
custom_image_data = requests.get(custom_image_url).content
custom_image = Image.open(io.BytesIO(custom_image_data))
custom_image = custom_image.resize((50, 50))
custom_photo = ImageTk.PhotoImage(custom_image)
custom_image_label = tk.Label(root, image=custom_photo)
custom_image_label.image = custom_photo
custom_image_label.pack(padx=10, pady=10, anchor="nw")  


webhook_label = tk.Label(root, text="Enter your Discord webhook:")
webhook_label.pack()

webhook_entry = tk.Entry(root)
webhook_entry.pack()

webhook_username_label = tk.Label(root, text="Webhook username:")
webhook_username_label.pack()

webhook_username_entry = tk.Entry(root)
webhook_username_entry.pack()

message_label = tk.Label(root, text="Enter your message:")
message_label.pack()

message_entry = tk.Entry(root)
message_entry.pack()

embed_checkbox_var = tk.IntVar()
embed_checkbox = tk.Checkbutton(root, text="Embed tick on/off", variable=embed_checkbox_var)
embed_checkbox.pack()

embed_title_label = tk.Label(root, text="Title of embed:")
embed_title_label.pack()

embed_title_entry = tk.Entry(root)
embed_title_entry.pack()

embed_message_label = tk.Label(root, text="Message in embed:")
embed_message_label.pack()

embed_message_entry = tk.Entry(root)
embed_message_entry.pack()

embed_image_label = tk.Label(root, text="Embed Image URL (optional):")
embed_image_label.pack()

embed_image_entry = tk.Entry(root)
embed_image_entry.pack()

embed_bottom_text_label = tk.Label(root, text="Embed Bottom Text (optional):")
embed_bottom_text_label.pack()

embed_bottom_text_entry = tk.Entry(root)
embed_bottom_text_entry.pack()


webhook_pfp_label = tk.Label(root, text="Enter Webhook Profile Picture URL (MayNotWork):")
webhook_pfp_label.pack()

webhook_pfp_entry = tk.Entry(root)
webhook_pfp_entry.insert(0, "https://example.com/image.jpg")  
webhook_pfp_entry.pack()

times_to_send_label = tk.Label(root, text="Amount of times to send:")
times_to_send_label.pack()

times_to_send_entry = tk.Entry(root)
times_to_send_entry.pack()

fast_send_checkbox_var = tk.IntVar()
fast_send_checkbox = tk.Checkbutton(root, text="Fast Send", variable=fast_send_checkbox_var)
fast_send_checkbox.pack()

embed_color_label = tk.Label(root, text="Select embed color:")
embed_color_label.pack()

embed_color_var = tk.StringVar()
embed_color_var.set("16711680")
embed_color_options = [
    ("Red", "16711680"),
    ("Blue", "255"),
    ("Green", "65280"),
    ("Orange", "16753920"),
    ("Purple", "8388736"),
    ("Yellow", "16776960")
]

for color_name, color_code in embed_color_options:
    tk.Radiobutton(root, text=color_name, variable=embed_color_var, value=color_code).pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()


root.mainloop()
