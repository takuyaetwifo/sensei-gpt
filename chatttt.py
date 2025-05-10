from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# OpenAI APIキーを環境変数から取得
openai.api_key = os.getenv("OPENAI_API_KEY")

NG_WORDS = [
    "エッチ", "殺す", "死ぬ", "暴力", "付き合う", "キス", "個人情報", "電話番号", "住所",
    "なぐる", "いやがらせ", "ばか", "おとなの", "せい", "セックス", "えろ", "グロ", "血"
]

@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    messages = []
    answer = ""

    if request.method == "POST":
        user_input = request.form.get("message", "")  # 安全に取得
        if not user_input:
            answer = "入力がありません"
        else:
            # NGワードチェック（簡易例）
            NG_WORDS = ["暴力", "えろ", "せい"]  # ここ省略可
            for ng in NG_WORDS:
                if ng in user_input:
                    answer = "ごめんね。そのことについてはおはなしできないよ。"
                    break
            else:
                # OpenAI 呼び出し
                messages = [
                    {"role": "system", "content": "あなたは子どもにやさしく教えるAI先生です。"},
                    {"role": "user", "content": user_input}
                ]
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=1000
                )
                    gpt_response = response.choices[0].message.content
                except Exception as e:
                    gpt_response = f"エラー: {str(e)}"

        return render_template("chat.html", username=session.get("username", "ゲスト"), answer=answer, messages=messages)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
