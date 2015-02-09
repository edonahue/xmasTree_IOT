#Create mysql connection
import MySQLdb

db = MySQLdb.connect(host="", # your host, usually localhost
                     user="user", # your username
                      passwd="", # your password
                      db="sensors") # name of the data base
cur = db.cursor() 

#Import GPIO and set pins
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pins = {
   25 : {'name' : 'Christmas Lights', 'state' : GPIO.LOW}
   }

for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
   for pin in pins:
      pins[pin]['state'] = False
   templateData = {
      'pins' : pins
      }
   return render_template('main.html', **templateData)
   
@app.route("/<changePin>/<action>")
def action(changePin, action):
   changePin = int(changePin)
   deviceName = pins[changePin]['name']
   if action == "on":
      GPIO.output(changePin, GPIO.HIGH)
      message = "Turned " + deviceName + " on."
      cur.execute("Insert into sensors.tree values ('On', sysdate());") 
      db.commit()
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."
      cur.execute("Insert into sensors.tree values ('Off', sysdate());")
      db.commit() 
   if action == "toggle":
      GPIO.output(changePin, not pins[changePin]['state'])
      message = "Toggled " + deviceName + "."
      cur.execute("Insert into sensors.tree values ('Clicked', sysdate());")
      db.commit()
     
   for pin in pins:
      pins[pin]['state'] = not pins[pin]['state']

   templateData = {
      'message' : message, 
      'pins' : pins
   }

   return render_template('main.html', **templateData)
   
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
