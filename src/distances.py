from dataclasses import dataclass
from typing import Iterable, Optional
from loggibud.v1.types import Delivery, Point
from loggibud.v1.distances import OSRMConfig, calculate_distance_matrix_great_circle_m
from src.types import Hub

import requests
import numpy as np


def calculate_distance_matrix_fastest_route_m(
  hubs: Iterable[Hub], deliveries: Iterable[Delivery], config: Optional[OSRMConfig]
):
  config = config or OSRMConfig()

  if len(deliveries) < 1 or len(hubs) < 1:
    return 0

  points = [hub.location for hub in hubs] + [delivery.point for delivery in deliveries]

  coords_uri = ";".join(
    ["{},{}".format(point.lng, point.lat) for point in points]
  )

  sources = ";".join(
    [str(i) for i in range(len(hubs))]
  )

  destinations = ";".join(
    [str(i) for i in range(len(hubs), len(deliveries)+len(hubs))]
  )

  response = requests.get(
    f"{config.host}/table/v1/driving/{coords_uri}?annotations=distance&sources={sources}&destinations={destinations}",
    timeout=config.timeout_s,
  )

  response.raise_for_status()

  return np.array(response.json()["distances"])

def calculate_distance_matrix_euclidean_m(
  hubs: Iterable[Hub], deliveries: Iterable[Delivery]
):
  points = [hub.location for hub in hubs] + [delivery.point for delivery in deliveries]

  distance_matrix = calculate_distance_matrix_great_circle_m(points)
  return distance_matrix[:len(hubs), len(hubs):]


  

