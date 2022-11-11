from typing import List
from loggibud.v1.types import Delivery
from src.types import CHVRPInstance

def _find_instance_containing_delivery(instances: List[CHVRPInstance], delivery: Delivery):
  for instance in instances:
    if delivery in instance.deliveries:
      return instance

def calculate_percentage_of_distinct_assignments(same_hub_deliveries: int, distinct_hub_deliveries: int) -> float:
  percentage = (distinct_hub_deliveries / (distinct_hub_deliveries + same_hub_deliveries)) * 100
  return percentage

def identify_distinct_assignments(euclidean_instances: List[CHVRPInstance], road_network_instances: List[CHVRPInstance]):
  same_hub_deliveries = []
  distinct_hub_deliveries = []

  for instance in euclidean_instances:
    for delivery in instance.deliveries:
      rn_instance = _find_instance_containing_delivery(road_network_instances, delivery)
      if rn_instance.hub == instance.hub:
        same_hub_deliveries.append(delivery)
      else:
        distinct_hub_deliveries.append(delivery)

  return same_hub_deliveries, distinct_hub_deliveries