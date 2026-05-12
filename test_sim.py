from simulator import RobotSimulator
from trajectories import get_trajectory

sim = RobotSimulator()

path = get_trajectory("A", scale=140, offset=(350, 220))
sim.load_trajectory("A", path)

while sim.is_running():
    sim.step()

sim.close()