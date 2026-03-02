from flask import Flask, request, jsonify, render_template_string
import phonenumbers
from phonenumbers import geocoder, carrier

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>AI Phone Tracker</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px;">
    <h2>AI Phone Tracker</h2>
    <input type="text" id="phone" placeholder="+1234567890">
    <button onclick="track()">Track</button>
    <div id="result" style="margin-top: 20px;"></div>
    <script>
        async function track() {
            const num = document.getElementById('phone').value;
            const res = await fetch(`/api/track?number=${encodeURIComponent(num)}`);
            const data = await res.json();
            document.getElementById('result').innerText = data.error || 
                `Location: ${data.location} | Carrier: ${data.carrier}`;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/track')
def track():
    number = request.args.get('number')
    try:
        parsed_number = phonenumbers.parse(number)
        return jsonify({
            "location": geocoder.description_for_number(parsed_number, "en"),
            "carrier": carrier.name_for_number(parsed_number, "en")
        })
    except:
        return jsonify({"error": "Invalid Number"}), 400