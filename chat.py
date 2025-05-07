from flask import Flask, request, render_template
import openai
import os
import re

app = Flask(__name__)

# OpenAI APIキーを環境変数から取得
openai.api_key = os.getenv("OPENAI_API_KEY")

# NGワードリスト（必要に応じて追加・調整してください）
NG_WORDS = [
    "エッチ", "殺す", "死ぬ", "暴力", "付き合う", "キス", "個人情報", "電話番号", "住所",
    "なぐる", "いやがらせ", "ばか", "おとなの", "せい", "セックス", "えろ", "グロ", "血"
]

@app.route("/", methods=["GET", "POST"])
def chat():
    answer = ""
    if request.method == "POST":
        user_input = request.form["message"]

        # NGワードチェック（小文字化して部分一致）
        for ng in NG_WORDS:
            if ng in user_input.lower():
                answer = "ごめんね。そのことについてはおはなしできないよ。ほかのことをきいてね。"
                return render_template("chat.html", answer=answer)

        # OpenAIに問い合わせ（子ども向けプロンプト）
        messages = [
            {"role": "system", "content": "あなたは子どもにやさしく教えるAI先生です。むずかしい言葉はつかわず、こわい・せいてき・あらっぽい話はしないでください。"},
            {"role": "user", "content": user_input}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = "ごめんね。いまはこたえられないみたい。あとでまたためしてね。"

    return render_template("chat.html", answer=answer)

# Render 用のホスト・ポート指定
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
