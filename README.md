# NodeProtect - IoT Lab

Hands-on IoT Security Lab using Flask and Docker.  
This lab allows students to interact with a simulated IoT device (temperature monitor) and practice security concepts.

---

## Repository Contents

- `app.py` : Flask application simulating the IoT device  
- `Dockerfile` : Docker image definition for NodeProtect  
- `requirements.txt` : Python dependencies (`flask`)  
- `.gitignore` : ignores Python cache files and env files

---

## Prerequisites

- Docker installed on your machine
- Optional: Docker Compose if you want to extend with Node-RED or other services

---

## Build & Run

1. **Build the Docker image**

```bash
docker build -t flask-iot .

Run the container

docker run -p 5000:5000 flask-iot

Open the lab

Go to http://localhost:5000
 in your browser

Features

Login to the IoT device (no logout implemented yet)

Adjust temperature values

Start/stop monitoring

Simple Flask web interface

⚠️ This is an educational lab, not for production use.
