"""
Simple Weather App - Windows Compatible Version
No Flask required! Just Python + requests

Requirements: pip install requests
"""

import requests
import json
from datetime import datetime
import sys
import io

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class WeatherApp:
    def __init__(self):
        self.api_base = "https://api.openweathermap.org/data/2.5"
        self.api_key = ""
    
    def setup_api_key(self):
        """Setup API key"""
        print("\n" + "="*60)
        print("WEATHER APP SETUP")
        print("="*60)
        print("\nYou need a FREE API key from OpenWeatherMap")
        print("1. Visit: https://openweathermap.org/api")
        print("2. Sign up (takes 2 minutes)")
        print("3. Get your API key")
        print("4. Wait 1-2 hours for activation")
        print("="*60 + "\n")
        
        self.api_key = input("Enter your API key: ").strip()
        
        if self.api_key:
            # Save to file
            try:
                with open('.weather_key.txt', 'w', encoding='utf-8') as f:
                    f.write(self.api_key)
                print(">> API key saved!\n")
            except Exception as e:
                print(f"Warning: Could not save key: {e}")
        else:
            print("ERROR: No API key provided!")
            return False
        return True
    
    def load_api_key(self):
        """Load API key from file"""
        try:
            with open('.weather_key.txt', 'r', encoding='utf-8') as f:
                self.api_key = f.read().strip()
            return True
        except FileNotFoundError:
            return False
    
    def get_weather_by_city(self, city):
        """Get weather for a city"""
        try:
            url = f"{self.api_base}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            print(f"\n>> Fetching weather for {city}...")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 401:
                print("ERROR: Invalid API key! Please check your key.")
                print("Tip: Wait 1-2 hours after creating a new key.")
                return None
            elif response.status_code == 404:
                print(f"ERROR: City '{city}' not found. Check spelling.")
                return None
            elif response.status_code != 200:
                print(f"ERROR: Server returned status code {response.status_code}")
                return None
            
            return response.json()
            
        except requests.exceptions.Timeout:
            print("ERROR: Request timeout. Please try again.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Network error: {e}")
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    def display_weather(self, data):
        """Display weather information"""
        if not data:
            return
        
        # Parse data
        city = data['name']
        country = data['sys']['country']
        temp = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        description = data['weather'][0]['description'].title()
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        visibility = round(data['visibility'] / 1000, 1)
        cloudiness = data['clouds']['all']
        
        # Get weather condition
        condition = self.get_weather_condition(data['weather'][0]['id'])
        
        # Display
        print("\n" + "="*60)
        print(f"WEATHER IN {city.upper()}, {country}")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
        print(f"\nCondition: {condition}")
        print(f"Description: {description}")
        print(f"\nTemperature: {temp} C (feels like {feels_like} C)")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
        print(f"Pressure: {pressure} hPa")
        print(f"Visibility: {visibility} km")
        print(f"Cloudiness: {cloudiness}%")
        print("="*60 + "\n")
    
    def get_weather_condition(self, weather_id):
        """Get weather condition text based on ID"""
        if weather_id < 300:
            return "THUNDERSTORM"
        elif weather_id < 400:
            return "DRIZZLE"
        elif weather_id < 600:
            return "RAIN"
        elif weather_id < 700:
            return "SNOW"
        elif weather_id < 800:
            return "FOG/MIST"
        elif weather_id == 800:
            return "CLEAR SKY"
        else:
            return "CLOUDY"
    
    def run(self):
        """Main application loop"""
        print("\n" + "="*60)
        print("WELCOME TO WEATHER APP")
        print("="*60)
        
        # Load or setup API key
        if not self.load_api_key():
            print("\n>> First time setup required")
            if not self.setup_api_key():
                return
        else:
            print("\n>> API key loaded successfully!\n")
        
        while True:
            print("\n" + "-"*60)
            print("OPTIONS:")
            print("1. Check weather for a city")
            print("2. Change API key")
            print("3. Exit")
            print("-"*60)
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                city = input("\nEnter city name: ").strip()
                if city:
                    weather_data = self.get_weather_by_city(city)
                    self.display_weather(weather_data)
                else:
                    print("ERROR: Please enter a valid city name")
            
            elif choice == '2':
                self.setup_api_key()
            
            elif choice == '3':
                print("\nThank you for using Weather App!")
                print("Goodbye!\n")
                break
            
            else:
                print("ERROR: Invalid choice! Please enter 1, 2, or 3")


# ============================================================================
# FLASK WEB VERSION (Optional - only if Flask is installed)
# ============================================================================

def run_flask_version():
    """Run Flask web version if available"""
    try:
        from flask import Flask, render_template_string, request, jsonify
        
        app = Flask(__name__)
        weather = WeatherApp()
        weather.load_api_key()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Weather App</title>
            <meta charset="UTF-8">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                }
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                    max-width: 600px;
                    width: 100%;
                }
                h1 { 
                    color: #333; 
                    text-align: center; 
                    margin-bottom: 10px;
                    font-size: 2.5rem;
                }
                .subtitle {
                    text-align: center;
                    color: #666;
                    margin-bottom: 30px;
                }
                input {
                    width: 100%;
                    padding: 15px;
                    border: 2px solid #ddd;
                    border-radius: 10px;
                    font-size: 16px;
                    margin-bottom: 15px;
                }
                input:focus {
                    outline: none;
                    border-color: #667eea;
                }
                button {
                    width: 100%;
                    padding: 15px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: transform 0.2s;
                }
                button:hover { 
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                #result {
                    margin-top: 30px;
                    padding: 25px;
                    background: #f8f9fa;
                    border-radius: 15px;
                    display: none;
                }
                .weather-header {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 20px;
                    text-align: center;
                }
                .weather-info { 
                    margin: 12px 0; 
                    font-size: 18px;
                    padding: 10px;
                    background: white;
                    border-radius: 8px;
                }
                .label {
                    font-weight: 600;
                    color: #667eea;
                }
                .error { 
                    color: #dc3545;
                    background: #ffe5e5;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                }
                .loading {
                    text-align: center;
                    color: #667eea;
                    font-size: 18px;
                }
                .tip {
                    background: #fff3cd;
                    padding: 15px;
                    border-radius: 10px;
                    margin-top: 20px;
                    border-left: 4px solid #ffc107;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Weather App</h1>
                <p class="subtitle">Get real-time weather information</p>
                
                <input type="password" id="apiKey" placeholder="Your OpenWeatherMap API Key">
                <input type="text" id="city" placeholder="Enter city name (e.g., Mumbai, London)">
                <button onclick="getWeather()">Get Weather</button>
                
                <div id="result"></div>
                
                <div class="tip">
                    <strong>Tip:</strong> Get your free API key from 
                    <a href="https://openweathermap.org/api" target="_blank">OpenWeatherMap</a>
                    <br><small>Wait 1-2 hours after creating a new key for activation</small>
                </div>
            </div>
            
            <script>
                function getWeather() {
                    const city = document.getElementById('city').value.trim();
                    const apiKey = document.getElementById('apiKey').value.trim();
                    const result = document.getElementById('result');
                    
                    if (!city || !apiKey) {
                        result.innerHTML = '<p class="error">Please enter both API key and city name!</p>';
                        result.style.display = 'block';
                        return;
                    }
                    
                    result.innerHTML = '<p class="loading">Fetching weather data...</p>';
                    result.style.display = 'block';
                    
                    fetch('/api/weather', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ city: city, api_key: apiKey })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            result.innerHTML = '<p class="error">' + data.error + '</p>';
                        } else {
                            result.innerHTML = `
                                <div class="weather-header">${data.city}, ${data.country}</div>
                                <div class="weather-info">
                                    <span class="label">Temperature:</span> ${data.temperature} C
                                </div>
                                <div class="weather-info">
                                    <span class="label">Feels Like:</span> ${data.feels_like} C
                                </div>
                                <div class="weather-info">
                                    <span class="label">Condition:</span> ${data.description}
                                </div>
                                <div class="weather-info">
                                    <span class="label">Humidity:</span> ${data.humidity}%
                                </div>
                                <div class="weather-info">
                                    <span class="label">Wind Speed:</span> ${data.wind_speed} m/s
                                </div>
                                <div class="weather-info">
                                    <span class="label">Pressure:</span> ${data.pressure} hPa
                                </div>
                            `;
                        }
                    })
                    .catch(error => {
                        result.innerHTML = '<p class="error">Network error: ' + error + '</p>';
                    });
                }
                
                // Allow Enter key to submit
                document.getElementById('city').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') getWeather();
                });
            </script>
        </body>
        </html>
        """
        
        @app.route('/')
        def home():
            return render_template_string(HTML_TEMPLATE)
        
        @app.route('/api/weather', methods=['POST'])
        def api_weather():
            data = request.get_json()
            city = data.get('city')
            api_key = data.get('api_key')
            
            weather.api_key = api_key
            weather_data = weather.get_weather_by_city(city)
            
            if weather_data:
                return jsonify({
                    'city': weather_data['name'],
                    'country': weather_data['sys']['country'],
                    'temperature': round(weather_data['main']['temp']),
                    'feels_like': round(weather_data['main']['feels_like']),
                    'description': weather_data['weather'][0]['description'].title(),
                    'humidity': weather_data['main']['humidity'],
                    'wind_speed': weather_data['wind']['speed'],
                    'pressure': weather_data['main']['pressure']
                })
            else:
                return jsonify({'error': 'Failed to fetch weather data'}), 400
        
        print("\n" + "="*60)
        print("Flask Web Server Starting...")
        print("Open your browser: http://127.0.0.1:5000")
        print("Press Ctrl+C to stop the server")
        print("="*60 + "\n")
        
        app.run(debug=True, port=5000, use_reloader=False)
        
    except ImportError:
        print("\nERROR: Flask not installed!")
        print("Install it with: pip install flask")
        return False


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--web':
            # Try to run Flask version
            if not run_flask_version():
                print("\nFalling back to command line version...\n")
                app = WeatherApp()
                app.run()
        elif sys.argv[1] == '--help':
            print("\n" + "="*60)
            print("WEATHER APP - USAGE")
            print("="*60)
            print("\nCommand Line Mode (default):")
            print("  python weather_app.py")
            print("\nWeb Server Mode (requires Flask):")
            print("  python weather_app.py --web")
            print("\nHelp:")
            print("  python weather_app.py --help")
            print("\nGet API Key:")
            print("  https://openweathermap.org/api")
            print("="*60 + "\n")
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        # Default: Run command line version
        app = WeatherApp()
        app.run()