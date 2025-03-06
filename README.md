# 🚀 Custom Microsoft Edge Profile Picker

## 📢 Introduction
Microsoft Edge lacks a **custom profile picker** like Google Chrome. Yes, it provides one, but it's quite **boring** and switching profiles can be a tedious process.

So, I decided to **build my own!** 🎉

This project is a **custom profile picker for Microsoft Edge** that allows you to quickly switch profiles with a beautiful and user-friendly UI. It also features **avatars, icons, and wallpaper customization** that persist between sessions!

---

## 📸 Screenshots
You can find the screenshots in the **`Screenshot`** folder. 🖼️

---

## 🔧 Requirements
Ensure you have the following installed before running the application:

- **Python** (Latest Version)
- **Tkinter** (GUI Toolkit)
- **JSON** (For storing configurations)
- **Subprocess** (To execute Edge profiles)
- **Pillow (PIL)** (For image processing)
- **Random Avatars** (For profile icons)

Install dependencies using:

```bash
pip install pillow
```

---

## 🛠️ Setup Instructions
### 1️⃣ Create Profiles in Microsoft Edge
Before using this app, **manually create profiles** in the **Microsoft Edge default application**.

### 2️⃣ Update the `app.py`
Modify the profile details inside the script:

```python
self.profiles = {
    "Work Profile": ("Profile 1", os.path.join(self.script_dir, "avatar1.png")), # Update based on your case
    "Data Profile": ("Profile 2", os.path.join(self.script_dir, "avatar2.png"))
}
```
📌 *Ensure the profile names match your Microsoft Edge profiles!*

### 3️⃣ Define Edge Path
Locate your **Microsoft Edge executable** and update its path in the script:

```python
edge_path = r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
```

---

## 🏗️ Application Setup
To create an executable application, use **PyInstaller**.

### 🔹 Standard Build (Basic App)
```bash
pyinstaller --onefile --windowed --icon="edge.ico" --add-data "avatar1.png;." --add-data "avatar2.png;." app.py
```
⚠️ *However, this version does not support wallpaper persistence and has a slower startup!*

### 🔹 Optimized Build (Better Performance ✅)
```bash
pyinstaller --onefile --windowed --icon="edge.ico" --noconsole --add-data "avatar1.png;." --add-data "avatar2.png;." --add-data "config.json;." --upx-exclude "msvcr100.dll" app.py
```

**Optimizations:**
- **🚀 Faster Launch:** `--noconsole` speeds up execution.
- **📦 UPX Compression:** `--upx-exclude` prevents unnecessary decompression delays.
- **🖼️ Optimized Image Loading:** Loads images only when needed.
- **📝 Precompiled Code:** Convert scripts to `.pyc` for efficiency.

---

## 🎉 Enjoy Your Custom Profile Picker!
After building, find your application inside the **`dist`** directory.

✅ **Quickly switch profiles** with ease
✅ **Beautiful UI with avatars & wallpapers**
✅ **Persistent settings** between sessions

💖 If you find this useful, give it a **star ⭐** and a **thumbs up 👍**!

---

### 📌 Future Improvements
- **🔄 Auto-detection of Edge profiles**
- **🎨 Customizable themes**
- **⚡ Faster startup optimizations**

Stay tuned for updates! 🚀

