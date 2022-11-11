from typing import Literal, List, Optional
from loggibud.v1.distances import OSRMConfig
from src.types import CHVRPInstance
from src.distances import calculate_distance_matrix_fastest_route_m, calculate_distance_matrix_euclidean_m
from loggibud.v1.types import Delivery


def get_total_size(deliveries: List[Delivery]) -> int:
  return sum([d.size for d in deliveries])


def split_into_days(instance: CHVRPInstance, distance_metric: Literal['euclidean', 'road_network'], osrm_config: Optional[OSRMConfig]):
  if(distance_metric == 'euclidean'):
    distance_matrix = calculate_distance_matrix_euclidean_m([instance.hub], instance.deliveries)
  else:
    distance_matrix = calculate_distance_matrix_fastest_route_m([instance.hub], instance.deliveries, osrm_config)
  
  deliveries_with_distance = []
  for i in range(len(instance.deliveries)):
    deliveries_with_distance.append((distance_matrix[0][i], instance.deliveries[i]))

  deliveries_with_distance.sort(key=lambda tup: tup[0])
  sorted_deliveries = [distance_delivery[1] for distance_delivery in deliveries_with_distance]

  instance.deliveries_per_day = [[]]
  for delivery in sorted_deliveries:
    fit = False

    # Tries to put the delivery in one of the existing sets
    for deliveries_day in instance.deliveries_per_day:
      total_size = sum([d.size for d in deliveries_day])
      if(total_size + delivery.size <= instance.hub.capacity):
        fit = True
        deliveries_day.append(delivery)
        break
    
    # Creates a new set of deliveries 
    if(not fit):
      instance.deliveries_per_day.append([delivery])

  

  
  