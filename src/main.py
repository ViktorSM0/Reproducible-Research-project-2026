from protolang_simulation import ProtolanguageSimulation
from adaptive_dynamics_simulation import AdaptiveDynamicsSimulation
from word_formation_simulation  import WordFormationSimulation
import numpy as np

if __name__ == "__main__":

    np.random.seed(12)

    proto_simulation = ProtolanguageSimulation(n_pop=100, n_objects=5, n_signals=5, sample_size=12)
    proto_simulation.run_simulation_and_plot(generations=50)

    adaptive_simulation = AdaptiveDynamicsSimulation(alpha=2.5, n_objects=20, n_sounds=40)
    adaptive_simulation.run_simulation_and_plot(total_mutations=30000)

    word_formation_simulation = WordFormationSimulation(n_objects=100, epsilon=0.2)
    word_formation_simulation.run_simulation_and_plot()
