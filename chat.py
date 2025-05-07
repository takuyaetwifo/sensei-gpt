from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def chat():
    answer = ""
    if request.method == "POST":
        user_input = request.form["message"]

        messages = [
            {"role": "system", "content": "あなたは子どもにやさしく教えるAI先生です。むずかしい言葉はつかわず、こわい・せいてき・あらっぽい話はしないでください。"},
            {"role": "user", "content": user_input}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer = response.choices[0].message.content

    return render_template("chat.html", answer=answer)
