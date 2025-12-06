"""
Analyze Entropy Volatility Patterns

Tests the hypothesis that:
- Generic AI: High entropy spikes next to high confidence (volatile, "riding the wave")
- Persona AI: Stable, consistent entropy (thoughtful, deliberate evaluation)
"""

import json
import matplotlib.pyplot as plt
import numpy as np

def load_data():
    """Load the 50-token distribution results."""
    with open('results/results_full_distributions.json', 'r') as f:
        return json.load(f)

def calculate_volatility_metrics(entropy_sequence):
    """Calculate various volatility metrics."""
    entropy_array = np.array(entropy_sequence)
    
    # Standard deviation (overall volatility)
    volatility = np.std(entropy_array)
    
    # Consecutive differences (how much it jumps around)
    diffs = np.abs(np.diff(entropy_array))
    avg_jump = np.mean(diffs)
    max_jump = np.max(diffs)
    
    # Count sharp transitions (changes > 0.5 bits)
    sharp_transitions = np.sum(diffs > 0.5)
    
    # Coefficient of variation (volatility relative to mean)
    cv = volatility / np.mean(entropy_array) if np.mean(entropy_array) > 0 else 0
    
    return {
        'std_dev': volatility,
        'avg_jump': avg_jump,
        'max_jump': max_jump,
        'sharp_transitions': sharp_transitions,
        'coefficient_of_variation': cv
    }

def create_volatility_comparison():
    """Create comprehensive volatility comparison visualization."""
    data = load_data()
    
    entropy_without = data['statistics']['entropy_per_token_without']
    entropy_with = data['statistics']['entropy_per_token_with']
    positions = np.arange(1, len(entropy_without) + 1)
    
    # Calculate volatility metrics
    metrics_without = calculate_volatility_metrics(entropy_without)
    metrics_with = calculate_volatility_metrics(entropy_with)
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3,
                          left=0.08, right=0.95, top=0.93, bottom=0.06)
    
    colors = {'generic': '#FF6B6B', 'persona': '#4ECDC4'}
    
    fig.suptitle('Entropy Volatility Analysis: "Confidence Riding" vs "Consistent Evaluation"', 
                 fontsize=18, fontweight='bold')
    
    # 1. Main entropy plot with annotations
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(positions, entropy_without, 'o-', color=colors['generic'], 
            linewidth=2.5, markersize=6, label='Generic AI', alpha=0.8)
    ax1.plot(positions, entropy_with, 's-', color=colors['persona'],
            linewidth=2.5, markersize=6, label='Persona AI', alpha=0.8)
    
    # Highlight volatile regions
    diffs_without = np.abs(np.diff(entropy_without))
    volatile_indices = np.where(diffs_without > 0.5)[0]
    for idx in volatile_indices:
        ax1.axvspan(positions[idx], positions[idx+1], alpha=0.2, color='red')
    
    ax1.set_xlabel('Token Position', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Entropy (bits)', fontsize=13, fontweight='bold')
    ax1.set_title('Entropy Across 50-Token Sequence (Red shading = sharp transitions)', 
                 fontsize=14, fontweight='bold', pad=15)
    ax1.legend(fontsize=12, loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Add volatility annotations
    ax1.text(0.02, 0.98, f"Generic AI Volatility: σ={metrics_without['std_dev']:.3f}", 
            transform=ax1.transAxes, fontsize=11, va='top',
            bbox=dict(boxstyle='round', facecolor=colors['generic'], alpha=0.3))
    ax1.text(0.02, 0.90, f"Persona AI Volatility: σ={metrics_with['std_dev']:.3f}", 
            transform=ax1.transAxes, fontsize=11, va='top',
            bbox=dict(boxstyle='round', facecolor=colors['persona'], alpha=0.3))
    
    # 2. Entropy differences (jumps between consecutive tokens)
    ax2 = fig.add_subplot(gs[1, 0])
    diffs_without = np.abs(np.diff(entropy_without))
    diffs_with = np.abs(np.diff(entropy_with))
    diff_positions = positions[:-1]
    
    ax2.bar(diff_positions - 0.2, diffs_without, width=0.4, 
           color=colors['generic'], alpha=0.7, label='Generic AI')
    ax2.bar(diff_positions + 0.2, diffs_with, width=0.4,
           color=colors['persona'], alpha=0.7, label='Persona AI')
    
    ax2.axhline(y=0.5, color='red', linestyle='--', linewidth=2, alpha=0.5, 
               label='Sharp transition threshold')
    
    ax2.set_xlabel('Token Position', fontsize=11, fontweight='bold')
    ax2.set_ylabel('|Entropy Change|', fontsize=11, fontweight='bold')
    ax2.set_title('Entropy Jumps Between Consecutive Tokens', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add metrics
    text = (f"Generic: {metrics_without['sharp_transitions']} sharp transitions\n"
            f"Persona: {metrics_with['sharp_transitions']} sharp transitions")
    ax2.text(0.98, 0.98, text, transform=ax2.transAxes, fontsize=10,
            va='top', ha='right', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # 3. Rolling window standard deviation (local volatility)
    ax3 = fig.add_subplot(gs[1, 1])
    window = 5
    rolling_std_without = [np.std(entropy_without[max(0, i-window):i+1]) 
                          for i in range(len(entropy_without))]
    rolling_std_with = [np.std(entropy_with[max(0, i-window):i+1]) 
                       for i in range(len(entropy_with))]
    
    ax3.plot(positions, rolling_std_without, 'o-', color=colors['generic'],
            linewidth=2, markersize=4, label='Generic AI', alpha=0.8)
    ax3.plot(positions, rolling_std_with, 's-', color=colors['persona'],
            linewidth=2, markersize=4, label='Persona AI', alpha=0.8)
    
    ax3.set_xlabel('Token Position', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Rolling Std Dev (5-token window)', fontsize=11, fontweight='bold')
    ax3.set_title('Local Volatility Over Time', fontsize=13, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # 4. Distribution of entropy values
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.hist(entropy_without, bins=20, color=colors['generic'], alpha=0.6, 
            label='Generic AI', edgecolor='black')
    ax4.hist(entropy_with, bins=20, color=colors['persona'], alpha=0.6,
            label='Persona AI', edgecolor='black')
    ax4.axvline(np.mean(entropy_without), color=colors['generic'], 
               linestyle='--', linewidth=2, label=f"Generic mean: {np.mean(entropy_without):.2f}")
    ax4.axvline(np.mean(entropy_with), color=colors['persona'],
               linestyle='--', linewidth=2, label=f"Persona mean: {np.mean(entropy_with):.2f}")
    
    ax4.set_xlabel('Entropy (bits)', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax4.set_title('Distribution of Entropy Values', fontsize=13, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 5. Volatility metrics comparison table
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.axis('off')
    
    metrics_data = [
        ['Metric', 'Generic AI', 'Persona AI', 'Interpretation'],
        ['─'*20, '─'*12, '─'*12, '─'*30],
        ['Std Deviation', f"{metrics_without['std_dev']:.3f}", 
         f"{metrics_with['std_dev']:.3f}",
         'Lower = more stable'],
        ['Avg Jump Size', f"{metrics_without['avg_jump']:.3f}",
         f"{metrics_with['avg_jump']:.3f}",
         'Avg change between tokens'],
        ['Max Jump', f"{metrics_without['max_jump']:.3f}",
         f"{metrics_with['max_jump']:.3f}",
         'Largest single transition'],
        ['Sharp Transitions', f"{metrics_without['sharp_transitions']}",
         f"{metrics_with['sharp_transitions']}",
         'Count of jumps > 0.5 bits'],
        ['Coeff. of Variation', f"{metrics_without['coefficient_of_variation']:.3f}",
         f"{metrics_with['coefficient_of_variation']:.3f}",
         'Volatility relative to mean'],
    ]
    
    table = ax5.table(cellText=metrics_data, cellLoc='left', loc='center',
                     colWidths=[0.35, 0.2, 0.2, 0.45])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Style header row
    for i in range(4):
        table[(0, i)].set_facecolor('#E8E8E8')
        table[(0, i)].set_text_props(weight='bold')
    
    # Color code the comparison columns
    for i in range(2, len(metrics_data)):
        table[(i, 1)].set_facecolor(colors['generic'] + '40')
        table[(i, 2)].set_facecolor(colors['persona'] + '40')
    
    ax5.set_title('Volatility Metrics Comparison', fontsize=13, fontweight='bold', pad=20)
    
    plt.savefig('visualizations/entropy_volatility_analysis.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/entropy_volatility_analysis.png")
    plt.close()

def create_hypothesis_verdict():
    """Create a clear verdict visualization on the hypothesis."""
    data = load_data()
    
    entropy_without = data['statistics']['entropy_per_token_without']
    entropy_with = data['statistics']['entropy_per_token_with']
    
    metrics_without = calculate_volatility_metrics(entropy_without)
    metrics_with = calculate_volatility_metrics(entropy_with)
    
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.axis('off')
    
    # Title
    title_text = "HYPOTHESIS TEST: 'Confidence Riding' vs 'Consistent Evaluation'"
    ax.text(0.5, 0.95, title_text, ha='center', fontsize=22, fontweight='bold',
           transform=ax.transAxes)
    
    # Hypothesis
    hypothesis = """HYPOTHESIS:
• Generic AI: Volatile entropy with sharp spikes (riding waves of confidence)
• Persona AI: Stable, consistent entropy (thoughtful, deliberate evaluation)"""
    
    ax.text(0.5, 0.88, hypothesis, ha='center', fontsize=14, style='italic',
           transform=ax.transAxes, family='monospace',
           bbox=dict(boxstyle='round,pad=1', facecolor='#FFE66D', alpha=0.3))
    
    # Results
    is_generic_more_volatile = metrics_without['std_dev'] > metrics_with['std_dev']
    is_generic_more_jumpy = metrics_without['avg_jump'] > metrics_with['avg_jump']
    has_more_sharp_transitions = metrics_without['sharp_transitions'] > metrics_with['sharp_transitions']
    
    results_text = f"""RESULTS (50 tokens analyzed):

VOLATILITY COMPARISON:
  Generic AI:  σ = {metrics_without['std_dev']:.3f}  |  Avg Jump = {metrics_without['avg_jump']:.3f}  |  Sharp Transitions = {metrics_without['sharp_transitions']}
  Persona AI:  σ = {metrics_with['std_dev']:.3f}  |  Avg Jump = {metrics_with['avg_jump']:.3f}  |  Sharp Transitions = {metrics_with['sharp_transitions']}
  
  Difference:  Δσ = {abs(metrics_without['std_dev'] - metrics_with['std_dev']):.3f} ({((metrics_without['std_dev'] - metrics_with['std_dev'])/metrics_with['std_dev']*100):+.1f}%)"""
    
    ax.text(0.5, 0.68, results_text, ha='center', fontsize=12, family='monospace',
           transform=ax.transAxes,
           bbox=dict(boxstyle='round,pad=1', facecolor='white', edgecolor='black', linewidth=2))
    
    # Verdict
    if is_generic_more_volatile and has_more_sharp_transitions:
        verdict = "✓ HYPOTHESIS CONFIRMED"
        verdict_color = '#4CAF50'
        explanation = """The data CONFIRMS the hypothesis:

• Generic AI shows HIGHER volatility (σ = {:.3f} vs {:.3f})
• Generic AI has MORE sharp transitions ({} vs {})
• Generic AI exhibits the "confidence riding" pattern with volatile entropy spikes
• Persona AI maintains more CONSISTENT entropy, indicating deliberate evaluation

INTERPRETATION: Personas create a more stable decision-making process, avoiding
the "ride the confidence wave" pattern seen in generic AI responses.""".format(
            metrics_without['std_dev'], metrics_with['std_dev'],
            metrics_without['sharp_transitions'], metrics_with['sharp_transitions']
        )
    elif not is_generic_more_volatile and not has_more_sharp_transitions:
        verdict = "✗ HYPOTHESIS REJECTED"
        verdict_color = '#F44336'
        explanation = """The data REJECTS the hypothesis:

• Persona AI actually shows HIGHER or similar volatility
• The "confidence riding" pattern is not more pronounced in generic AI
• Both approaches show comparable entropy stability

INTERPRETATION: The hypothesis about generic AI "riding confidence waves" while
personas maintain stability is not supported by this 50-token sample.""".format(
            metrics_without['std_dev'], metrics_with['std_dev'],
            metrics_without['sharp_transitions'], metrics_with['sharp_transitions']
        )
    else:
        verdict = "⚠ MIXED RESULTS"
        verdict_color = '#FF9800'
        explanation = """The data shows MIXED results:

• Some metrics support the hypothesis, others don't
• The pattern is more nuanced than the simple "riding vs stable" dichotomy
• Additional analysis with more samples needed for definitive conclusion

INTERPRETATION: Reality is more complex than the binary hypothesis suggests."""
    
    ax.text(0.5, 0.45, verdict, ha='center', fontsize=26, fontweight='bold',
           transform=ax.transAxes, color=verdict_color,
           bbox=dict(boxstyle='round,pad=0.8', facecolor=verdict_color, alpha=0.2, 
                    edgecolor=verdict_color, linewidth=4))
    
    ax.text(0.5, 0.25, explanation, ha='center', fontsize=11,
           transform=ax.transAxes, family='monospace',
           bbox=dict(boxstyle='round,pad=1', facecolor='#F0F0F0', edgecolor='black', linewidth=1.5))
    
    # Footer note
    note = "Note: This analysis is based on a single 50-token sequence. Multiple runs would provide more robust conclusions."
    ax.text(0.5, 0.02, note, ha='center', fontsize=9, style='italic', color='gray',
           transform=ax.transAxes)
    
    plt.savefig('visualizations/hypothesis_verdict.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/hypothesis_verdict.png")
    plt.close()
    
    return verdict, metrics_without, metrics_with

def main():
    print("\n" + "="*70)
    print("Entropy Volatility Analysis")
    print("="*70)
    print("\nTesting hypothesis: Generic AI shows volatile 'confidence riding'")
    print("vs Persona AI showing consistent evaluation patterns.\n")
    
    print("1. Creating comprehensive volatility comparison...")
    create_volatility_comparison()
    
    print("\n2. Generating hypothesis verdict...")
    verdict, metrics_without, metrics_with = create_hypothesis_verdict()
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nVerdict: {verdict}")
    print(f"\nKey Findings:")
    print(f"  Generic AI Volatility (σ): {metrics_without['std_dev']:.3f}")
    print(f"  Persona AI Volatility (σ): {metrics_with['std_dev']:.3f}")
    print(f"  Generic Sharp Transitions: {metrics_without['sharp_transitions']}")
    print(f"  Persona Sharp Transitions: {metrics_with['sharp_transitions']}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
