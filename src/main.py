from protolang_simulation import ProtolanguageSimulation
from adaptive_dynamics_simulation import AdaptiveDynamicsSimulation

if __name__ == "__main__":
    proto_experiment = ProtolanguageSimulation(n_pop=100, n_objects=5, n_signals=5, sample_size=12)
    proto_experiment.run_simulation_and_plot(generations=50)

    adaptive_experiment = AdaptiveDynamicsSimulation(alpha=2.5, n_objects=10, n_sounds=20)
    adaptive_experiment.run_simulation_and_plot(total_mutations=50000)
