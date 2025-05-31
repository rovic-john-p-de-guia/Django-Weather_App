document.addEventListener('DOMContentLoaded', function() {
    const weatherForm = document.getElementById('weather-form');
    const weatherResult = document.getElementById('weather-result');
    const errorMessage = document.getElementById('error-message');

    weatherForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const location = document.getElementById('location').value;
        
        try {
            const response = await fetch('/weather/get-weather/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `location=${encodeURIComponent(location)}`
            });

            const data = await response.json();

            if (response.ok) {
                displayWeather(data);
                errorMessage.classList.add('d-none');
            } else {
                showError(data.error || 'Failed to fetch weather data');
            }
        } catch (error) {
            showError('An error occurred while fetching weather data');
        }
    });

    function displayWeather(data) {
        document.getElementById('location-name').textContent = data.location;
        document.getElementById('temperature').textContent = data.temperature;
        document.getElementById('temperature-unit').textContent = data.temperature_unit || '';
        document.getElementById('summary').textContent = data.summary || '';
        document.getElementById('description').textContent = data.description || '';
        document.getElementById('feels-like').textContent = data.feels_like !== undefined ? `${data.feels_like} ${data.temperature_unit || ''}` : '';
        document.getElementById('temp-min').textContent = data.temp_min !== undefined ? `${data.temp_min} ${data.temperature_unit || ''}` : '';
        document.getElementById('temp-max').textContent = data.temp_max !== undefined ? `${data.temp_max} ${data.temperature_unit || ''}` : '';
        document.getElementById('humidity').textContent = data.humidity !== undefined ? `${data.humidity}${data.humidity_unit || ''}` : '';
        document.getElementById('pressure').textContent = data.pressure !== undefined ? `${data.pressure} ${data.pressure_unit || ''}` : '';
        document.getElementById('wind').textContent = data.wind_speed !== undefined ? `${data.wind_speed} ${data.wind_speed_unit || ''} ${data.wind_direction ? '(' + data.wind_direction + ')' : ''}` : '';
        document.getElementById('cloudiness').textContent = data.cloudiness !== undefined ? `${data.cloudiness}${data.cloudiness_unit || ''}` : '';
        document.getElementById('rain').textContent = data.rain_amount !== undefined ? `${data.rain_amount || 0} ${data.rain_unit || ''}` : '';
        document.getElementById('snow').textContent = data.snow_amount !== undefined ? `${data.snow_amount || 0} ${data.snow_unit || ''}` : '';
        document.getElementById('visibility').textContent = data.visibility_distance !== undefined ? `${data.visibility_distance} ${data.visibility_unit || ''}` : '';
        document.getElementById('precipitation-prob').textContent = data.probability_of_precipitation !== undefined ? `${data.probability_of_precipitation}${data.probability_of_precipitation_unit || ''}` : '';
        document.getElementById('part-of-day').textContent = data.part_of_day || '';
        document.getElementById('datetime').textContent = data.datetime || '';
        if (data.icon) {
            document.getElementById('weather-icon').src = data.icon.startsWith('http') ? data.icon : `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
        }
        weatherResult.classList.remove('d-none');
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('d-none');
        weatherResult.classList.add('d-none');
    }

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}); 