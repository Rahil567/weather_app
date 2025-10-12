document.getElementById('weatherForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const city = document.getElementById('city').value;
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = "⏳ Getting prediction...";

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `city=${encodeURIComponent(city)}`
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `❌ Error: ${data.error}`;
        } else {
            resultDiv.innerHTML = `
                <h3>${data.city}</h3>
                <p>Temperature: ${data.temperature}°C</p>
                <p>Humidity: ${data.humidity}%</p>
                <p>Wind Speed: ${data.wind_speed} m/s</p>
                <p><strong>Rain Prediction: ${data.rain_prediction}</strong></p>
            `;
        }
    } catch (err) {
        resultDiv.innerHTML = `❌ Error fetching prediction: ${err}`;
    }
});