# gpxtokml

Converts a to a GPX in a simple KML file . The GPX file is the output of a generic K37 Runnning Smartwach. This file contains the point of an running traning session. Only latitude and longitude. I made this script to get an kml file for importing in My Maps Google and saving my races with distances, average speed...
I found this repo https://github.com/pglez82/gpx2kml.git. It was a great kickoff to start.


## Usage
Install the dependencies with `pip install -r requirements`. Run the program:

```python
python gpxtokml.py -f test_files/sport_1_2024_04_07_081506.gpx -n "10KM Marathon..."
```