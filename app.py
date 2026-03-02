from flask import Flask, render_template, request
import re

app = Flask(__name__)

def check_phishing(url):
    score = 0

    if len(url) > 75:
        score += 1

    if "@" in url:
        score += 1

    if url.count('.') > 3:
        score += 1

    suspicious_words = ['login', 'verify', 'bank', 'update', 'secure', 'account']
    for word in suspicious_words:
        if word in url.lower():
            score += 1

    if re.match(r"^http[s]?://\d+\.\d+\.\d+\.\d+", url):
        score += 1

    if score >= 2:
        return "⚠️ This Website is Likely PHISHING!"
    else:
        return "✅ This Website looks SAFE."

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    result = check_phishing(url)
    return render_template("index.html", prediction_text=result)

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=10000)