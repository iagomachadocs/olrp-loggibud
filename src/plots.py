import folium
import numpy as np
from typing import List
from distinctipy import distinctipy

from loggibud.v1.types import Point, Delivery
from src.types import CHVRPInstance, Hub

def plot_elements(hubs: List[Hub], deliveries: List[Delivery], candidates: List[Hub]):
  points = [delivery.point for delivery in deliveries]
  center_lat = np.mean([p.lat for p in points])
  center_lng = np.mean([p.lng for p in points])

  # create a map
  m = folium.Map(
    location=(center_lat, center_lng),
    zoom_start=11,
    tiles="cartodbpositron",
  )

  for point in points:
    folium.CircleMarker(
      [point.lat, point.lng], popup=point, color="blue", radius=1, weight=4
    ).add_to(m)

  for hub in hubs:
    folium.CircleMarker(
      [hub.location.lat, hub.location.lng], popup=hub, color="black", radius=3, weight=10
    ).add_to(m)

  for candidate in candidates:
    folium.CircleMarker(
      [candidate.location.lat, candidate.location.lng], popup=candidate, color="orange", radius=3, weight=10
    ).add_to(m)

  return m

def plot_instances(instances: List[CHVRPInstance]):
  # create a map
  m = folium.Map(
    location=(instances[0].hub.location.lat, instances[0].hub.location.lng),
    zoom_start=11,
    tiles="cartodbpositron",
  )

  colors = distinctipy.get_colors(len(instances))
  colors = [distinctipy.get_hex(color) for color in colors]

  i = 0
  for instance in instances:

    for delivery in instance.deliveries:
      folium.CircleMarker(
        [delivery.point.lat, delivery.point.lng], popup=delivery, color=colors[i], radius=1, weight=4
      ).add_to(m)
    
    folium.CircleMarker(
      [instance.hub.location.lat, instance.hub.location.lng], popup=instance.hub, color='black', radius=3, weight=10
    ).add_to(m)

    i += 1
  return m

def plot_chvrp_instance(instance: CHVRPInstance):
  points = [delivery.point for delivery in instance.deliveries]
  center_lat = np.mean([p.lat for p in points])
  center_lng = np.mean([p.lng for p in points])

  # create a map
  m = folium.Map(
    location=(center_lat, center_lng),
    zoom_start=11,
    tiles="cartodbpositron",
  )

  colors = distinctipy.get_colors(n_colors=len(instance.deliveries_per_day), exclude_colors=[(1,0.27, 0), (0,0,0), (1,1,1)])
  colors = [distinctipy.get_hex(color) for color in colors]

  for i in range(len(instance.deliveries_per_day)):
    for delivery in instance.deliveries_per_day[i]:
      folium.CircleMarker(
        [delivery.point.lat, delivery.point.lng], popup=delivery, color=colors[i], radius=1, weight=4
      ).add_to(m)

  folium.CircleMarker(
    [instance.hub.location.lat, instance.hub.location.lng], popup=instance.hub, color='black', radius=3, weight=10
  ).add_to(m)

  return m



def plot_distinct_assignments(hubs: List[Hub], candidate: Hub, same_hub_deliveries: List[Delivery], distinct_hub_deliveries: List[Delivery]):
  # create a map
  m = folium.Map(
    location=(candidate.location.lat, candidate.location.lng),
    zoom_start=11,
    tiles="cartodbpositron",
  )


  for delivery in same_hub_deliveries:
    folium.CircleMarker(
      [delivery.point.lat, delivery.point.lng], popup=delivery, color='green', radius=1, weight=4
    ).add_to(m)

  for delivery in distinct_hub_deliveries:
    folium.CircleMarker(
      [delivery.point.lat, delivery.point.lng], popup=delivery, color='red', radius=1, weight=4
    ).add_to(m)

  for hub in hubs:
    folium.CircleMarker(
      [hub.location.lat, hub.location.lng], popup=hub, color='black', radius=3, weight=10
    ).add_to(m)

  folium.CircleMarker(
    [candidate.location.lat, candidate.location.lng], popup=candidate, color='orange', radius=3, weight=10
  ).add_to(m)

  return m

def plot_clusters(hubs: List[Point], candidate: Point, clusters: List[List[Delivery]], centers: List[Point]):
  m = folium.Map(
    location=(hubs[0].lat, hubs[0].lng),
    zoom_start=12,
    tiles="cartodbpositron",
  )

  colors = distinctipy.get_colors(n_colors=len(clusters), exclude_colors=[(0,1,0), (0,0,0), (1,1,1)])
  colors = [distinctipy.get_hex(color) for color in colors]

  for i in range(len(clusters)):
    color = colors[i]

    cluster = clusters[i]
    for delivery in cluster:
      folium.CircleMarker(
        [delivery.point.lat, delivery.point.lng], popup=delivery, color=color, radius=1, weight=4
      ).add_to(m)

    center = centers[i]
    folium.CircleMarker(
      [center.lat, center.lng], popup=delivery, color='green', radius=3, weight=10
    ).add_to(m)

  for hub in hubs + [candidate]:
    folium.CircleMarker(
      [hub.lat, hub.lng], popup=hub, color='black', radius=3, weight=10
    ).add_to(m)

  return m