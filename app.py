from flask import Flask, request, jsonify, render_template_string, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # nécessaire pour les sessions

USERS = {"admin": "1234"}
current_temp = 25.0
monitoring = True

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>IoT Device Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<h1>IoT Device Dashboard</h1>

<!-- Login -->
<form id="login-form">
    <input name="username" placeholder="Username">
    <input name="password" type="password" placeholder="Password">
    <button type="submit">Login</button>
</form>
<p id="login-result"></p>
<button id="logout-btn" onclick="logout()" style="display:none;">Logout</button>

<!-- Controls -->
<div>
    <input type="number" id="temp-input" placeholder="Set temp">
    <button onclick="setTemp()">Set Temperature</button>
    <button onclick="toggleMonitor()">Toggle Monitoring</button>
</div>

<!-- Graph -->
<canvas id="tempChart" width="400" height="200"></canvas>

<script>
const loginForm = document.getElementById("login-form");
const loginResult = document.getElementById("login-result");
const logoutBtn = document.getElementById("logout-btn");

let loggedIn = false;
let monitoring = true;

// Login fetch
loginForm.addEventListener("submit", async e => {
    e.preventDefault();
    const formData = new FormData(loginForm);
    const res = await fetch("/login", { method: "POST", body: formData });
    if(res.status === 200){
        loginResult.textContent = "Login OK!";
        loggedIn = true;
        logoutBtn.style.display = "inline";
    } else {
        loginResult.textContent = "Login failed!";
    }
});

// Logout fetch
async function logout(){
    await fetch("/logout");
    loggedIn = false;
    loginResult.textContent = "Logged out!";
    logoutBtn.style.display = "none";
}

// Chart setup
const ctx = document.getElementById('tempChart').getContext('2d');
const data = { labels: [], datasets:[{label:'Temp °C',data:[],borderColor:'red',tension:0.3}]};
const config = { type:'line', data:data, options:{animation:false, scales:{y:{min:15,max:35}}} };
const tempChart = new Chart(ctx, config);

// Fetch temperature every second
async function fetchTemp(){
    if(!monitoring) return;
    const res = await fetch('/api/temperature');
    const json = await res.json();
    const now = new Date().toLocaleTimeString();
    if(data.labels.length>20){data.labels.shift();data.datasets[0].data.shift();}
    data.labels.push(now);
    data.datasets[0].data.push(json.value);
    tempChart.update();
}
setInterval(fetchTemp, 1000);

// Controls
function toggleMonitor(){ monitoring = !monitoring; }
async function setTemp(){
    if(!loggedIn){ alert("Login required"); return; }
    const val = parseFloat(document.getElementById("temp-input").value);
    await fetch("/set_temperature?value="+val);
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/login", methods=["POST"])
def login():
    u = request.form.get("username")
    p = request.form.get("password")
    if USERS.get(u) == p:
        session["logged_in"] = True
        return "", 200
    return "", 401

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return "", 200

@app.route("/api/temperature")
def get_temp():
    global current_temp
    # valeur aléatoire autour de la température courante
    current_temp += random.uniform(-0.5,0.5)
    return jsonify({"value": round(current_temp,1)})

@app.route("/set_temperature")
def set_temperature():
    global current_temp
    if not session.get("logged_in"):
        return "Unauthorized", 401
    try:
        current_temp = float(request.args.get("value"))
    except:
        pass
    return "", 200

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
