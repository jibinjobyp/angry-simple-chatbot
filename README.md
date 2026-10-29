

---

# 🤬 Angry Robot Friend! (Made with Python)

Have you ever wanted to build your very own robot that gets super easily annoyed and yells funny things back at you? That is exactly what this project is!

Instead of using big, complicated AI from giant tech companies, this robot is built **completely from scratch** using a tiny computer brain written in Python.

---

## 🧩 How Does It Work?

Building this robot is like teaching a little digital baby how to talk:

1. **The Angry Diary (`chat_data.txt`):** We gave the robot a tiny diary filled with funny, grumpy sentences (like *"What the heck do you want?!"*).
2. **Learning Letters:** The robot reads the diary letter by letter and learns which letters usually go together.
3. **The Memory Brain (`PyTorch RNN`):** Thanks to a special memory layer, the robot actually remembers what you just typed to it, instead of just guessing random letters!
4. **The Chat Window (`Flask + Website`):** We wrapped the robot inside a cool dark-mode website so you can type messages and watch it yell back at you in real-time.

---

## 🛠️ What Tools Did We Use?

* **Python:** The main language that brings the robot to life.
* **PyTorch:** The library that builds the robot's tiny neural-network brain.
* **Flask:** The magic tool that connects our Python code to a web browser.
* **HTML & CSS:** Makes the chat window look sleek and clean.

---

## 🚀 How to Play With It On Your Computer

Want to run the angry robot yourself? Follow these 4 easy steps:

### 1. Download the Code

Clone this repository to your computer using Git:

```bash
git clone https://github.com/YOUR_USERNAME/angry-simple-chatbot.git
cd angry-simple-chatbot

```

### 2. Make a Safe Sandbox (`venv`)

Create a virtual environment so your computer stays nice and clean:

* **Windows:** `python -m venv venv`
* **Mac/Linux:** `python3 -m venv venv`

Turn it on:

* **Windows (CMD):** `venv\Scripts\activate`
* **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
* **Mac/Linux:** `source venv/bin/activate`

### 3. Install the Magic Ingredients

Install the required packages inside your sandbox:

```bash
pip install torch flask

```

### 4. Wake Up the Robot!

Run the app:

```bash
python app.py

```

Now, open your web browser, type **`[http://127.0.0.1:5000](http://127.0.0.1:5000)`**, and start chatting with your new grumpy robot friend!
