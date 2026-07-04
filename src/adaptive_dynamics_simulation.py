import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import *

class AdaptiveDynamicsSimulation:
    """
    This class simulates linguistic optimization under acoustic noise constraints.
    It introduces a continuous acoustic spectrum where physical sounds naturally blur
    into neighboring signals based on an exponential perception error matrix (U).
    A dominant resident language is subjected to constant structural mutations (linguistic drift, lexical decay).
    Mutants only overthrow the population if they successfully maximize communication efficiency by pushing
    acoustic signals as far apart as possible, highlighting the mathematical "Error Limit"
    inherent to non-combinatorial systems.
    
    """
    def __init__(self, alpha=2.5, n_objects=8, n_sounds=16):
        
        self.alpha = alpha
        self.n_objects = n_objects
        self.n_sounds = n_sounds

        self.a_objects = np.linspace(1.0, 0.2, n_objects) # generate a list of objects with weights (high -> low)
        self.x_sounds = np.sort(np.random.rand(n_sounds)) # generate random sounds in continuous sound spectrum between 0.0 and 1.0
        self.U = self._build_perception_matrix() # create the perception matrix

        self.P_res = normalize_rows(np.random.rand(n_objects, n_sounds))
        self.Q_res = derive_passive_Q(self.P_res)

    def _build_perception_matrix(self):
        S = np.zeros((self.n_sounds, self.n_sounds))
        for i in range(self.n_sounds):
            for j in range(self.n_sounds):
                S[i, j] = np.exp(-self.alpha * abs(self.x_sounds[i] - self.x_sounds[j])) # physical distance between every pair of sounds on our spectrum
        return S / S.sum(axis=1, keepdims=True)

    def calculate_system_fitness(self, P_speaker, Q_listener, P_listener, Q_speaker):

        # Calculate successful communication probabilities per object (diagonal of the result matrix)
        success_rate_res = np.diag(P_speaker @ self.U @ Q_listener)
        success_rate_mut = np.diag(P_listener @ self.U @ Q_speaker)

        # Multiply by object values 'a' and sum
        term1 = np.sum(self.a_objects * success_rate_res)
        term2 = np.sum(self.a_objects * success_rate_mut)

        return 0.5 * (term1 + term2)

    def generate_mutant(self):
        P_mut = self.P_res.copy()
        P_mut += np.random.uniform(-0.02, 0.02, size=P_mut.shape)
        P_mut = np.clip(P_mut, 0, 1)

        bin_mask = np.random.rand(*P_mut.shape) < 0.005
        P_mut[bin_mask] = np.random.choice([0.0, 1.0], size=np.sum(bin_mask))

        for i in range(self.n_objects):
            if np.random.rand() < 0.002: P_mut[i, :] = 0.0
        for j in range(self.n_sounds):
            if np.random.rand() < 0.002: P_mut[:, j] = 0.0

        P_mut = normalize_rows(P_mut)
        Q_mut = derive_passive_Q(P_mut)
        return P_mut, Q_mut

    def run_simulation(self, total_mutations=30000):

        current_efficiency = -1

        print("Running Adaptive Dynamics Simulation...")
        for step in range(1, total_mutations + 1):
            P_mut, Q_mut = self.generate_mutant()

            F_res_res = self.calculate_system_fitness(self.P_res, self.Q_res, self.P_res, self.Q_res)
            F_mut_res = self.calculate_system_fitness(P_mut, self.Q_res, self.P_res, Q_mut)
            F_mut_mut = self.calculate_system_fitness(P_mut, Q_mut, P_mut, Q_mut)

            if F_mut_mut > F_mut_res > F_res_res:
                self.P_res = P_mut
                self.Q_res = Q_mut

            current_efficiency = (F_res_res / np.sum(self.a_objects)) * 100

        return current_efficiency

    def run_simulation_and_plot(self, total_mutations=30000, plot=False):
        efficiency_history = []
        invasion_points = []

        print("Running Adaptive Dynamics Simulation...")
        for step in range(1, total_mutations + 1):
            P_mut, Q_mut = self.generate_mutant()

            F_res_res = self.calculate_system_fitness(self.P_res, self.Q_res, self.P_res, self.Q_res)
            F_mut_res = self.calculate_system_fitness(P_mut, self.Q_res, self.P_res, Q_mut)
            F_mut_mut = self.calculate_system_fitness(P_mut, Q_mut, P_mut, Q_mut)

            if F_mut_mut > F_mut_res > F_res_res:
                self.P_res = P_mut
                self.Q_res = Q_mut
                invasion_points.append(step)

            current_efficiency = (F_res_res / np.sum(self.a_objects)) * 100
            efficiency_history.append(current_efficiency)

        plt.figure(figsize=(12, 6))
        plt.plot(range(1, total_mutations + 1), efficiency_history, color='purple', label='Information Transfer Efficiency')

        if invasion_points:
            plt.vlines(invasion_points, ymin=min(efficiency_history), ymax=max(efficiency_history),
                       colors='green', alpha=0.15, linestyles='solid', label='Successful Mutant Invasion')

        plt.title(f'Evolutionary Language Game Optimization (Object: {self.n_objects} Sound: {self.n_sounds})')
        plt.xlabel('Mutation Steps / Cycles')
        plt.ylabel('Communication Performance Max Potential (%)')
        plt.legend(loc='lower right')
        plt.grid(True, alpha=0.3)
        save_plot(f"evolutionary_language_game_optimization_{self.n_objects}_{self.n_sounds}.png")
        if plot == True:
            plt.show()

        n_objects, n_sounds = self.P_res.shape
        x, y = np.meshgrid(np.arange(n_sounds), np.arange(n_objects))
        x_flat = x.flatten()
        y_flat = y.flatten()
        sizes_flat = self.P_res.flatten()

        plt.figure(figsize=(12, 6))

        scatter = plt.scatter(
            x_flat,
            y_flat,
            s=sizes_flat * 1200,
            c=sizes_flat,
            cmap='YlGnBu',
            alpha=0.75,
            edgecolors='black'
        )

        plt.title(f'Optimized Active Language Profile (Object: {n_objects} Sound: {n_sounds})', fontsize=14)
        plt.xlabel('Acoustic Spectrum Signal Channels', fontsize=12)
        plt.ylabel('Observed Objects', fontsize=12)

        plt.xticks(np.arange(n_sounds))
        plt.yticks(np.arange(n_objects))

        plt.colorbar(scatter, label='Selection Probability')
        plt.grid(True, linestyle='--', alpha=0.3)

        plt.tight_layout()
        save_plot(f"optimized_active_language_profile_{self.n_objects}_{self.n_sounds}.png")
        if plot == True:
            plt.show()
