import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import *

class ProtolanguageSimulation:
    """
    This class simulates cultural language convergence in a finite population.
    It models a multi-agent evolutionary game where individuals interact blindly
    using randomized signaling matrices (P and Q). Over successive generations, agents
    reproduce proportionally to their communication success (fitness). Offspring acquire
    language by sampling finite communication patterns from their parents, introducing
    transmission noise. This demonstrates how a population can naturally self-organize
    and converge on a shared, cohesive protolanguage without central authority.
    """
    def __init__(self, n_pop=100, n_objects=5, n_signals=5, sample_size=15):
        self.n_pop = n_pop
        self.n_objects = n_objects
        self.n_signals = n_signals
        self.sample_size = sample_size

        self.population = []
        for _ in range(self.n_pop):
            # Normalise values to represent the probabilities
            P = normalize_rows(np.random.rand(n_objects, n_signals))
            Q = normalize_rows(np.random.rand(n_signals, n_objects))
            self.population.append({'P': P, 'Q': Q})

    def calculate_pairwise_payoff(self, ind_A, ind_B):
        term1 = np.sum(ind_A['P'] * ind_B['Q'].T)
        term2 = np.sum(ind_B['P'] * ind_A['Q'].T)
        return 0.5 * (term1 + term2) / self.n_objects

    def evaluate_population_fitness(self):
        payoffs = np.zeros(self.n_pop)
        # Calculate the pairwise fitness payoff with the whole population
        for i in range(self.n_pop):
            for j in range(self.n_pop):
                if i != j:
                    payoffs[i] += self.calculate_pairwise_payoff(self.population[i], self.population[j])
        return payoffs / (self.n_pop - 1)

    def reproduce_and_sample(self, parent_matrices):
        child_P = np.zeros((self.n_objects, self.n_signals))
        child_Q = np.zeros((self.n_signals, self.n_objects))

        # sample from parents for P(Listener) matrix
        for i in range(self.n_objects):
            sampled_signals = np.random.choice(self.n_signals, size=self.sample_size, p=parent_matrices['P'][i])
            for sig in sampled_signals: child_P[i, sig] += 1

        # sample from parents for Q(Receiver) matrix
        for j in range(self.n_signals):
            sampled_objects = np.random.choice(self.n_objects, size=self.sample_size, p=parent_matrices['Q'][j])
            for obj in sampled_objects: child_Q[j, obj] += 1

        return {'P': normalize_rows(child_P), 'Q': normalize_rows(child_Q)}

    def step_generation(self):
        fitness_scores = self.evaluate_population_fitness()
        avg_fitness = np.mean(fitness_scores)

        selection_probs = (fitness_scores - fitness_scores.min() + 1e-6)
        selection_probs /= selection_probs.sum()
        parent_indices = np.random.choice(self.n_pop, size=self.n_pop, p=selection_probs)

        next_gen = []
        for idx in parent_indices:
            next_gen.append(self.reproduce_and_sample(self.population[idx]))

        self.population = next_gen
        return avg_fitness

    def run_simulation_and_plot(self, generations=30):

        fitness_history = []
        coherence_history = []
        avg_P = []

        print("Running Protolanguage Simulation...")
        for g in range(1, generations + 1):
            avg_fit = self.step_generation()
            fitness_history.append(avg_fit)

            all_P = np.array([ind['P'] for ind in self.population])
            avg_P.append(np.mean(all_P, axis=0))
            coherence = 1.0 - np.mean(np.var(all_P, axis=0))
            coherence_history.append(coherence)

        fig, ax1 = plt.subplots(figsize=(10, 5))

        color = 'tab:blue'
        ax1.set_xlabel('Generation')
        ax1.set_ylabel('Avg Communication Efficiency (Fitness)', color=color)
        ax1.plot(range(1, generations + 1), fitness_history, color=color, linewidth=2.5, label='Fitness')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, linestyle='--', alpha=0.6)

        ax2 = ax1.twinx()
        color = 'tab:orange'
        ax2.set_ylabel('Language Matrix Alignment (Coherence)', color=color)
        ax2.plot(range(1, generations + 1), coherence_history, color=color, linewidth=2.5, linestyle='--', label='Coherence')
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title('Emergence of Protolanguage Fitness and Cohesion Over Generations')
        fig.tight_layout()

        save_plot("protolanguage_fitness_coherence.png")

        # plt.show()

        fig, axes = plt.subplots(3, 2, figsize=(10, 12))
        axes = axes.flatten()
        m = self.n_objects
        n = self.n_signals
        x, y = np.meshgrid(np.arange(m), np.arange(n))

        for idx, ax in enumerate(axes):

            mat = avg_P[idx * 5]
            title = f"P matrix at time {idx * 5}"
            scatter = ax.scatter(x, y[::-1], s=mat*500, alpha=0.6, edgecolors='black')
            ax.set_xticks(np.arange(m))
            ax.set_yticks(np.arange(n))
            ax.set_xticklabels([f"Sound {i + 1}" for i in range(m)])
            ax.set_yticklabels([f"Object {i + 1}" for i in range(n)][::-1])
            ax.set_xlim(-0.5, 4.5)
            ax.set_ylim(-0.5, 4.5)
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.set_title(title, fontsize=14)

        plt.tight_layout()
        save_plot("emergence_of_protolanguage.png")

        # plt.show()
