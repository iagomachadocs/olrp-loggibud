from dataclasses import dataclass

from loggibud.v1.types import CVRPSolution, Point, Delivery
from typing import List

@dataclass
class Hub:
  id: str
  """Unique identifier"""

  location: Point
  """Location of the hub"""

  capacity: int
  """Maximum sum of sizes allowed per solution."""

@dataclass
class OLRPInstance:
  region: str
  """Region of this instance."""

  vehicle_capacity: int
  """Maximum sum of sizes per vehicle allowed in the solution."""

  deliveries: List[Delivery]
  """List of deliveries to be solved."""

  hubs: List[Hub]
  """List of existent hubs"""

  candidates: List[Hub]
  """List of hub candidates"""


@dataclass
class CHVRPInstance:
  """A CVRP instance that has limitations in the hub capacity"""

  hub: Hub
  """Hub of this instance"""

  vehicle_capacity: int
  """Maximum sum of sizes per vehicle allowed in the solution."""

  deliveries: List[Delivery]
  """List of deliveries to be solved."""

  deliveries_per_day: List[List[Delivery]]
  """List of deliveries splitted according to hub capacity"""



@dataclass
class CHVRPSolution:
  hub_id: str
  solutions_per_day: List[CVRPSolution]

  @property
  def deliveries(self):
    return [d for s in self.solutions for d in s.deliveries]


@dataclass
class OLRPSolution:
  candidate_id: str
  solutions: List[CHVRPSolution]
  total_route_distance_km: float

  @property
  def deliveries(self):
    return [d for s in self.solutions for d in s.deliveries]