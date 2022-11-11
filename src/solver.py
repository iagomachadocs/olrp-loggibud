from typing import Literal, List, Optional
from loggibud.v1.distances import OSRMConfig

from src.evaluation import evaluate_olrp_solution
from src.split import split_into_days
from src.types import OLRPInstance, OLRPSolution, CHVRPInstance
from src.delivery_assignment import min_dist_assignment, cluster_assignment
from src.routes_generation import generate_solutions



def solve(instance: OLRPInstance, distance_metric: Literal['euclidean', 'road_network'], assignment_heuristic: Literal['min_dist', 'cluster'], osrm_config: Optional[OSRMConfig]) -> OLRPSolution:
  chvrp_instances_per_candidate: List[tuple(str, List[CHVRPInstance])]
  # Assignment
  if(assignment_heuristic == 'min_dist'):
    chvrp_instances_per_candidate = []
    for candidate in instance.candidates:
      instances = min_dist_assignment(instance.hubs + [candidate], instance.deliveries, instance.vehicle_capacity, distance_metric, osrm_config)
      chvrp_instances_per_candidate.append((candidate.id, instances))
  else:
    chvrp_instances_per_candidate = []
    for candidate in instance.candidates:
      (instances, clusters, centers) = cluster_assignment(instance.hubs + [candidate], instance.deliveries, instance.vehicle_capacity, distance_metric, osrm_config)
      chvrp_instances_per_candidate.append((candidate.id, instances))

  # Split
  for (candidate_id, chvrp_instances) in chvrp_instances_per_candidate:
    for chvrp_instance in chvrp_instances:
      split_into_days(chvrp_instance, distance_metric, osrm_config)

  # Route generation
  chvrp_solutions_per_candidate = [(candidate_id, generate_solutions(instances, osrm_config)) for (candidate_id, instances) in chvrp_instances_per_candidate]

  # Calculate route distances
  olrp_solutions: List[OLRPSolution] = []
  for i in range(len(chvrp_instances_per_candidate)):
    candidate_id, instances = chvrp_instances_per_candidate[i]
    _, solutions = chvrp_solutions_per_candidate[i]

    total_route_distance_km = evaluate_olrp_solution(instances, solutions, osrm_config)

    olrp_solution = OLRPSolution(candidate_id, solutions, total_route_distance_km)

    olrp_solutions.append(olrp_solution)

  # Get best candidate
  olrp_solutions.sort(key=lambda solution: solution.total_route_distance_km)
  return olrp_solutions[0]
