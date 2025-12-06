"""
Visualization Script for Persona Probability Experiment

Creates compelling visualizations that tell the story of discovery:
1. Initial expectation vs. reality
2. The surprising confidence decrease
3. The deeper insight about probability redistribution
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

class PersonaStoryVisualizer:
    """Creates visualizations that tell the discovery story."""
    
    def __init__(self, output_dir: str = 'visualizations'):
        """Initialize visualizer with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = {
            'without': '#FF6B6B',  # Red for generic
            'with': '#4ECDC4',     # Teal for persona
            'highlight': '#FFE66D', # Yellow for key insights
            'text': '#2C3E50'      # Dark text
        }
    
    def load_results(self):
        """Load experiment results."""
        with open('results_single_token.json', 'r') as f:
            self.single = json.load(f)
        with open('results_multi_token.json', 'r') as f:
            self.multi = json.load(f)
    
    def create_story_narrative(self):
        """Create a 4-panel story visualization."""
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle('The Persona Discovery Journey: From Expectation to Insight', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        # Panel 1: The Expectation
        ax1 = plt.subplot(2, 2, 1)
        self._plot_expectation(ax1)
        
        # Panel 2: The Surprising Result
        ax2 = plt.subplot(2, 2, 2)
        self._plot_surprise(ax2)
        
        # Panel 3: The Deeper Investigation
        ax3 = plt.subplot(2, 2, 3)
        self._plot_investigation(ax3)
        
        # Panel 4: The Powerful Insight
        ax4 = plt.subplot(2, 2, 4)
        self._plot_insight(ax4)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'discovery_journey.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {self.output_dir / 'discovery_journey.png'}")
        plt.close()
    
    def _plot_expectation(self, ax):
        """Panel 1: What we expected."""
        ax.text(0.5, 0.7, '❓ THE EXPECTATION', 
                ha='center', va='center', fontsize=14, fontweight='bold',
                transform=ax.transAxes)
        
        ax.text(0.5, 0.5, 'Hypothesis: Personas should INCREASE\ntoken confidence across the board',
                ha='center', va='center', fontsize=11,
                transform=ax.transAxes, style='italic')
        
        # Simple bar chart showing expected increase
        categories = ['Without\nPersona', 'With\nPersona\n(Expected)']
        expected = [0.75, 0.90]  # Hypothetical expectation
        bars = ax.bar(categories, expected, color=[self.colors['without'], self.colors['highlight']], 
                      alpha=0.7, width=0.6)
        
        # Add arrow showing expected increase
        ax.annotate('', xy=(1, 0.88), xytext=(0, 0.77),
                   arrowprops=dict(arrowstyle='->', lw=2, color=self.colors['highlight']))
        ax.text(0.5, 0.83, 'Expected\nIncrease', ha='center', fontsize=9, 
               color=self.colors['highlight'], fontweight='bold')
        
        ax.set_ylabel('Average Confidence', fontsize=10)
        ax.set_ylim(0, 1.0)
        ax.set_title('We expected personas to boost confidence', fontsize=10, pad=10)
        ax.grid(True, alpha=0.3)
    
    def _plot_surprise(self, ax):
        """Panel 2: The surprising actual result."""
        ax.text(0.5, 0.7, '😮 THE SURPRISE', 
                ha='center', va='center', fontsize=14, fontweight='bold',
                color=self.colors['without'], transform=ax.transAxes)
        
        # Actual results
        without_avg = np.mean(self.multi['without_persona']['probabilities'])
        with_avg = np.mean(self.multi['with_persona']['probabilities'])
        
        categories = ['Without\nPersona', 'With\nPersona\n(Actual)']
        actual = [without_avg, with_avg]
        bars = ax.bar(categories, actual, 
                      color=[self.colors['without'], self.colors['with']], 
                      alpha=0.7, width=0.6)
        
        # Add arrow showing actual decrease
        ax.annotate('', xy=(1, with_avg - 0.02), xytext=(0, without_avg + 0.02),
                   arrowprops=dict(arrowstyle='->', lw=2, color=self.colors['without']))
        
        decrease_pct = ((with_avg - without_avg) / without_avg) * 100
        ax.text(0.5, (without_avg + with_avg) / 2, f'{decrease_pct:.1f}%\nDecrease!', 
               ha='center', fontsize=9, color=self.colors['without'], 
               fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.set_ylabel('Average Confidence', fontsize=10)
        ax.set_ylim(0, 1.0)
        ax.set_title('Reality: Confidence DECREASED by 21.4%', fontsize=10, pad=10)
        ax.grid(True, alpha=0.3)
    
    def _plot_investigation(self, ax):
        """Panel 3: Looking deeper at token-by-token."""
        ax.text(0.5, 0.9, '🔍 DEEPER INVESTIGATION', 
                ha='center', va='center', fontsize=14, fontweight='bold',
                transform=ax.transAxes)
        
        # Token-by-token confidence
        tokens_without = self.multi['without_persona']['probabilities']
        tokens_with = self.multi['with_persona']['probabilities']
        
        x = np.arange(len(tokens_without))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, tokens_without, width, 
                      label='Without Persona', color=self.colors['without'], alpha=0.7)
        bars2 = ax.bar(x + width/2, tokens_with, width,
                      label='With Persona', color=self.colors['with'], alpha=0.7)
        
        # Highlight first token where persona is MORE confident
        ax.add_patch(plt.Rectangle((-0.4, 0), 0.8, tokens_with[0], 
                                   fill=False, edgecolor=self.colors['highlight'], 
                                   linewidth=3, linestyle='--'))
        ax.text(0, tokens_with[0] + 0.05, 'Higher!', ha='center', 
               fontsize=8, color=self.colors['highlight'], fontweight='bold')
        
        ax.set_xlabel('Token Position', fontsize=10)
        ax.set_ylabel('Confidence', fontsize=10)
        ax.set_title('Token-by-token reveals the pattern', fontsize=10, pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels([f'T{i+1}' for i in x])
        ax.legend(fontsize=8)
        ax.set_ylim(0, 1.1)
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_insight(self, ax):
        """Panel 4: The powerful insight."""
        ax.text(0.5, 0.85, '💡 THE INSIGHT', 
                ha='center', va='center', fontsize=14, fontweight='bold',
                color=self.colors['with'], transform=ax.transAxes)
        
        # Show first token comparison
        first_without = self.multi['without_persona']['probabilities'][0]
        first_with = self.multi['with_persona']['probabilities'][0]
        
        data = [first_without, first_with]
        labels = ['Generic AI\n"Design..."', 'Azure Architect\n"To..."']
        colors_bars = [self.colors['without'], self.colors['with']]
        
        bars = ax.bar(labels, data, color=colors_bars, alpha=0.7, width=0.6)
        
        # Add value labels
        for bar, val in zip(bars, data):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                   f'{val*100:.1f}%', ha='center', va='bottom', 
                   fontweight='bold', fontsize=10)
        
        ax.set_ylabel('First Token Confidence', fontsize=10)
        ax.set_ylim(0, 1.1)
        ax.set_title('Personas RESHAPE probabilities toward\nexpert responses', 
                    fontsize=10, pad=10, fontweight='bold')
        
        # Add insight text
        ax.text(0.5, 0.25, 
               'Lower average confidence =\nMore expert deliberation\nat key decision points',
               ha='center', va='center', fontsize=9, style='italic',
               transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor=self.colors['highlight'], 
                        alpha=0.3, edgecolor=self.colors['with'], linewidth=2))
        
        ax.grid(True, alpha=0.3, axis='y')
    
    def create_probability_redistribution(self):
        """Create detailed probability redistribution visualization."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('How Personas Redistribute Token Probabilities', 
                    fontsize=14, fontweight='bold')
        
        # Left: Top tokens without persona
        without_tokens = self.single['without_persona']['tokens'][:10]
        without_probs = self.single['without_persona']['probabilities'][:10]
        
        ax1.barh(range(len(without_tokens)), without_probs, 
                color=self.colors['without'], alpha=0.7)
        ax1.set_yticks(range(len(without_tokens)))
        ax1.set_yticklabels([f'"{t}"' for t in without_tokens], fontsize=9)
        ax1.set_xlabel('Probability', fontsize=10)
        ax1.set_title('WITHOUT Persona: Top 10 Tokens\n(Generic AI)', 
                     fontsize=11, fontweight='bold')
        ax1.invert_yaxis()
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Highlight selected token
        selected_idx = without_tokens.index(
            self.single['without_persona']['selected_token'])
        ax1.get_children()[selected_idx].set_color(self.colors['highlight'])
        ax1.get_children()[selected_idx].set_alpha(1.0)
        ax1.text(without_probs[selected_idx] + 0.02, selected_idx, 
                '← Selected', fontsize=9, va='center', fontweight='bold')
        
        # Right: Top tokens with persona
        with_tokens = self.single['with_persona']['tokens'][:10]
        with_probs = self.single['with_persona']['probabilities'][:10]
        
        ax2.barh(range(len(with_tokens)), with_probs,
                color=self.colors['with'], alpha=0.7)
        ax2.set_yticks(range(len(with_tokens)))
        ax2.set_yticklabels([f'"{t}"' for t in with_tokens], fontsize=9)
        ax2.set_xlabel('Probability', fontsize=10)
        ax2.set_title('WITH Persona: Top 10 Tokens\n(Azure Architect)', 
                     fontsize=11, fontweight='bold')
        ax2.invert_yaxis()
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Highlight selected token
        selected_idx_with = with_tokens.index(
            self.single['with_persona']['selected_token'])
        ax2.get_children()[selected_idx_with].set_color(self.colors['highlight'])
        ax2.get_children()[selected_idx_with].set_alpha(1.0)
        ax2.text(with_probs[selected_idx_with] + 0.02, selected_idx_with,
                '← Selected', fontsize=9, va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'probability_redistribution.png', 
                   dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {self.output_dir / 'probability_redistribution.png'}")
        plt.close()
    
    def create_response_comparison(self):
        """Create side-by-side response comparison."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Get the actual generated text
        text_without = self.multi['without_persona']['full_text']
        text_with = self.multi['with_persona']['full_text']
        
        ax.text(0.5, 0.95, 'Same Question, Different Responses', 
               ha='center', va='top', fontsize=14, fontweight='bold',
               transform=ax.transAxes)
        
        ax.text(0.5, 0.85, 'Prompt: "How should I design the system?"',
               ha='center', va='top', fontsize=11, style='italic',
               transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
        
        # Without persona response
        ax.text(0.25, 0.65, 'Generic AI Response:',
               ha='center', va='top', fontsize=11, fontweight='bold',
               color=self.colors['without'], transform=ax.transAxes)
        
        ax.text(0.25, 0.55, f'"{text_without}"',
               ha='center', va='top', fontsize=10,
               transform=ax.transAxes, wrap=True,
               bbox=dict(boxstyle='round', facecolor=self.colors['without'], 
                        alpha=0.2, edgecolor=self.colors['without'], linewidth=2))
        
        avg_without = np.mean(self.multi['without_persona']['probabilities'])
        ax.text(0.25, 0.38, f'Avg Confidence: {avg_without*100:.1f}%',
               ha='center', va='top', fontsize=9, style='italic',
               transform=ax.transAxes)
        
        # With persona response  
        ax.text(0.75, 0.65, 'Azure Architect Response:',
               ha='center', va='top', fontsize=11, fontweight='bold',
               color=self.colors['with'], transform=ax.transAxes)
        
        ax.text(0.75, 0.55, f'"{text_with}"',
               ha='center', va='top', fontsize=10,
               transform=ax.transAxes, wrap=True,
               bbox=dict(boxstyle='round', facecolor=self.colors['with'],
                        alpha=0.2, edgecolor=self.colors['with'], linewidth=2))
        
        avg_with = np.mean(self.multi['with_persona']['probabilities'])
        ax.text(0.75, 0.38, f'Avg Confidence: {avg_with*100:.1f}%',
               ha='center', va='top', fontsize=9, style='italic',
               transform=ax.transAxes)
        
        # Add conclusion
        ax.text(0.5, 0.15, 
               'Same input → Different probability distributions → Different expert-level responses',
               ha='center', va='top', fontsize=10, fontweight='bold',
               transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor=self.colors['highlight'],
                        alpha=0.3, edgecolor=self.colors['text'], linewidth=2))
        
        ax.axis('off')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'response_comparison.png',
                   dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {self.output_dir / 'response_comparison.png'}")
        plt.close()
    
    def create_all_visualizations(self):
        """Create all visualization types."""
        print("\n" + "="*60)
        print("Creating Discovery Journey Visualizations")
        print("="*60)
        
        self.load_results()
        
        print("\n1. Creating 4-panel discovery narrative...")
        self.create_story_narrative()
        
        print("\n2. Creating probability redistribution comparison...")
        self.create_probability_redistribution()
        
        print("\n3. Creating response comparison...")
        self.create_response_comparison()
        
        print("\n" + "="*60)
        print("✓ All visualizations complete!")
        print("="*60)
        print(f"\nCheck the '{self.output_dir}' directory for:")
        print("  - discovery_journey.png (The main story)")
        print("  - probability_redistribution.png (Detailed token analysis)")
        print("  - response_comparison.png (Side-by-side responses)")

def main():
    visualizer = PersonaStoryVisualizer()
    visualizer.create_all_visualizations()

if __name__ == "__main__":
    main()
