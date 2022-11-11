from loggibud.v1.types import CVRPInstance, Point
from loggibud.v1.distances import OSRMConfig, calculate_distance_matrix_m
import random
import time

from src.solver import solve
from src.types import OLRPInstance, Hub


if __name__ == "__main__":
  # http://router.project-osrm.org
  # http://ec2-34-222-175-250.us-west-2.compute.amazonaws.com
  osrm_config = OSRMConfig(host="http://localhost:5000")

  # Load instances from files
  hubs = []
  deliveries = []
  file_path = "./data/cvrp-instances-1.0/dev/rj-{}/cvrp-{}-rj-90.json"
  for i in range(6):
    instace = CVRPInstance.from_file(file_path.format(i, i))
    hubs.append(instace.origin)
    deliveries = deliveries + instace.deliveries

  hubs = hubs[:3]
  for i in range(len(hubs)):
    hubs[i] = Hub(id=f'h{i}', location=hubs[i], capacity=1000)

  random.seed(6)
  deliveries = random.sample(deliveries, 1000)

  candidate1 = Hub(id='c1', location=Point(-43.45709100057598, -23.013786746112544), capacity=1000)
  candidate2 = Hub(id='c2', location=Point(-43.507709885731735, -22.87962438443935), capacity=1000)
  candidate3 = Hub(id='c3', location=Point(-43.12324223148901, -22.88506575654086), capacity=1000)

  candidates = [candidate1, candidate2, candidate3]

  instance = OLRPInstance(region='rj', vehicle_capacity=180, deliveries=deliveries, hubs=hubs, candidates=candidates)

  solution = solve(instance, 'euclidean', 'cluster', osrm_config)

  print(solution)

