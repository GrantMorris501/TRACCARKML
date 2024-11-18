### README: Real-Time GPS Tracking to Google Earth KML Converter

---

#### **Overview**

This Python project processes GPS tracking data from a Traccar MySQL database and converts it into a **KML file** for visualization in Google Earth. The program updates the KML file every 30 seconds, displaying the latest device locations and statuses with custom icons and color-coded indicators.

---

#### **Features**
- **Real-Time Data**: Automatically fetches the latest position and status of devices from a Traccar database.
- **Categorization**: Groups devices by roles such as *Leader*, *Rover*, *Event Leader*, and *Police*.
- **Custom Icons**: Applies unique icons to each group for easy identification.
- **Status Indicators**: Color-codes device statuses (e.g., red for "Unknown", light blue for "Moving").
- **KML Output**: Saves a Google Earth-compatible KML file for visualization.
- **Periodic Updates**: Updates the KML file every 30 seconds for near real-time tracking.

---

#### **Getting Started**

##### **System Requirements**
- **Python 3.x**
- MySQL server with Traccar database
- A web server (e.g., Apache or Nginx) to serve the KML file
- Google Earth installed for viewing the KML file

##### **Required Python Libraries**
Install the required libraries using `pip`:
```bash
pip install peewee simplekml
```

---

#### **Setup Instructions**

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/GrantMorris501/TRACCARKML.git
   cd repo-name
   ```

2. **Configure Database Connection**  
   Edit the database configuration in `Traccar_KML.py`:
   ```python
   db = MySQLDatabase(
       "TRACK", 
       host="localhost", 
       user="USER", 
       passwd="USER_PASSWORD"
   )
   ```
   Replace `TRACK`, `USER`, and `USER_PASSWORD` with your database details.

3. **Run the Program**  
   Execute the script to start generating the KML file:
   ```bash
   python3 gps_kml_generator.py
   ```

4. **Access the KML File**  
   The KML file is saved to `/var/www/html/gps.kml` by default.  
   If your web server is set up, you can access the file via your server URL:
   ```
   http://<your_server_ip>/gps.kml
   ```

5. **Visualize in Google Earth**  
   - Open Google Earth.
   - Go to *File* > *Open* and load the KML file as a network link.

---

#### **Customizing the Script**

- **Update Interval**  
  The script updates the KML file every 30 seconds. To change this interval, modify the `threading.Timer` value:
  ```python
  threading.Timer(30, gps_run).start()
  ```

- **Icon Configuration**  
  Customize the icons for each group in the `icon_map` dictionary:
  ```python
  icon_map = {
      "Leader": "http://maps.google.com/mapfiles/kml/shapes/arrow.png",
      "Rover": "http://maps.google.com/mapfiles/kml/shapes/motorcycling.png",
      "Event_Leader": "http://maps.google.com/mapfiles/kml/shapes/woman.png",
      "Police": "http://maps.google.com/mapfiles/kml/shapes/police.png"
  }
  ```

- **Output File Location**  
  The default output path is `/var/www/html/gps.kml`. Update the path in the script as needed:
  ```python
  kml.save("/path/to/your/directory/gps.kml")
  ```

---

#### **Project Structure**

```
repo-name/
├── Traccar_KML.py  # Main script to generate the KML file
└── README.md             # Project documentation
```

---

#### **Troubleshooting**

- **Database Connection Issues**  
  - Ensure the database server is running.
  - Verify credentials and connection settings in the script.

- **KML Not Updating**  
  - Check for script errors during execution.
  - Verify write permissions for the output directory.

- **Google Earth Not Displaying Data**  
  - Ensure the KML file is accessible via the server URL.
  - Confirm the file path in Google Earth is correct.

---

#### **Contributing**

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit and push your changes:
   ```bash
   git commit -m "Add feature description"
   git push origin feature-name
   ```
4. Open a pull request.

---

#### **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

#### **Contact**

For questions or support, feel free to open an issue or contact [your-email@example.com](mailto:your-email@example.com).
