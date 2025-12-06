"""
Creates a visualization showing probability redistribution across token sequences.
Demonstrates how personas focus confidence on first token, then deliberate on subsequent tokens.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

def load_data():
    """Load the multi-scenario results."""
    with open('results/results_multi_scenario.json', 'r') as f:
        return json.load(f)

def create_probability_redistribution_viz():
    """
    Create a visualization showing how probability is distributed across tokens.
    Shows focused vs distributed confidence patterns.
    """
    data = load_data()
    
    # Find the most dramatic example (Problem Solving scenario)
    problem_solving = [s for s in data if s['scenario']['name'] == 'Problem Solving'][0]
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.25,
                          left=0.08, right=0.95, top=0.94, bottom=0.06)
    
    colors = {
        'generic': '#FF6B6B',
        'persona': '#4ECDC4',
        'low': '#FFE5E5',
        'high': '#E5F9F7'
    }
    
    fig.suptitle('Probability Redistribution: Generic AI vs Persona AI', 
                 fontsize=20, fontweight='bold')
    
    # ==================================================================================
    # Top Section: First Token Probability Distribution
    # ==================================================================================
    
    ax_generic_first = fig.add_subplot(gs[0, 0])
    ax_persona_first = fig.add_subplot(gs[0, 1])
    
    # Generic AI first token
    generic_first = problem_solving['first_token']['without']
    ax_generic_first.set_title('Generic AI - First Token\n(Uncertainty: Spread Probabilities)', 
                              fontsize=14, fontweight='bold', color=colors['generic'], pad=15)
    
    tokens_gen = generic_first['top_5_tokens']
    probs_gen = [p * 100 for p in generic_first['top_5_probs']]
    
    bars_gen = ax_generic_first.barh(range(len(tokens_gen)), probs_gen, 
                                     color=colors['generic'], alpha=0.7, edgecolor='black', linewidth=1.5)
    bars_gen[0].set_alpha(1.0)  # Highlight selected
    bars_gen[0].set_linewidth(2.5)
    
    ax_generic_first.set_yticks(range(len(tokens_gen)))
    ax_generic_first.set_yticklabels([f'"{t}"' for t in tokens_gen], fontsize=11)
    ax_generic_first.set_xlabel('Probability (%)', fontsize=11, fontweight='bold')
    ax_generic_first.set_xlim(0, 105)
    ax_generic_first.invert_yaxis()
    ax_generic_first.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (bar, prob) in enumerate(zip(bars_gen, probs_gen)):
        ax_generic_first.text(prob + 2, i, f'{prob:.1f}%', 
                             va='center', fontsize=10, fontweight='bold')
    
    # Highlight the spread
    ax_generic_first.axvspan(0, 50, alpha=0.1, color='yellow')
    ax_generic_first.text(25, -0.7, 'Probabilities SPREAD across options\n(No clear winner)', 
                         ha='center', fontsize=10, style='italic',
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.2))
    
    # Persona AI first token
    persona_first = problem_solving['first_token']['with']
    ax_persona_first.set_title('Persona AI - First Token\n(Confidence: Focused Probability)', 
                              fontsize=14, fontweight='bold', color=colors['persona'], pad=15)
    
    tokens_per = persona_first['top_5_tokens']
    probs_per = [p * 100 for p in persona_first['top_5_probs']]
    
    bars_per = ax_persona_first.barh(range(len(tokens_per)), probs_per,
                                     color=colors['persona'], alpha=0.7, edgecolor='black', linewidth=1.5)
    bars_per[0].set_alpha(1.0)  # Highlight selected
    bars_per[0].set_linewidth(2.5)
    
    ax_persona_first.set_yticks(range(len(tokens_per)))
    ax_persona_first.set_yticklabels([f'"{t}"' for t in tokens_per], fontsize=11)
    ax_persona_first.set_xlabel('Probability (%)', fontsize=11, fontweight='bold')
    ax_persona_first.set_xlim(0, 105)
    ax_persona_first.invert_yaxis()
    ax_persona_first.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (bar, prob) in enumerate(zip(bars_per, probs_per)):
        ax_persona_first.text(prob + 2, i, f'{prob:.1f}%', 
                             va='center', fontsize=10, fontweight='bold')
    
    # Highlight the focus
    ax_persona_first.axvspan(90, 100, alpha=0.1, color='lightblue')
    ax_persona_first.text(95, -0.7, 'Probability CONCENTRATED\n(Clear direction)', 
                         ha='center', fontsize=10, style='italic',
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.2))
    
    # ==================================================================================
    # Middle Section: Token-by-Token Confidence Pattern
    # ==================================================================================
    
    ax_generic_seq = fig.add_subplot(gs[1, 0])
    ax_persona_seq = fig.add_subplot(gs[1, 1])
    
    # Generic AI sequence
    generic_seq = problem_solving['sequence']['without']
    ax_generic_seq.set_title('Generic AI - Next 9 Tokens\n(Following Template)', 
                            fontsize=14, fontweight='bold', color=colors['generic'], pad=15)
    
    token_positions = range(1, len(generic_seq['tokens']) + 1)
    generic_probs = [p * 100 for p in generic_seq['probabilities']]
    
    ax_generic_seq.plot(token_positions, generic_probs, 'o-', 
                       color=colors['generic'], linewidth=2.5, markersize=8, alpha=0.8)
    ax_generic_seq.fill_between(token_positions, generic_probs, alpha=0.2, color=colors['generic'])
    
    ax_generic_seq.set_xlabel('Token Position', fontsize=11, fontweight='bold')
    ax_generic_seq.set_ylabel('Confidence (%)', fontsize=11, fontweight='bold')
    ax_generic_seq.set_ylim(0, 105)
    ax_generic_seq.grid(True, alpha=0.3)
    ax_generic_seq.set_xticks(token_positions)
    
    # Add token labels
    for i, (pos, token, prob) in enumerate(zip(token_positions, generic_seq['tokens'], generic_probs)):
        if i % 2 == 0:  # Label every other token to avoid crowding
            ax_generic_seq.text(pos, prob + 5, f'"{token}"', 
                              ha='center', fontsize=8, rotation=45)
    
    # Add average line
    avg_gen = np.mean(generic_probs)
    ax_generic_seq.axhline(y=avg_gen, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
    ax_generic_seq.text(len(token_positions) * 0.98, avg_gen + 3, 
                       f'Avg: {avg_gen:.1f}%', ha='right', fontsize=10,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    ax_generic_seq.text(0.5, -0.15, 'High confidence throughout\n(Predictable, template-driven)', 
                       ha='center', va='top', transform=ax_generic_seq.transAxes,
                       fontsize=10, style='italic',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.2))
    
    # Persona AI sequence
    persona_seq = problem_solving['sequence']['with']
    ax_persona_seq.set_title('Persona AI - Next 9 Tokens\n(Deliberate Choice)', 
                            fontsize=14, fontweight='bold', color=colors['persona'], pad=15)
    
    persona_probs = [p * 100 for p in persona_seq['probabilities']]
    
    ax_persona_seq.plot(token_positions, persona_probs, 'o-',
                       color=colors['persona'], linewidth=2.5, markersize=8, alpha=0.8)
    ax_persona_seq.fill_between(token_positions, persona_probs, alpha=0.2, color=colors['persona'])
    
    ax_persona_seq.set_xlabel('Token Position', fontsize=11, fontweight='bold')
    ax_persona_seq.set_ylabel('Confidence (%)', fontsize=11, fontweight='bold')
    ax_persona_seq.set_ylim(0, 105)
    ax_persona_seq.grid(True, alpha=0.3)
    ax_persona_seq.set_xticks(token_positions)
    
    # Add token labels
    for i, (pos, token, prob) in enumerate(zip(token_positions, persona_seq['tokens'], persona_probs)):
        if i % 2 == 0:  # Label every other token to avoid crowding
            ax_persona_seq.text(pos, prob + 5, f'"{token}"', 
                              ha='center', fontsize=8, rotation=45)
    
    # Add average line
    avg_per = np.mean(persona_probs)
    ax_persona_seq.axhline(y=avg_per, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
    ax_persona_seq.text(len(token_positions) * 0.98, avg_per + 3, 
                       f'Avg: {avg_per:.1f}%', ha='right', fontsize=10,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    ax_persona_seq.text(0.5, -0.15, 'Variable confidence\n(Thoughtful, deliberate word choice)', 
                       ha='center', va='top', transform=ax_persona_seq.transAxes,
                       fontsize=10, style='italic',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.2))
    
    # ==================================================================================
    # Bottom Section: Confidence Distribution Heatmap
    # ==================================================================================
    
    ax_generic_heat = fig.add_subplot(gs[2, 0])
    ax_persona_heat = fig.add_subplot(gs[2, 1])
    
    # Generic heatmap
    ax_generic_heat.set_title('Generic AI - Confidence Distribution', 
                             fontsize=14, fontweight='bold', color=colors['generic'], pad=15)
    
    generic_matrix = np.array(generic_probs).reshape(1, -1)
    im_gen = ax_generic_heat.imshow(generic_matrix, cmap='Reds', aspect='auto', 
                                    vmin=0, vmax=100, interpolation='nearest')
    
    ax_generic_heat.set_yticks([0])
    ax_generic_heat.set_yticklabels(['Confidence'], fontsize=11)
    ax_generic_heat.set_xticks(range(len(generic_seq['tokens'])))
    ax_generic_heat.set_xticklabels([f'{i+1}' for i in range(len(generic_seq['tokens']))], fontsize=10)
    ax_generic_heat.set_xlabel('Token Position', fontsize=11, fontweight='bold')
    
    # Add value annotations
    for i, prob in enumerate(generic_probs):
        color = 'white' if prob > 50 else 'black'
        ax_generic_heat.text(i, 0, f'{prob:.0f}', ha='center', va='center',
                           fontsize=10, fontweight='bold', color=color)
    
    # Colorbar
    cbar_gen = plt.colorbar(im_gen, ax=ax_generic_heat, orientation='horizontal', pad=0.15)
    cbar_gen.set_label('Confidence (%)', fontsize=10, fontweight='bold')
    
    ax_generic_heat.text(0.5, -0.35, 'Mostly high confidence (red)\nPredictable pattern', 
                        ha='center', va='top', transform=ax_generic_heat.transAxes,
                        fontsize=10, style='italic',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.2))
    
    # Persona heatmap
    ax_persona_heat.set_title('Persona AI - Confidence Distribution', 
                             fontsize=14, fontweight='bold', color=colors['persona'], pad=15)
    
    persona_matrix = np.array(persona_probs).reshape(1, -1)
    im_per = ax_persona_heat.imshow(persona_matrix, cmap='Blues', aspect='auto',
                                    vmin=0, vmax=100, interpolation='nearest')
    
    ax_persona_heat.set_yticks([0])
    ax_persona_heat.set_yticklabels(['Confidence'], fontsize=11)
    ax_persona_heat.set_xticks(range(len(persona_seq['tokens'])))
    ax_persona_heat.set_xticklabels([f'{i+1}' for i in range(len(persona_seq['tokens']))], fontsize=10)
    ax_persona_heat.set_xlabel('Token Position', fontsize=11, fontweight='bold')
    
    # Add value annotations
    for i, prob in enumerate(persona_probs):
        color = 'white' if prob > 50 else 'black'
        ax_persona_heat.text(i, 0, f'{prob:.0f}', ha='center', va='center',
                           fontsize=10, fontweight='bold', color=color)
    
    # Colorbar
    cbar_per = plt.colorbar(im_per, ax=ax_persona_heat, orientation='horizontal', pad=0.15)
    cbar_per.set_label('Confidence (%)', fontsize=10, fontweight='bold')
    
    ax_persona_heat.text(0.5, -0.35, 'Mixed confidence (varied colors)\nDeliberate word selection', 
                        ha='center', va='top', transform=ax_persona_heat.transAxes,
                        fontsize=10, style='italic',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.2))
    
    # Add summary text
    summary_text = (
        f"🔑 KEY INSIGHT:\n"
        f"Generic AI: First token {generic_first['probability']*100:.1f}% → Avg sequence {avg_gen:.1f}% (consistently high)\n"
        f"Persona AI: First token {persona_first['probability']*100:.1f}% → Avg sequence {avg_per:.1f}% (deliberate variation)\n\n"
        f"The persona starts with extreme confidence, then DELIBERATELY considers alternatives.\n"
        f"Generic AI follows templates. Persona AI makes thoughtful choices."
    )
    
    fig.text(0.5, 0.01, summary_text, ha='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=1', facecolor='#FFE66D', alpha=0.3, edgecolor='black', linewidth=2))
    
    plt.savefig('visualizations/probability_redistribution_detailed.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/probability_redistribution_detailed.png")
    plt.close()

def create_entropy_comparison():
    """
    Create a visualization showing entropy (probability distribution spread) comparison.
    """
    data = load_data()
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Probability Distribution Patterns: Focus vs Deliberation', 
                 fontsize=18, fontweight='bold')
    
    colors = {'generic': '#FF6B6B', 'persona': '#4ECDC4'}
    
    # Analyze first three scenarios
    for idx, scenario_data in enumerate(data[:3]):
        scenario_name = scenario_data['scenario']['name']
        
        # First token comparison
        ax_first = axes[0, idx]
        ax_first.set_title(f'{scenario_name}\nFirst Token', fontsize=12, fontweight='bold')
        
        generic_first_probs = scenario_data['first_token']['without']['top_5_probs']
        persona_first_probs = scenario_data['first_token']['with']['top_5_probs']
        
        x = np.arange(5)
        width = 0.35
        
        bars1 = ax_first.bar(x - width/2, [p*100 for p in generic_first_probs], width,
                            label='Generic', color=colors['generic'], alpha=0.7)
        bars2 = ax_first.bar(x + width/2, [p*100 for p in persona_first_probs], width,
                            label='Persona', color=colors['persona'], alpha=0.7)
        
        ax_first.set_ylabel('Probability (%)', fontsize=10)
        ax_first.set_xlabel('Top 5 Token Options', fontsize=10)
        ax_first.set_xticks(x)
        ax_first.set_xticklabels(['1st', '2nd', '3rd', '4th', '5th'], fontsize=9)
        ax_first.legend(fontsize=9)
        ax_first.grid(True, alpha=0.3, axis='y')
        ax_first.set_ylim(0, 105)
        
        # Add entropy annotation
        generic_entropy = -sum(p * np.log2(p) if p > 0 else 0 for p in generic_first_probs)
        persona_entropy = -sum(p * np.log2(p) if p > 0 else 0 for p in persona_first_probs)
        
        ax_first.text(0.5, 0.95, f'Entropy: Gen={generic_entropy:.2f}, Per={persona_entropy:.2f}',
                     ha='center', va='top', transform=ax_first.transAxes,
                     fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.2))
        
        # Sequence comparison
        ax_seq = axes[1, idx]
        ax_seq.set_title(f'Token Sequence (10 tokens)', fontsize=12, fontweight='bold')
        
        generic_seq_probs = scenario_data['sequence']['without']['probabilities']
        persona_seq_probs = scenario_data['sequence']['with']['probabilities']
        
        positions = range(1, 11)
        ax_seq.plot(positions, [p*100 for p in generic_seq_probs], 'o-',
                   color=colors['generic'], linewidth=2, markersize=6,
                   label=f'Generic (avg: {np.mean(generic_seq_probs)*100:.1f}%)', alpha=0.8)
        ax_seq.plot(positions, [p*100 for p in persona_seq_probs], 's-',
                   color=colors['persona'], linewidth=2, markersize=6,
                   label=f'Persona (avg: {np.mean(persona_seq_probs)*100:.1f}%)', alpha=0.8)
        
        ax_seq.set_ylabel('Confidence (%)', fontsize=10)
        ax_seq.set_xlabel('Token Position', fontsize=10)
        ax_seq.legend(fontsize=8, loc='best')
        ax_seq.grid(True, alpha=0.3)
        ax_seq.set_ylim(0, 105)
        ax_seq.set_xticks(positions)
    
    plt.tight_layout()
    plt.savefig('visualizations/probability_patterns_comparison.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/probability_patterns_comparison.png")
    plt.close()

def main():
    print("\n" + "="*70)
    print("Creating Probability Redistribution Visualizations")
    print("="*70)
    
    print("\n1. Creating detailed probability redistribution visualization...")
    create_probability_redistribution_viz()
    
    print("\n2. Creating probability patterns comparison...")
    create_entropy_comparison()
    
    print("\n" + "="*70)
    print("✓ All probability redistribution visualizations complete!")
    print("="*70)
    print("\nThese visualizations show:")
    print("  - How personas focus confidence on first token (99% vs 46%)")
    print("  - How personas then deliberate on subsequent tokens (varied confidence)")
    print("  - Contrast with generic AI's template-following behavior")
    print("  - Entropy/distribution patterns across multiple scenarios")

if __name__ == "__main__":
    main()
