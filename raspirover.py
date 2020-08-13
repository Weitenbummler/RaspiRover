
import time
import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
from roboclaw_3 import Roboclaw

geschwindigkeit = 60

roboclaw = Roboclaw('/dev/ttyACM0', 38400)
roboclaw.Open()

# Flask - Webseite

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
   
        #geschwindigkeit = request.form["geschwindigkeit"]

        if request.form['steuerbefehl'] == "vor": fahre_rover_vorwaerts(geschwindigkeit)
        if request.form['steuerbefehl'] == "stop": stoppe_rover()
        if request.form['steuerbefehl'] == "zurueck": fahre_rover_rueckwaerts(geschwindigkeit)
        if request.form['steuerbefehl'] == "rechts": drehe_rover_nach_rechts(geschwindigkeit)
        if request.form['steuerbefehl'] == "links": drehe_rover_nach_links(geschwindigkeit)

    return render_template ('index.html')

# Kommandos direkt über einzelne URLs

@app.route("/vor/<int:geschwindigkeit>")
def vorwaerts(geschwindigkeit):
    fahre_rover_vorwaerts(geschwindigkeit)
    return "vorwärts"

@app.route("/zurueck/<int:geschwindigkeit>")
def zurueck(geschwindigkeit):
    fahre_rover_rueckwaerts(geschwindigkeit)
    return "zurück"

@app.route("/stop")
def stop():
    stoppe_rover()
    return "stop"

@app.route("/links")
def links():
    drehe_rover_nach_links(geschwindigkeit)
    return "links"

@app.route("/rechts")
def rechts():
    drehe_rover_nach_rechts(geschwindigkeit)
    return "rechts"

# Befehle an Roboclaw geben

def fahre_rover_vorwaerts(geschwindigkeit):
    drehe_rechten_motor_vorwaerts(geschwindigkeit)
    drehe_linken_motor_vorwaerts(geschwindigkeit)
    return "OK"

def fahre_rover_rueckwaerts(geschwindigkeit):
    drehe_rechten_motor_rueckwaerts(geschwindigkeit)
    drehe_linken_motor_rueckwaerts(geschwindigkeit)
    return "OK"

def drehe_rover_nach_rechts(geschwindigkeit):
    drehe_rechten_motor_rueckwaerts(geschwindigkeit)
    drehe_linken_motor_vorwaerts(geschwindigkeit)
    return "OK"

def drehe_rover_nach_links(geschwindigkeit):
    drehe_rechten_motor_vorwaerts(geschwindigkeit)
    drehe_linken_motor_rueckwaerts(geschwindigkeit)
    return "OK"

def stoppe_rover():
    drehe_rechten_motor_vorwaerts(0)
    drehe_linken_motor_vorwaerts(0)
    return "OK"
 
def drehe_rechten_motor_vorwaerts(geschwindigkeit):
    roboclaw.ForwardM1(0x80, geschwindigkeit)
    return "OK"
  
def drehe_linken_motor_vorwaerts(geschwindigkeit):
    roboclaw.ForwardM2(0x80, geschwindigkeit)
    return "OK"

def drehe_rechten_motor_rueckwaerts(geschwindigkeit):
    roboclaw.BackwardM1(0x80, geschwindigkeit)
    return "OK"

def drehe_linken_motor_rueckwaerts(geschwindigkeit):
    roboclaw.BackwardM2(0x80, geschwindigkeit)
    return "OK"

# MQTT

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set("mqtt_user", password="mqttpwd")
client.connect("192.168.178.74", 1883, 60)
client.publish("RaspiRover/Status", "test")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337, debug=True)
