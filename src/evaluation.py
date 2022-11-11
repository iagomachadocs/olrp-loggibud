from typing import List, Optional
from loggibud.v1.distances import OSRMConfig, calculate_route_distance_m
from src.types import CHVRPInstance, CHVRPSolution

def check_deliveries(instance: CHVRPInstance, solution: CHVRPSolution):
  # Check if all deliveries are present
  for i in range(len(instance.deliveries_per_day)):
    cvrp_solution = solution.solutions_per_day[i]
    solution_demands = set(d for v in cvrp_solution.vehicles for d in v.deliveries)
    assert solution_demands == set(instance.deliveries_per_day[i])

def check_vehicles(instance: CHVRPInstance, solution: CHVRPSolution):
  for solution_day in solution.solutions_per_day:
    # Check if max vehicle capacity is respected
    max_capacity = max(
      sum(d.size for d in v.deliveries) for v in solution_day.vehicles
    )
    assert max_capacity <= instance.vehicle_capacity

    # Check if maximum number of origins is consistent.
    origins = set([v.origin for v in solution_day.vehicles])
    assert len(origins) <= 1

def check_hub_capacity(instance: CHVRPInstance, solution: CHVRPSolution):
  for solution_day in solution.solutions_per_day:
    # Check if max hub capacity is respected
    total_size = sum(
      sum(d.size for d in v.deliveries) for v in solution_day.vehicles
    )

    assert total_size <= instance.hub.capacity

def calculate_total_distance_km(solution: CHVRPSolution, osrm_config: Optional[OSRMConfig]) -> float:
  total_distance = 0
  for solution_day in solution.solutions_per_day:
    route_distances_m = [
      calculate_route_distance_m(v.circuit, osrm_config)
      for v in solution_day.vehicles
    ]
    total_distance += sum(route_distances_m)
  
  return round(total_distance/ 1_000, 4)


def evaluate_olrp_solution(instances: List[CHVRPInstance], solutions: List[CHVRPSolution], osrm_config: Optional[OSRMConfig]) -> float:
  total_distance = 0
  for i in range(len(instances)):
    instance = instances[i]
    solution = solutions[i]
    
    check_deliveries(instance, solution)
    check_vehicles(instance, solution)
    check_hub_capacity(instance, solution)

    total_distance += calculate_total_distance_km(solution, osrm_config)
  return total_distance

      
      
      