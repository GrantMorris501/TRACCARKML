import time as t  # For handling time-related functions
import os  # Provides functions to interact with the operating system
import sys  # Provides access to system-specific parameters and functions
from peewee import *  # Peewee ORM for interacting with the database
import getpass  # Securely handle user passwords
import simplekml  # Library for generating KML files
import threading  # For running periodic tasks in a separate thread

# Initialize a connection to a MySQL database using Peewee
db = MySQLDatabase(
    "TRACK", 
    host="localhost", 
    user="USER", 
    passwd="USER_PASSWORD"
)

# Define the "devices" table in the database
class Devices(Model):
    name = TextField()  # Name of the device
    uniqueId = IntegerField()  # Unique ID of the device
    lastUpdate = DateField()  # Last update date
    positionId = TextField()  # Position ID
    groupid = IntegerField()  # Group ID
    attributes = TextField()  # Device attributes
    phone = TextField()  # Device phone number
    model = TextField()  # Device model
    contact = TextField()  # Device contact information
    category = TextField()  # Device category

    class Meta:
        database = db  # Connect to the "db" database

# Define the "positions" table in the database
class Positions(Model):
    deviceId = IntegerField()  # ID of the device
    servertime = DateTimeField()  # Server timestamp
    devicetime = DateTimeField()  # Device timestamp
    latitude = DoubleField()  # Latitude of the device
    longitude = DoubleField()  # Longitude of the device
    speed = FloatField()  # Speed of the device

    class Meta:
        database = db

# Define the "groups" table in the database
class Groups(Model):
    name = TextField()  # Name of the group

    class Meta:
        database = db

# Define the "events" table in the database
class Events(Model):
    Type = TextField()  # Event type (e.g., device status)
    deviceid = IntegerField()  # ID of the associated device

    class Meta:
        database = db

# Function to generate a live GPS tracking KML file and save it periodically
def gps_run():
    Latest_User = []  # List to store the latest device information
    users = Devices.select().order_by(Devices.groupid)  # Fetch all devices
    act_groups = Groups.select()  # Fetch all groups
    group_key = {g.id: g.name for g in act_groups}  # Map group IDs to names

    for device in users:
        gps_location = Positions.select().where(
            Positions.deviceId == device.id
        ).order_by(Positions.id.desc()).limit(1)  # Fetch the latest position
        gps_status = Events.select().where(
            Events.deviceid == device.id
        ).order_by(Events.id.desc()).limit(1)  # Fetch the latest event status

        for status in gps_status:
            for position in gps_location:
                icon_type = group_key.get(device.groupid, "Unknown")
                temp_list = [device.name, position.latitude, position.longitude, icon_type, status.Type]
                Latest_User.append(temp_list)

    # Generate the KML file
    kml = simplekml.Kml(name='Live Track', open=1)
    folgroup = []  # List to track created folders in KML

    for user in Latest_User:
        name, lat, lon, icon_type, icon_status = user
        if icon_type not in folgroup:
            fol = kml.newfolder(name=icon_type, open=1)
            folgroup.append(icon_type)

        # Add a point for each user
        pnt = fol.newpoint(name=name, coords=[(lon, lat)])
        icon_map = {
            "Leader": "http://maps.google.com/mapfiles/kml/shapes/arrow.png",
            "Rover": "http://maps.google.com/mapfiles/kml/shapes/motorcycling.png",
            "Event_Leader": "http://maps.google.com/mapfiles/kml/shapes/woman.png",
            "Police": "http://maps.google.com/mapfiles/kml/shapes/police.png"
        }
        pnt.style.iconstyle.icon.href = icon_map.get(icon_type, "")

        # Adjust icon color based on status
        if icon_status == "deviceUnknown":
            pnt.style.iconstyle.color = simplekml.Color.red
        elif icon_status == "deviceMoving":
            pnt.style.iconstyle.color = simplekml.Color.lightblue

    # Save the KML file
    kml.save("/var/www/html/gps.kml")
    # Run the function again after 30 seconds
    threading.Timer(30, gps_run).start()

# Start the GPS tracking function
gps_run()
