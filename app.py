from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

app = Flask(__name__)
app.secret_key = "fitflex_secret"

# Groq AI Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# DB setup
conn = sqlite3.connect("fitflex.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")
conn.commit()


@app.route("/")
def home():
    return render_template("index.html")


# 🔥 CHATBOT + AI (FIXED)
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are FitFlex AI fitness trainer. Give short fitness + diet answers."},
                {"role": "user", "content": user_msg}
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "AI error: " + str(e)})


# 🔥 DIET PLAN API
@app.route("/diet", methods=["POST"])
def diet():
    data = request.json
    goal = data.get("goal")

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a diet expert. Give simple Indian diet plan."},
            {"role": "user", "content": goal}
        ]
    )

    return jsonify({"diet": response.choices[0].message.content})


if __name__ == "__main__":
    app.run(debug=True)