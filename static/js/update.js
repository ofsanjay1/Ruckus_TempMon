let highestTemperature = 0;

function fetchTemperature() {
    console.log('Fetching temperature...');
    fetch('/temperature')
        .then(response => response.json())
        .then(data => {
            console.log('Fetched data:', data);

            const temperatureContainer = document.getElementById('temperature-container');
            temperatureContainer.innerHTML = '';

            data.forEach(device => {
                const deviceContainer = document.createElement('div');
                deviceContainer.className = 'device-container';
                
                const locationElement = document.createElement('h2');
                locationElement.textContent = device.location;

                const temperatureElement = document.createElement('p');
                temperatureElement.className = `temperature ${parseFloat(device.temperature) > 40 ? 'high' : ''}`;
                temperatureElement.textContent = device.temperature;

                deviceContainer.appendChild(locationElement);
                deviceContainer.appendChild(temperatureElement);
                temperatureContainer.appendChild(deviceContainer);
                
                const currentTemperature = parseFloat(device.temperature);
                highestTemperature = Math.max(highestTemperature, currentTemperature);
            });

            const temperatureElements = document.querySelectorAll('.temperature');
            temperatureElements.forEach(temperatureElement => {
                if (highestTemperature >= 50) {
                    temperatureElement.classList.add('high');
                } else {
                    temperatureElement.classList.remove('high');
                }
            });

            if (highestTemperature > 50) {
                document.body.style.backgroundColor = 'red';
            } else {
                document.body.style.backgroundColor = '#f0f0f0';
            }
        })
        .catch(error => {
            console.error('Error fetching temperature:', error);
        });
}

// Fetch temperature immediately and then every 60 seconds
fetchTemperature();
setInterval(fetchTemperature, 600000);

