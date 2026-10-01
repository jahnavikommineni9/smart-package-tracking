# Smart Package Tracking & Condition Monitoring System

An IoT-inspired package tracking and condition monitoring project. The system demonstrates how package location, delivery status, and environmental conditions can be monitored through a web dashboard.

## Project Background

I developed this project during my second year of B.Tech as part of my learning in the Internet of Things (IoT) domain. I am uploading it to GitHub now to document my earlier work, preserve the source code, and showcase my practical experience with IoT concepts and web-based monitoring.

## Problem Statement

During transportation, packages may be delayed, exposed to unsuitable temperatures or humidity, or damaged by physical impact. Tracking delivery progress and monitoring package conditions can help logistics teams identify issues earlier.

This project demonstrates a monitoring dashboard for package status and sensor readings. The current version uses simulated sensor data, so it can be run and explored without physical IoT hardware.

## System Architecture

The diagram illustrates a possible end-to-end IoT architecture:

1. **Sensors and tracking modules:** GPS/GSM modules can provide location and communication; RFID readers can identify tagged packages; and a Raspberry Pi can act as an edge device or gateway.
2. **Satellite/GPS and connectivity:** Satellite-based positioning can help determine the vehicle or shipment location. The device sends available tracking information over a network.
3. **Internet communication:** The Internet connects the vehicle or gateway to the backend service and web dashboard.
4. **Backend server:** A server receives, processes, and makes tracking information available to the application.
5. **Database:** Shipment records, status updates, and sensor readings can be stored for retrieval and monitoring.
6. **Web application:** A dashboard lets users view package information, delivery status, and condition alerts.

**Implementation note:** The image is a reference architecture. This repository's current runnable prototype uses **Python, Flask, SQLite, HTML, CSS, and JavaScript**, with simulated sensor readings. It does not currently integrate GPS/GSM hardware, RFID, Raspberry Pi, a Spring Boot server, MongoDB, or Angular. Those components could be explored in a future hardware-integrated version.

## Features

- Package tracking IDs, recipients, and destinations
- Delivery status tracking: Picked Up, In Transit, Delivered, and Exception
- Simulated temperature, humidity, and shock readings
- Condition alerts when configured example thresholds are exceeded
- Search by tracking ID, recipient, or destination
- Dashboard summary cards for shipments and alerts
- SQLite database initialized automatically
- REST API endpoints for package data, summaries, simulated telemetry, and status updates

## Technology Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **IoT concept:** Simulated temperature, humidity, and shock sensor readings

## Project Structure

```text
Smart-Package-Tracking/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── packages.db              # created automatically when the app runs
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── screenshots/
    └── system-architecture.png
```

## How to Run Locally

**Prerequisite:** Python 3.10 or newer.

1. Clone this repository and open the project folder.
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it on Windows:

   ```bash
   .venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   python app.py
   ```

6. Open **http://127.0.0.1:5000** in your browser.

The database and sample package records are created automatically on the first startup.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/packages` | Returns package records; supports the `q` search parameter |
| `GET` | `/api/summary` | Returns shipment counts and the number of packages with alerts |
| `POST` | `/api/simulate` | Generates simulated sensor readings |
| `PATCH` | `/api/packages/<tracking_id>/status` | Updates a package status using a JSON body |

Example request body for a status update:

```json
{
  "status": "Delivered"
}
```

Allowed statuses are `Picked Up`, `In Transit`, `Delivered`, and `Exception`.

## Condition Monitoring and Alerts

The prototype uses example thresholds to demonstrate alerts:

- Temperature below 2°C or above 8°C
- Humidity above 70%
- Shock reading above 1.5 g

These values are illustrative only. Real deployments should use thresholds appropriate to the type of goods, sensor accuracy, and transportation requirements.

## Results and Output

When the application is running, the dashboard displays package IDs, recipient and destination details, environmental readings, delivery status, and condition alerts. The **Refresh sensor data** button generates new simulated readings, while the status dropdown allows a package's delivery status to be changed.

For a complete results section, add screenshots captured from the running application to the `screenshots/` folder and embed them here. For example:

```markdown
![Package dashboard](screenshots/dashboard.png)
![Condition alerts](screenshots/condition-alerts.png)
```

The architecture image above is included as a system design reference; it is not a screenshot of the running application.

## Future Improvements

- Connect an ESP32, GPS module, RFID reader, temperature/humidity sensor, or accelerometer.
- Send device readings to a secured HTTP endpoint or MQTT broker.
- Add map-based location tracking and historical sensor charts.
- Add authentication, role-based access, and audit logs.
- Deploy the application using a production-ready WSGI server and HTTPS.

## Limitations

- Sensor readings are simulated and are not collected from real devices.
- The demo uses sample shipment information.
- The Flask development server is intended for local development, not direct production use.

## GitHub Upload

If you are creating a new GitHub repository, keep **Add README** turned off because this project already contains a README file. After creating the repository, run these commands from this project folder, replacing the URL with your repository URL:

```bash
git init
git add .
git commit -m "Add smart package tracking project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/smart-package-tracking.git
git push -u origin main
```

---

**Project status:** Academic learning project developed during second year and uploaded to GitHub later for documentation and portfolio purposes.
