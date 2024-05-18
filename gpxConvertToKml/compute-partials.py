import gpxpy
import gpxpy.gpx
import argparse
import os
import math
from utils import *

parser = argparse.ArgumentParser(description='Convert a GPX to KML for using in Google Maps')
parser.add_argument("-f", "--file", type=str,help="gpx file to be converted", required=True)
parser.add_argument("-n", "--name", type=str,help="name of race track", required=True)

args = parser.parse_args()

name_race = os.path.splitext(args.name)[0]

gpx_file = open(args.file, 'r')

gpx = gpxpy.parse(gpx_file)

segments = gpx.tracks[0].segments

#Compute total distance iterating points for each segment and save each point in a sample.txt file
dis = 0
txt_points =''
for i in range(len(segments)-1):
  dis += segments[i].points[0].distance_2d(segments[i+1].points[0])
  txt_points= txt_points + 'id_segment: '+str(i)+'-'+str(segments[i].points[0])+'\n'
n =  len(segments)-1
txt_points = txt_points + 'id_segment: '+str(n)+'-'+str(segments[n].points[0])+'\n'

dist_km = dis/1000

dist_km_int = int(dist_km)

# Open text file in write mode
text_file = open("sample.txt", "w")

# Take content
content = txt_points

# Write content to file
n = text_file.write(content)

if n == len(content):
    print("Success! String written to text file.")
else:
    print("Failure! String not written to text file.")

# Close file
text_file.close()

print('Distancia Total carrera: '+ str(dist_km))
print('Cantidad de puntos medidos: ' + str(len(segments)))


dist_km_int = int(dist_km)
print('Distancia en KM enteros: '+ str(dist_km_int))


num_km = range (1, dist_km_int + 1)


seg_ini = 0
dist_actual = 0
dist_total =0
for h in num_km:
  i = seg_ini
  
  while dist_actual < 1000 and i < len(segments)-1 :   
    dist_actual += segments[i].points[0].distance_2d(segments[i+1].points[0])
    #print('id_segment: '+str(i)+'-'+str(segments[i].points[0]))
    #print('Distancia actual: '+ str(dist_actual/1000))
    i=i+1

  seg_fin = i
  dist_total += dist_actual
  #print('KM:'+ str(h))
  #print('Segmento inicial del tramo: '+ str(seg_ini))
  #print('Segmento final del tramo: '+ str(seg_fin))
  #print('Distancia del tramo: '+ str(dist_actual/1000))
  #print('Distancia Acumulada: '+ str(dist_total/1000))

  time_dif_seconds = gpx.tracks[0].segments[seg_ini].points[0].time_difference(gpx.tracks[0].segments[seg_fin].points[0])

  #Compute average speed in meters / seconds
  average_speed = average_speed_m_s(dist_actual,time_dif_seconds)

  #average_speed_min_km = average_speed_m_k(average_speed)

  #average_speed_min_km = average_speed_m_s_txt(average_speed_min_km)
  
  #Convert average speed in min / km
  average_speed_min_km2 =average_speed2_m_k(average_speed)
  
  #print('Ritmo medio: '+ average_speed_min_km)
  #print(average_speed_m_k(average_speed))
  #print( average_speed_m_s_txt(average_speed_m_k(average_speed)))
  print('KM'+ str(h) +' ' +average_speed_min_km2)
  
  seg_ini = seg_fin 
  dist_actual = 0

meters_race = dist_km - dist_km_int

if meters_race > 0.1:

  for i in range (seg_ini,len(segments)-1):   
    dist_actual += segments[i].points[0].distance_2d(segments[i+1].points[0])

  dist_last_segment = dist_actual
    
  time_dif_seconds_last_segment = gpx.tracks[0].segments[seg_ini].points[0].time_difference(gpx.tracks[0].segments[len(segments)-1].points[0])

  #Compute average speed in meters / seconds
  average_speed = average_speed_m_s(dist_last_segment,time_dif_seconds_last_segment)

  #Convert average speed in min / km
  average_speed_min_km = average_speed2_m_k(average_speed)

  print(str(int(dist_last_segment)) + ' metros finales '+ str(average_speed_min_km))
  #print('Segmento inicial del tramo: '+ str(seg_ini))
  #print('Segmento final del tramo: '+ str(len(segments)-1))
  #print('Distancia del tramo: '+ str(dist_last_segment))

  #average_speed_min_km = average_speed_m_s_txt(average_speed_min_km)
  


#print('Distancia Total: '+ str((dist_total+dist_last_segment)/1000))
#print('Metros restantes: '+ str(meters_race))


