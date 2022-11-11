import loggibud.v1.baselines.shared.ortools as ortools
from typing import List, Optional
from loggibud.v1.distances import OSRMConfig
from loggibud.v1.eval.task1 import evaluate_solution
from loggibud.v1.types import CVRPInstance, CVRPSolution
from src.types import CHVRPInstance, CHVRPSolution


def generate_solutions(instances: List[CHVRPInstance], osrm_config: Optional[OSRMConfig]) -> List[CHVRPSolution]:
  ortools_params = ortools.ORToolsParams(osrm_config=osrm_config)
  chvrp_solutions = []
  for instance in instances:
    solutions = [ortools.solve(CVRPInstance(origin=instance.hub.location, vehicle_capacity=instance.vehicle_capacity, deliveries=deliveries, name="", region=""), ortools_params) for deliveries in instance.deliveries_per_day]
    chvrp_solutions.append(CHVRPSolution(hub_id=instance.hub.id, solutions_per_day=solutions))
  return chvrp_solutions


