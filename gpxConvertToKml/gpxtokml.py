import gpxpy
import gpxpy.gpx
import xml.etree.cElementTree as ET
import argparse
import os
from datetime import datetime
from xml.dom import minidom
import pytz
from zoneinfo import ZoneInfo
import math

parser = argparse.ArgumentParser(description='Convert a GPX to KML for using in Google Maps')
parser.add_argument("-f", "--file", type=str,help="gpx file to be converted", required=True)
parser.add_argument("-n", "--name", type=str,help="name of race track", required=True)

args = parser.parse_args()

name_race = os.path.splitext(args.name)[0]

gpx_file = open(args.file, 'r')

gpx = gpxpy.parse(gpx_file)

timestamp = gpx.time

timestampstring = timestamp.replace(tzinfo=None).isoformat()+'Z'

coordinates = ""

#Return each point coordinate of Track
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            coordinates+="{},{} ".format(point.longitude,point.latitude)

start_point =   "{},{}, ".format(gpx.tracks[0].segments[0].points[0].longitude,gpx.tracks[0].segments[0].points[0].latitude)   
start_time = gpx.get_time_bounds().start_time

#Date format and zone info
date_format = "%d/%m/%Y, %H:%M:%S"
zone_info = "America/Buenos_Aires"

start_datetime = start_time.astimezone(ZoneInfo(zone_info)).strftime(date_format)
start_point_description = start_datetime

finish_point = "{},{} ".format(gpx.tracks[0].segments[-1].points[0].longitude,gpx.tracks[0].segments[-1].points[0].latitude) 
finish_time = gpx.get_time_bounds().end_time

#Compute race time as timedelta
race_duration = finish_time - start_time

finish_datetime = finish_time.astimezone(ZoneInfo(zone_info)).strftime(date_format)
finish_point_description = finish_datetime

segments = gpx.tracks[0].segments

#Compute total distance iterating points for each segment   
dis = 0
for i in range(len(segments) - 1):
  dis += segments[i].points[0].distance_2d(segments[i+1].points[0])

time_dif_seconds = gpx.tracks[0].segments[0].points[0].time_difference(gpx.tracks[0].segments[-1].points[0])

dist_km = round(dis/1000,2)

#Compute average speed in meters / seconds
average_speed = dis/time_dif_seconds

#Convert average speed in min / km
average_speed_min_km = 1/(0.06*average_speed)

frac, whole = math.modf(average_speed_min_km)

min=int(whole)
sec = round(frac*60)

average_speed_min_km =  str(min) + ':' + str(sec) + ' min/km'

kml_attrib = {
  "xmlns": "http://www.opengis.net/kml/2.2" 
}

style_red_attib = {
  "id": "red"
}

style_route_red_attib = {
  "id": "route_red"
}

style_icon_attrib = {
  "id" : "icon-1899-0288D1-nodesc-normal"
}

#Create the kml file as an xml
name_file = os.path.splitext(os.path.basename(args.file))[0] 
name_text = name_file
description_text = ""

root = ET.Element("kml",kml_attrib)
document_tag = ET.SubElement(root,"Document")
name_tag = ET.SubElement(document_tag,"name").text= name_text
timestamp_tag = ET.SubElement(document_tag,"TimeStamp")
when_tag = ET.SubElement(timestamp_tag,"when").text = timestampstring
description_tag = ET.SubElement(document_tag,"description").text = description_text
visibilty_tag = ET.SubElement(document_tag,"visibility").text = "1"
open_tag = ET.SubElement(document_tag, "open").text ="1"

style_red_tag = ET.SubElement(document_tag,"Style",style_red_attib)
line_style_red_tag = ET.SubElement(style_red_tag,"LineStyle")
color_red_tag = ET.SubElement(line_style_red_tag,"color").text = "ff1400ff"
width_red_tag = ET.SubElement(line_style_red_tag,"width").text = "4"

style_route_red_tag = ET.SubElement(document_tag,"Style",style_route_red_attib)
line_style_route_red_tag = ET.SubElement(style_route_red_tag,"LineStyle")
color_route_red_tag = ET.SubElement(line_style_route_red_tag,"color").text = "961400FF"
width_route_red_tag = ET.SubElement(line_style_route_red_tag,"width").text = "4"


#Start Line Style
style2_icon_start_tag = ET.SubElement(document_tag,"Style",{
  "id" : "icon-1899-0F9D58-normal"
})
icon_style2_tag = ET.SubElement(style2_icon_start_tag,"IconStyle")
color_icon_style2_tag = ET.SubElement(icon_style2_tag, "color").text = "ff589d0f"
scale_icon_style2_tag = ET.SubElement(icon_style2_tag,"scale").text = "1"
icon2_style2_tag  = ET.SubElement(icon_style2_tag,"Icon")
href_icon2_tag = ET.SubElement(icon2_style2_tag, "href").text = "https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png"
hotspot_icon2_tag = ET.SubElement(icon_style2_tag,"hotSpot", {
  "x" : "32",
  "xunits" : "pixels",
  "y" : "64",
  "yunits" : "insetPixels"
})
label_icon2_tag = ET.SubElement(style2_icon_start_tag, "LabelStyle")
scale_label_icon2_tag = ET.SubElement(label_icon2_tag, "scale").text = "0"

style2h_icon_start_tag = ET.SubElement(document_tag,"Style",{
  "id" : "icon-1899-0F9D58-highlight"
})
icon_style2h_tag = ET.SubElement(style2h_icon_start_tag,"IconStyle")
color_icon_style2h_tag = ET.SubElement(icon_style2h_tag, "color").text = "ff589d0f"
scale_icon_style2h_tag = ET.SubElement(icon_style2h_tag,"scale").text = "1"
icon2_style2h_tag  = ET.SubElement(icon_style2h_tag,"Icon")
href_icon2h_tag = ET.SubElement(icon2_style2h_tag, "href").text = "https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png"
hotspot_icon2h_tag = ET.SubElement(icon_style2h_tag,"hotSpot", {
  "x" : "32",
  "xunits" : "pixels",
  "y" : "64",
  "yunits" : "insetPixels"
})
label_icon2h_tag = ET.SubElement(style2h_icon_start_tag, "LabelStyle")
scale_label_icon2_tag = ET.SubElement(label_icon2h_tag, "scale").text = "0"

style_map_tag = ET.SubElement(document_tag,"StyleMap", {
  "id":  "icon-1899-0F9D58"
})
pair_tag = ET.SubElement(style_map_tag,"Pair")
key_tag = ET.SubElement(pair_tag, "key").text = "normal"
style_url_map_tag = ET.SubElement(pair_tag, "styleUrl").text = "#icon-1899-0F9D58-normal"

pair2_tag = ET.SubElement(style_map_tag,"Pair")
key2_tag = ET.SubElement(pair2_tag, "key").text = "highlight"
style_url_map2_tag = ET.SubElement(pair2_tag, "styleUrl").text = "#icon-1899-0F9D58-highlight"

###  Finish Line Style
style2_icon_start_tag = ET.SubElement(document_tag,"Style",{
  "id" : "icon-1899-C2185B-normal"
})
icon_style2_tag = ET.SubElement(style2_icon_start_tag,"IconStyle")
color_icon_style2_tag = ET.SubElement(icon_style2_tag, "color").text = "ff589d0f"
scale_icon_style2_tag = ET.SubElement(icon_style2_tag,"scale").text = "1"
icon2_style2_tag  = ET.SubElement(icon_style2_tag,"Icon")
href_icon2_tag = ET.SubElement(icon2_style2_tag, "href").text = "https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png"
hotspot_icon2_tag = ET.SubElement(icon_style2_tag,"hotSpot", {
  "x" : "32",
  "xunits" : "pixels",
  "y" : "64",
  "yunits" : "insetPixels"
})
label_icon2_tag = ET.SubElement(style2_icon_start_tag, "LabelStyle")
scale_label_icon2_tag = ET.SubElement(label_icon2_tag, "scale").text = "0"

style2h_icon_start_tag = ET.SubElement(document_tag,"Style",{
  "id" : "icon-1899-C2185B-highlight"
})
icon_style2h_tag = ET.SubElement(style2h_icon_start_tag,"IconStyle")
color_icon_style2h_tag = ET.SubElement(icon_style2h_tag, "color").text = "ff589d0f"
scale_icon_style2h_tag = ET.SubElement(icon_style2h_tag,"scale").text = "1"
icon2_style2h_tag  = ET.SubElement(icon_style2h_tag,"Icon")
href_icon2h_tag = ET.SubElement(icon2_style2h_tag, "href").text = "https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png"
hotspot_icon2h_tag = ET.SubElement(icon_style2h_tag,"hotSpot", {
  "x" : "32",
  "xunits" : "pixels",
  "y" : "64",
  "yunits" : "insetPixels"
})
label_icon2h_tag = ET.SubElement(style2h_icon_start_tag, "LabelStyle")
scale_label_icon2_tag = ET.SubElement(label_icon2h_tag, "scale").text = "0"

style_map_tag = ET.SubElement(document_tag,"StyleMap", {
  "id":  "icon-1899-C2185B"
})
pair_tag = ET.SubElement(style_map_tag,"Pair")
key_tag = ET.SubElement(pair_tag, "key").text = "normal"
style_url_map_tag = ET.SubElement(pair_tag, "styleUrl").text = "#icon-1899-C2185B-normal"

pair2_tag = ET.SubElement(style_map_tag,"Pair")
key2_tag = ET.SubElement(pair2_tag, "key").text = "highlight"
style_url_map2_tag = ET.SubElement(pair2_tag, "styleUrl").text = "#icon-1899-C2185B-highlight"
###

folder_tag = ET.SubElement(document_tag,"Folder")
name_folder_tag = ET.SubElement(folder_tag,"name").text = "Tracks"
description_folder_tag = ET.SubElement(folder_tag,"description").text = "A list of tracks"
visibilty_folder_tag = ET.SubElement(folder_tag,"visibility").text = "1"
open_folder_tag = ET.SubElement(folder_tag,"open").text = "1"

placemark_tag = ET.SubElement(folder_tag,"Placemark")
visibilty_placemark_tag = ET.SubElement(placemark_tag,"visibility").text ="0"
open_placemark_tag  = ET.SubElement(placemark_tag,"open").text = "0"
style_url_tag = ET.SubElement(placemark_tag,"styleUrl").text = "#red"
name_placemark_tag = ET.SubElement(placemark_tag,"name").text = name_race
description_placemark_tag = ET.SubElement(placemark_tag,"description").text ="Distance: "+ str(dist_km)+ " km"  + "\nDuration: " + str(race_duration) + "\nStar Time: " + start_point_description+ "\nFinish Time: "+ finish_point_description  +"\nAverage speed: " + average_speed_min_km
line_string_tag = ET.SubElement(placemark_tag,"LineString")
extrude_tag = ET.SubElement(line_string_tag,"extrude").text = "true"
tessellate_tag = ET.SubElement(line_string_tag,"tessellate").text = "true"
altitude_mode_tag = ET.SubElement(line_string_tag,"altitudeMode").text = "clampToGround"
coordinates_tag = ET.SubElement(line_string_tag, "coordinates").text= coordinates


placemark2_tag = ET.SubElement(folder_tag,"Placemark")
name_placemark2_tag = ET.SubElement(placemark2_tag,"name").text = "Start Line"
style2_url_tag = ET.SubElement(placemark2_tag,"styleUrl").text="#icon-1899-C2185B"
point_tag = ET.SubElement(placemark2_tag,"Point")
description_point_tag = ET.SubElement(placemark2_tag,"description").text = start_point_description
point_coordinates_tag = ET.SubElement(point_tag, "coordinates").text = start_point

placemark3_tag = ET.SubElement(folder_tag,"Placemark")
name_placemark3_tag = ET.SubElement(placemark3_tag,"name").text = "Finish Line"
style3_url_tag = ET.SubElement(placemark3_tag,"styleUrl").text="#icon-1899-0F9D58"
point2_tag = ET.SubElement(placemark3_tag,"Point")
description_point2_tag = ET.SubElement(placemark3_tag, "description").text = finish_point_description
point2_coordinates_tag = ET.SubElement(point2_tag, "coordinates").text = finish_point

tree = ET.ElementTree(root)

#Pretty kml
xml_str = ET.tostring(root, encoding='unicode')
dom = minidom.parseString(xml_str)

formatted_xml = dom.toprettyxml(indent='  ', newl='\n', encoding=None)

#File Output Path 
file_path = os.path.splitext(args.file)[0] +'.kml'

# Write the formatted XML to the file
with open(file_path, 'w') as f:
    f.write(formatted_xml)

