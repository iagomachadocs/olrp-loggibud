import math
import numpy as np
from typing import List, Literal, Optional
from sklearn_extra.cluster import KMedoids

from loggibud.v1.types import Point, Delivery
from loggibud.v1.distances import OSRMConfig, calculate_distance_matrix_great_circle_m, calculate_route_distance_m

from src.types import CHVRPInstance, Hub
from src.distances import calculate_distance_matrix_fastest_route_m, calculate_distance_matrix_euclidean_m

def euclidean_distance(a: Point, b: Point) -> float:
  distance_matrix = calculate_distance_matrix_great_circle_m([a, b])
  return distance_matrix[0][1]

def road_network_distance(a: Point, b: Point) -> float:
  return calculate_route_distance_m([a, b])


def min_dist_assignment(
  hubs: List[Hub], deliveries: List[Delivery], vehicle_capacity: int, distance_metric:  Literal['euclidean', 'road_network'], osrm_config: Optional[OSRMConfig]
) -> List[CHVRPInstance]:

  if(distance_metric == 'euclidean'):
    distance_matrix = calculate_distance_matrix_euclidean_m(hubs, deliveries)
  else:
    distance_matrix = calculate_distance_matrix_fastest_route_m(hubs, deliveries, osrm_config)

  instances = [CHVRPInstance(hub=hub, vehicle_capacity=vehicle_capacity, deliveries=[], deliveries_per_day=[]) for hub in hubs]
  
  for i in range(len(deliveries)):
    distances = distance_matrix[:, i]
    nearest_hub_index = np.argmin(distances)

    nearest_instance = instances[nearest_hub_index]
    nearest_instance.deliveries.append(deliveries[i])
  
  return instances

def cluster_assignment(hubs: List[Hub], deliveries: List[Delivery], vehicle_capacity: int, distance_metric: Literal['euclidean', 'road_network'], osrm_config: Optional[OSRMConfig]):
  points = np.array(
    [[d.point.lng, d.point.lat] for d in deliveries]
  )
  total_size = sum([d.size for d in deliveries])
  num_clusters = math.ceil(total_size/vehicle_capacity)
  
  clustering = KMedoids(n_clusters=num_clusters, random_state=0)
  clusters = clustering.fit_predict(points)

  delivery_array = np.array(deliveries)

  clusters_deliveries = [
    delivery_array[clusters == i].tolist() for i in range(num_clusters)
  ]

  centers = [Point(lng=p[0], lat=p[1]) for p in clustering.cluster_centers_]

  instances = [CHVRPInstance(hub=hub, vehicle_capacity=vehicle_capacity, deliveries=[], deliveries_per_day=[]) for hub in hubs]

  if(distance_metric == 'euclidean'):
    distance_matrix = calculate_distance_matrix_euclidean_m(hubs, deliveries)
  else:
    distance_matrix = calculate_distance_matrix_fastest_route_m(hubs, deliveries, osrm_config)

  def __find_delivery_index(point: Point, deliveries: List[Delivery]) -> int:
    for i in range(len(deliveries)):
      if deliveries[i].point == point:
        return i

  for i in range(num_clusters):
    center = centers[i]
    center_index = __find_delivery_index(center, delivery_array)

    distances = distance_matrix[:, center_index]
    nearest_hub_index = np.argmin(distances)
    
    nearest_instance = instances[nearest_hub_index]
    nearest_instance.deliveries = nearest_instance.deliveries + clusters_deliveries[i]
  
  return (instances, clusters_deliveries, centers)









  
  



