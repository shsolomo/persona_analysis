"""
Multi-Scenario Visualization Script

Creates compelling visualizations showing patterns across multiple test scenarios.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

class MultiScenarioVisualizer:
    """Creates visualizations for multi-scenario experiment results."""
    
    def __init__(self, results_file: str = 'results_multi_scenario.json',
                 output_dir: str = 'visualizations'):
        """Initialize visualizer."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        with open(results_file, 'r') as f:
            self.results = json.load(f)
        
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = {
            'without': '#FF6B6B',
            'with': '#4ECDC4',
            'highlight': '#FFE66D',
            'text': '#2C3E50',
            'increase': '#51CF66',
            'decrease': '#FF6B6B'
        }
    
    def create_first_token_comparison(self):
        """Create comprehensive first token comparison chart."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('First Token Analysis Across Scenarios', 
                    fontsize=16, fontweight='bold')
        
        scenarios = [r['scenario']['name'] for r in self.results]
        
        # Panel 1: First token confidence comparison
        without_first = [r['first_token']['without']['probability'] * 100 
                        for r in self.results]
        with_first = [r['first_token']['with']['probability'] * 100 
                     for r in self.results]
        
        x = np.arange(len(scenarios))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, without_first, width, 
                       label='Without Persona', color=self.colors['without'], alpha=0.7)
        bars2 = ax1.bar(x + width/2, with_first, width,
                       label='With Persona', color=self.colors['with'], alpha=0.7)
        
        ax1.set_ylabel('First Token Confidence (%)', fontsize=10)
        ax1.set_title('First Token Confidence by Scenario', fontsize=11, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels([s.replace(' ', '\n') for s in scenarios], 
                           fontsize=8, rotation=0)
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.set_ylim(0, 110)
        
        # Panel 2: Confidence change
        changes = [r['first_token']['first_token_confidence_change'] 
                  for r in self.results]
        colors_change = [self.colors['increase'] if c > 0 else self.colors['decrease'] 
                        for c in changes]
        
        bars = ax2.barh(range(len(scenarios)), changes, color=colors_change, alpha=0.7)
        ax2.set_yticks(range(len(scenarios)))
        ax2.set_yticklabels(scenarios, fontsize=9)
        ax2.set_xlabel('Confidence Change (%)', fontsize=10)
        ax2.set_title('First Token Confidence Change', fontsize=11, fontweight='bold')
        ax2.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, changes)):
            x_pos = val + (5 if val > 0 else -5)
            ax2.text(x_pos, i, f'{val:+.1f}%', 
                    va='center', ha='left' if val > 0 else 'right',
                    fontsize=8, fontweight='bold')
        
        # Panel 3: Token distribution (best case)
        best_idx = changes.index(max(changes))
        best_result = self.results[best_idx]
        
        without_tokens = best_result['first_token']['without']['top_5_tokens']
        without_probs = [p * 100 for p in best_result['first_token']['without']['top_5_probs']]
        
        ax3.barh(range(len(without_tokens)), without_probs, 
                color=self.colors['without'], alpha=0.7)
        ax3.set_yticks(range(len(without_tokens)))
        ax3.set_yticklabels([f'"{t}"' for t in without_tokens], fontsize=9)
        ax3.set_xlabel('Probability (%)', fontsize=10)
        ax3.set_title(f'WITHOUT Persona: "{best_result["scenario"]["name"]}"\n' +
                     f'Selected: "{without_tokens[0]}" ({without_probs[0]:.1f}%)',
                     fontsize=10, fontweight='bold')
        ax3.invert_yaxis()
        ax3.grid(True, alpha=0.3, axis='x')
        
        # Panel 4: Token distribution (with persona)
        with_tokens = best_result['first_token']['with']['top_5_tokens']
        with_probs = [p * 100 for p in best_result['first_token']['with']['top_5_probs']]
        
        ax4.barh(range(len(with_tokens)), with_probs,
                color=self.colors['with'], alpha=0.7)
        ax4.set_yticks(range(len(with_tokens)))
        ax4.set_yticklabels([f'"{t}"' for t in with_tokens], fontsize=9)
        ax4.set_xlabel('Probability (%)', fontsize=10)
        ax4.set_title(f'WITH Persona: "{best_result["scenario"]["name"]}"\n' +
                     f'Selected: "{with_tokens[0]}" ({with_probs[0]:.1f}%)',
                     fontsize=10, fontweight='bold')
        ax4.invert_yaxis()
        ax4.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'multi_first_token_analysis.png', 
                   dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {self.output_dir / 'multi_first_token_analysis.png'}")
        plt.close()
    
    def create_sequence_confidence_comparison(self):
        """Create sequence confidence comparison."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('Sequence Confidence Analysis Across Scenarios',
                    fontsize=14, fontweight='bold')
        
        scenarios = [r['scenario']['name'] for r in self.results]
        
        # Panel 1: Average confidence comparison
        without_avg = [r['sequence']['without']['avg_confidence'] * 100 
                      for r in self.results]
        with_avg = [r['sequence']['with']['avg_confidence'] * 100 
                   for r in self.results]
        
        x = np.arange(len(scenarios))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, without_avg, width,
                       label='Without Persona', color=self.colors['without'], alpha=0.7)
        bars2 = ax1.bar(x + width/2, with_avg, width,
                       label='With Persona', color=self.colors['with'], alpha=0.7)
        
        ax1.set_ylabel('Average Confidence (%)', fontsize=10)
        ax1.set_title('Average Sequence Confidence', fontsize=11, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels([s.replace(' ', '\n') for s in scenarios],
                           fontsize=8, rotation=0)
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.set_ylim(0, 110)
        
        # Panel 2: Confidence change
        changes = [r['sequence']['avg_confidence_change'] for r in self.results]
        colors_change = [self.colors['increase'] if c > 0 else self.colors['decrease']
                        for c in changes]
        
        bars = ax2.barh(range(len(scenarios)), changes, color=colors_change, alpha=0.7)
        ax2.set_yticks(range(len(scenarios)))
        ax2.set_yticklabels(scenarios, fontsize=9)
        ax2.set_xlabel('Confidence Change (%)', fontsize=10)
        ax2.set_title('Average Sequence Confidence Change', fontsize=11, fontweight='bold')
        ax2.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, changes)):
            x_pos = val + (5 if val > 0 else -5)
            ax2.text(x_pos, i, f'{val:+.1f}%',
                    va='center', ha='left' if val > 0 else 'right',
                    fontsize=8, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'multi_sequence_confidence.png',
                   dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {self.output_dir / 'multi_sequence_confidence.png'}")
        plt.close()
    
    def create_response_showcase(self):
        """Create a showcase of different responses."""
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle('Response Comparison Across Scenarios',
                    fontsize=14, fontweight='bold')
        
        n_scenarios = len(self.results)
        
        for idx, result in enumerate(self.results):
            ax = plt.subplot(3, 2, idx + 1)
            
            scenario_name = result['scenario']['name']
            prompt = result['scenario']['prompt']
            text_without = result['sequence']['without']['text']
            text_with = result['sequence']['with']['text']
            
            # Title
            ax.text(0.5, 0.95, scenario_name,
                   ha='center', va='top', fontsize=10, fontweight='bold',
                   transform=ax.transAxes)
            
            ax.text(0.5, 0.85, f'Q: "{prompt}"',
                   ha='center', va='top', fontsize=8, style='italic',
                   transform=ax.transAxes, wrap=True)
            
            # Responses
            ax.text(0.05, 0.65, 'Generic:',
                   ha='left', va='top', fontsize=8, fontweight='bold',
                   color=self.colors['without'], transform=ax.transAxes)
            
            ax.text(0.05, 0.55, f'"{text_without}"',
                   ha='left', va='top', fontsize=7,
                   transform=ax.transAxes, wrap=True,
                   bbox=dict(boxstyle='round', facecolor=self.colors['without'],
                            alpha=0.1, edgecolor=self.colors['without'], linewidth=1))
            
            ax.text(0.05, 0.35, 'Architect:',
                   ha='left', va='top', fontsize=8, fontweight='bold',
                   color=self.colors['with'], transform=ax.transAxes)
            
            ax.text(0.05, 0.25, f'"{text_with}"',
                   ha='left', va='top', fontsize=7,
                   transform=ax.transAxes, wrap=True,
                   bbox=dict(boxstyle='round', facecolor=self.colors['with'],
                            alpha=0.1, edgecolor=self.colors['with'], linewidth=1))
            
            ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'multi_response_showcase.png',
                   dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {self.output_dir / 'multi_response_showcase.png'}")
        plt.close()
    
    def create_pattern_summary(self):
        """Create overall pattern summary visualization."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Multi-Scenario Pattern Analysis',
                    fontsize=16, fontweight='bold')
        
        # Extract all data
        first_changes = [r['first_token']['first_token_confidence_change'] 
                        for r in self.results]
        seq_changes = [r['sequence']['avg_confidence_change'] 
                      for r in self.results]
        scenarios = [r['scenario']['name'] for r in self.results]
        
        # Panel 1: Scatter plot
        colors_scatter = [self.colors['highlight'] if fc > 0 and sc < 0 
                         else self.colors['increase'] if fc > 0 and sc > 0
                         else self.colors['decrease']
                         for fc, sc in zip(first_changes, seq_changes)]
        
        ax1.scatter(first_changes, seq_changes, s=200, c=colors_scatter, alpha=0.6)
        for i, name in enumerate(scenarios):
            ax1.annotate(name, (first_changes[i], seq_changes[i]),
                        fontsize=7, ha='center')
        
        ax1.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax1.axvline(x=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax1.set_xlabel('First Token Confidence Change (%)', fontsize=10)
        ax1.set_ylabel('Avg Sequence Confidence Change (%)', fontsize=10)
        ax1.set_title('Pattern Distribution', fontsize=11, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Add quadrant labels
        ax1.text(0.95, 0.95, 'Both ↑', transform=ax1.transAxes, 
                ha='right', va='top', fontsize=8, style='italic',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        ax1.text(0.05, 0.05, 'Both ↓', transform=ax1.transAxes,
                ha='left', va='bottom', fontsize=8, style='italic',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        ax1.text(0.95, 0.05, 'First ↑, Avg ↓\n(Expert Pattern)', 
                transform=ax1.transAxes,
                ha='right', va='bottom', fontsize=8, style='italic',
                bbox=dict(boxstyle='round', facecolor=self.colors['highlight'], alpha=0.5))
        
        # Panel 2: Statistics summary
        ax2.axis('off')
        stats_text = f"""
OVERALL STATISTICS

First Token Confidence:
  • Average Change: {np.mean(first_changes):+.1f}%
  • Median Change: {np.median(first_changes):+.1f}%
  • Range: {np.min(first_changes):+.1f}% to {np.max(first_changes):+.1f}%

Sequence Average:
  • Average Change: {np.mean(seq_changes):+.1f}%
  • Median Change: {np.median(seq_changes):+.1f}%
  • Range: {np.min(seq_changes):+.1f}% to {np.max(seq_changes):+.1f}%

Pattern Counts:
  • First token increased: {sum(1 for x in first_changes if x > 0)}/{len(first_changes)}
  • Sequence avg decreased: {sum(1 for x in seq_changes if x < 0)}/{len(seq_changes)}
  • "Expert pattern" (↑/↓): {sum(1 for fc, sc in zip(first_changes, seq_changes) if fc > 0 and sc < 0)}/{len(first_changes)}
        """
        
        ax2.text(0.1, 0.9, stats_text, transform=ax2.transAxes,
                fontsize=9, family='monospace', va='top')
        
        # Panel 3: Histogram of first token changes
        ax3.hist(first_changes, bins=10, color=self.colors['with'], alpha=0.7, edgecolor='black')
        ax3.axvline(x=0, color='black', linestyle='--', linewidth=1)
        ax3.axvline(x=np.mean(first_changes), color='red', linestyle='-', linewidth=2,
                   label=f'Mean: {np.mean(first_changes):+.1f}%')
        ax3.set_xlabel('First Token Confidence Change (%)', fontsize=10)
        ax3.set_ylabel('Count', fontsize=10)
        ax3.set_title('Distribution: First Token Changes', fontsize=11, fontweight='bold')
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Panel 4: Histogram of sequence changes
        ax4.hist(seq_changes, bins=10, color=self.colors['with'], alpha=0.7, edgecolor='black')
        ax4.axvline(x=0, color='black', linestyle='--', linewidth=1)
        ax4.axvline(x=np.mean(seq_changes), color='red', linestyle='-', linewidth=2,
                   label=f'Mean: {np.mean(seq_changes):+.1f}%')
        ax4.set_xlabel('Sequence Confidence Change (%)', fontsize=10)
        ax4.set_ylabel('Count', fontsize=10)
        ax4.set_title('Distribution: Sequence Changes', fontsize=11, fontweight='bold')
        ax4.legend(fontsize=8)
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'multi_pattern_summary.png',
                   dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {self.output_dir / 'multi_pattern_summary.png'}")
        plt.close()
    
    def create_all_visualizations(self):
        """Create all visualization types."""
        print("\n" + "="*60)
        print("Creating Multi-Scenario Visualizations")
        print("="*60)
        
        print("\n1. Creating first token analysis...")
        self.create_first_token_comparison()
        
        print("\n2. Creating sequence confidence comparison...")
        self.create_sequence_confidence_comparison()
        
        print("\n3. Creating response showcase...")
        self.create_response_showcase()
        
        print("\n4. Creating pattern summary...")
        self.create_pattern_summary()
        
        print("\n" + "="*60)
        print("✓ All multi-scenario visualizations complete!")
        print("="*60)
        print(f"\nCheck the '{self.output_dir}' directory for:")
        print("  - multi_first_token_analysis.png")
        print("  - multi_sequence_confidence.png")
        print("  - multi_response_showcase.png")
        print("  - multi_pattern_summary.png")

def main():
    visualizer = MultiScenarioVisualizer()
    visualizer.create_all_visualizations()

if __name__ == "__main__":
    main()
