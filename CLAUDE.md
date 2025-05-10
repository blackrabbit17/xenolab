# Commands and Guidelines for XenoLab

## Build & Run Commands
- Frontend: `cd frontend && npm run dev` - Run development server
- Frontend: `cd frontend && npm run build` - Build for production
- Frontend: `cd frontend && npm run lint` - Lint JavaScript/Vue files
- Frontend: `cd frontend && npm run format` - Format with Prettier
- Backend: `cd backend && python manage.py runserver` - Run Django server
- Backend: `cd backend && python manage.py test` - Run all tests
- Backend: `cd backend && python manage.py test app_name.tests.TestClass` - Run specific test
- Backend: `cd backend && python manage.py sunlight` - Run sunlight simulation
- Backend: `cd backend && python manage.py wind` - Run wind simulation
- Backend: `cd backend && python manage.py temphumidity` - Record temperature/humidity

## Style Guidelines
- Frontend: Vue 3 with Composition API, Pinia for state management
- Frontend: 2-space indentation, no semicolons, single quotes, 100-char line limit
- Backend: Follow PEP 8 standards for Python code
- Backend: Use Django's model-view-template pattern
- Imports: Group standard library, third-party, and local imports
- Error handling: Use try/except in Python, try/catch in JavaScript
- Naming: camelCase for JS variables/functions, PascalCase for Vue components, snake_case for Python

## Backend Structure
- Django 5.2 with SQLite database
- Main apps: temphumidity, wind, sunlight, camera, xenolab (core)
- Hardware integration via Adafruit libraries and GPIO controls
  - Temperature/Humidity: adafruit_dht (DHT11 sensor on GPIO4)
  - Sunlight: neopixel (LED strip on GPIO12, 24 LEDs)
  - Wind: serial communication with USB relay (/dev/ttyACM0)
  - Camera: picamera/picamera2 (supports legacy and newer Pi camera modules)
- API endpoints: /wind/, /sunlight/, /temphumidity/, /camera/*, /lifeform/, /map/, /atmospherics/
- Models track environmental readings with timestamps (TempHumidityReading, Wind, Sunlight)
- Asset files in /backend/assets/ contain lifeform specifications
- Custom management commands run as services for environmental control

## Frontend Structure
- Vue 3 + Vite, Tailwind CSS for styling
- Uses chart.js for data visualization
- Communicates with backend via API endpoints

Note: Update this cheatsheet when learning new information about the project structure.