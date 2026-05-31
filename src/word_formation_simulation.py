import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import *

class WordFormationSimulation:
    """
    A unified simulation environment to model and reproduce 
    "The Evolution of Language".
    It models:
      - 1: Protolanguage error limits (1 sound = 1 object)
      - 2: Word formation without context (Word length l=2)
      - 3: Word formation with contextual lexicon matching
    """
    def __init__(self, n_objects, epsilon):
        self.n_objects = n_objects
        self.epsilon = epsilon
        
        # Environmental context: objects ranked by declining value 
        self.object_values = np.linspace(1.0, 0.01, n_objects)

    def _sum_values_up_to(self, limit):
        k = int(min(limit, self.n_objects))
        return np.sum(self.object_values[:k])

    def calculate_3a_fitness(self, m_sounds):
        """
        F = [1 + (m-1)*epsilon]^-1 * sum(a_i) from i=1 to m
        """
        total_val = self._sum_values_up_to(m_sounds)
        denominator = 1.0 + (m_sounds - 1) * self.epsilon
        return total_val / denominator

    def calculate_3b_fitness(self, m_sounds, target_objects):
        """
        F = [1 + (m-1)*epsilon]^-2 * sum(a_i) up to min(m^2, target_objects)
        """
        vocab_capacity = m_sounds ** 2
        active_words = min(vocab_capacity, target_objects)
        total_val = self._sum_values_up_to(active_words)
        denominator = (1.0 + (m_sounds - 1) * self.epsilon) ** 2
        return total_val / denominator

    def calculate_3c_fitness(self, m_sounds, active_lexicon_size):
        """
        Adapts word similarity penalties dynamically based on how much of the
        total word space (m^2) is utilized by active lexicon words.
        """
        if active_lexicon_size == 0:
            return 0.0
        
        total_possible_words = m_sounds ** 2
        saturation = active_lexicon_size / total_possible_words
        
        # Raw phonetic noise penalty for word length l=2
        noise_factor = (1.0 + (m_sounds - 1) * self.epsilon) ** 2
        
        # Linearly scales down background acoustic error when matched against a lean lexicon
        adjusted_denominator = 1.0 + (noise_factor - 1.0) * saturation
        
        total_val = self._sum_values_up_to(active_lexicon_size)
        return total_val / adjusted_denominator

    def run_simulation_and_plot(self):

        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        objects_range = np.arange(1, self.n_objects + 1)
        
        # Plot 1: Protolanguage (No Word Formation)
        fitness_a = [self.calculate_3a_fitness(m) for m in objects_range]
        
        axes[0].plot(objects_range, fitness_a, color='steelblue', lw=2)
        axes[0].set_title("(a) Without Word Formation")
        axes[0].set_xlabel("Num of Objects")
        axes[0].set_ylabel("Payoff")
        axes[0].set_xlim(1, self.n_objects)
        axes[0].grid(True, alpha=0.2)
        
        max_y_a = max(fitness_a)
        peak_m_a = objects_range[np.argmax(fitness_a)]
        axes[0].axvline(peak_m_a, color='red', linestyle='--', alpha=0.7)
        axes[0].text(peak_m_a + 2, max_y_a * 0.85, f"Optimum m={peak_m_a}", fontsize=9)
        axes[0].set_ylim(0, max_y_a * 1.1)

        # Plot 2: Word Formation (Length l = 2)
        max_y_b = 0.0
        # Plots independent evaluation curves for sound repertoires m = 3 through 10
        for m in range(3, 11):
            fitness_b_curve = []
            for obj in objects_range:
                f = self.calculate_3b_fitness(m_sounds=m, target_objects=obj)
                fitness_b_curve.append(f)
            
            # Bound the plot line to the maximum structural capacity (m^2) of that specific pool
            max_vocab = m ** 2
            valid_curve = fitness_b_curve[:max_vocab]
            max_y_b = max(max_y_b, max(valid_curve))  # Track absolute maximum for y-lim scaling
            
            axes[1].plot(objects_range[:max_vocab], valid_curve, color='steelblue', lw=1.5)
            axes[1].text(max_vocab - 3, valid_curve[-1] + 0.2, str(m), fontsize=9)

        axes[1].set_title("(b) Word Formation (l=2)")
        axes[1].set_xlabel("Num of Objects")
        axes[1].set_ylabel("Payoff")
        axes[1].set_xlim(1, self.n_objects)
        axes[1].grid(True, alpha=0.2)        
        axes[1].set_ylim(0, max_y_b * 1.1)

        # Plot 3: Contextual Lexicon Verification
        # Emulates the paper's optimized sound pool profile (m = 11 phonemes)
        m_c = 11 
        fitness_c = [self.calculate_3c_fitness(m_sounds=m_c, active_lexicon_size=obj) for obj in objects_range]
        
        axes[2].plot(objects_range, fitness_c, color='steelblue', lw=2)
        axes[2].set_title("(c) Lexicon Context Recognition")
        axes[2].set_xlabel("Num of Objects")
        axes[2].set_ylabel("Payoff")
        axes[2].set_xlim(1, self.n_objects)
        axes[2].grid(True, alpha=0.2)
        
        max_y_c = max(fitness_c)
        peak_obj_c = objects_range[np.argmax(fitness_c)]
        axes[2].axvline(peak_obj_c, color='red', linestyle='--', alpha=0.7)
        axes[2].text(peak_obj_c + 2, max_y_c * 0.85, f"Optimum words={peak_obj_c}", fontsize=9)  
        axes[2].set_ylim(0, max_y_c * 1.1)

        plt.tight_layout()
        save_plot(f"word_formation_simulation.png")
        # plt.show()