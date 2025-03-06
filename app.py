import os
import json
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFilter

CONFIG_FILE = "config.json"

class EdgeProfilePicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Microsoft Edge Profile Picker")
        self.root.geometry("700x450")
        self.root.configure(bg="#F5F5F7")
        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.profiles = {
            "Work Profile": ("Profile 1", os.path.join(self.script_dir, "avatar1.png")),
            "Data Profile": ("Profile 2", os.path.join(self.script_dir, "avatar2.png"))
        }
        
        self.bg_image = None

        self.background_label = tk.Label(self.root)
        self.background_label.place(relwidth=1, relheight=1)

        self.load_config()

        self.parent_frame = tk.Frame(self.root, bg="#F5F5F7")
        self.parent_frame.pack(expand=True)

        title = tk.Label(self.parent_frame, text="Select a Profile", font=("Arial", 18, "bold"), fg="#333", bg="#F5F5F7")
        title.pack(pady=10)

        for profile_name, profile_data in self.profiles.items():
            self.create_profile_card(profile_name, profile_data)

        self.customize_button = tk.Button(
            self.root,
            text="Customize",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#007AFF",
            bd=0,
            padx=20,
            pady=10,
            command=self.choose_background,
            relief="flat",
            activebackground="#005BB5",
            activeforeground="white"
        )
        self.customize_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        self.customize_button.bind("<Enter>", lambda e: self.customize_button.config(bg="#005BB5")) 
        self.customize_button.bind("<Leave>", lambda e: self.customize_button.config(bg="#007AFF")) 
        self.apply_background()
    
    def open_edge(self, profile_name):
        edge_path = r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
        if profile_name in self.profiles:
            profile_dir = self.profiles[profile_name][0]
            profile_arg = f"--profile-directory={profile_dir}"
            try:
                subprocess.Popen([edge_path, profile_arg], shell=True)
                self.root.destroy()
            except FileNotFoundError:
                messagebox.showerror("Error", "Microsoft Edge executable not found!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch Edge: {e}")
        else:
            messagebox.showerror("Error", "Invalid profile selection!")
    
    def create_profile_card(self, profile_name, profile_data):
        profile_dir, avatar_path = profile_data
        card = tk.Canvas(self.parent_frame, width=160, height=220, bg="#F5F5F7", highlightthickness=0)
        card.pack(side="left", padx=15, pady=10)
        shadow = Image.new("RGBA", (160, 220), "#00000000")
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle((0, 0, 160, 220), radius=20, fill="#00000020")
        shadow = shadow.filter(ImageFilter.GaussianBlur(10))
        shadow = ImageTk.PhotoImage(shadow)
        card.create_image(5, 5, anchor="nw", image=shadow)
        card.shadow = shadow 

        self.create_rounded_rectangle(card, 5, 5, 155, 215, radius=20, fill="white", outline="#E0E0E0")
        avatar = self.create_rounded_avatar(avatar_path, (60, 60))
        avatar = ImageTk.PhotoImage(avatar)
        avatar_label = tk.Label(card, image=avatar, bg="white")
        avatar_label.image = avatar
        card.create_window(80, 70, window=avatar_label)
        label = tk.Label(card, text=profile_name, font=("Arial", 14, "bold"), fg="#333", bg="white")
        card.create_window(80, 140, window=label)
        button = tk.Button(
            card,
            text="Select",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#007AFF",
            bd=0,
            padx=20,
            pady=5,
            command=lambda: self.open_edge(profile_name),
            relief="flat",
            activebackground="#005BB5",
            activeforeground="white"
        )
        button_window = card.create_window(80, 180, window=button)
        button.bind("<Enter>", lambda e: button.config(bg="#005BB5")) 
        button.bind("<Leave>", lambda e: button.config(bg="#007AFF"))  
    
    def create_rounded_avatar(self, image_path, size):
        try:
            image = Image.open(image_path)
            image = image.resize(size, Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"Error loading {image_path}: {e}")
            image = Image.new("RGB", size, "#007AFF")
        
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, *size), fill=255)
        
        rounded_image = Image.new("RGBA", size)
        rounded_image.paste(image, (0, 0), mask)
        return rounded_image
    
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)
    
    def choose_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.set_background(file_path)
            self.save_config(file_path)
    
    def set_background(self, image_path):
        image = Image.open(image_path)
        image = image.resize((700, 450), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)
        self.background_label.config(image=self.bg_image)
    
    def save_config(self, image_path):
        with open(CONFIG_FILE, "w") as file:
            json.dump({"background": image_path}, file)
    
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                self.set_background(config.get("background", ""))
    
    def apply_background(self):
        self.load_config()
        self.parent_frame.lift()
        self.customize_button.lift()

if __name__ == "__main__":
    root = tk.Tk()
    app = EdgeProfilePicker(root)
    root.mainloop()