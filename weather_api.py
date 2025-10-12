from flask import Flask, render_template, request, jsonify
from weather import get_live_weather_and_prediction

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        city = request.form.get('city')
        if not city:
            return jsonify({"error": "City name is required"}), 400

        result = get_live_weather_and_prediction(city)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)