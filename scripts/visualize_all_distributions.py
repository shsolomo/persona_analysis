"""
Visualizes the complete top-5 probability distribution for all 10 tokens.
Shows how probability mass is distributed at each token position.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

def load_data():
    """Load the full distribution results."""
    with open('results/results_full_distributions.json', 'r') as f:
        return json.load(f)

def create_all_token_distributions_viz():
    """
    Create visualization showing top-5 distributions for all 10 tokens.
    """
    data = load_data()
    
    fig = plt.figure(figsize=(24, 14))
    gs = fig.add_gridspec(2, 10, hspace=0.3, wspace=0.4,
                          left=0.04, right=0.98, top=0.92, bottom=0.06)
    
    colors = {
        'generic': '#FF6B6B',
        'persona': '#4ECDC4',
        'selected': '#FFD93D'
    }
    
    fig.suptitle('Complete Top-5 Probability Distribution Across All Tokens\nGeneric AI vs Persona AI', 
                 fontsize=20, fontweight='bold')
    
    # Get token data
    without_tokens = data['without_persona']['tokens']
    with_tokens = data['with_persona']['tokens']
    
    # Top row: Generic AI (without persona)
    for i, token_data in enumerate(without_tokens):
        ax = fig.add_subplot(gs[0, i])
        
        selected_token = token_data['selected_token']
        top_5_tokens = token_data['top_5_tokens']
        top_5_probs = [p * 100 for p in token_data['top_5_probs']]
        
        # Highlight selected token
        bar_colors = [colors['selected'] if t == selected_token else colors['generic'] 
                      for t in top_5_tokens]
        
        bars = ax.bar(range(5), top_5_probs, color=bar_colors, 
                     edgecolor='black', linewidth=1.5, alpha=0.8)
        
        # Make selected token more prominent
        for j, (bar, token) in enumerate(zip(bars, top_5_tokens)):
            if token == selected_token:
                bar.set_linewidth(2.5)
                bar.set_alpha(1.0)
        
        # Add probability labels
        for j, (bar, prob) in enumerate(zip(bars, top_5_probs)):
            if prob > 5:  # Only label if probability > 5%
                ax.text(j, prob + 3, f'{prob:.0f}%', 
                       ha='center', fontsize=8, fontweight='bold')
        
        # Format axis
        ax.set_ylim(0, 110)
        ax.set_xticks(range(5))
        ax.set_xticklabels([f'"{t[:8]}"' if len(t) <= 8 else f'"{t[:6]}.."' 
                            for t in top_5_tokens], 
                           rotation=45, ha='right', fontsize=7)
        ax.set_title(f'Token {i+1}\n"{selected_token}"', 
                    fontsize=9, fontweight='bold', color=colors['generic'], pad=8)
        
        if i == 0:
            ax.set_ylabel('Probability (%)', fontsize=9, fontweight='bold')
        else:
            ax.set_yticklabels([])
        
        ax.grid(True, alpha=0.2, axis='y')
    
    # Add "Generic AI" label
    fig.text(0.02, 0.72, 'GENERIC AI', rotation=90, va='center', ha='center',
            fontsize=14, fontweight='bold', color=colors['generic'])
    
    # Bottom row: Persona AI (with persona)
    for i, token_data in enumerate(with_tokens):
        ax = fig.add_subplot(gs[1, i])
        
        selected_token = token_data['selected_token']
        top_5_tokens = token_data['top_5_tokens']
        top_5_probs = [p * 100 for p in token_data['top_5_probs']]
        
        # Highlight selected token
        bar_colors = [colors['selected'] if t == selected_token else colors['persona'] 
                      for t in top_5_tokens]
        
        bars = ax.bar(range(5), top_5_probs, color=bar_colors,
                     edgecolor='black', linewidth=1.5, alpha=0.8)
        
        # Make selected token more prominent
        for j, (bar, token) in enumerate(zip(bars, top_5_tokens)):
            if token == selected_token:
                bar.set_linewidth(2.5)
                bar.set_alpha(1.0)
        
        # Add probability labels
        for j, (bar, prob) in enumerate(zip(bars, top_5_probs)):
            if prob > 5:  # Only label if probability > 5%
                ax.text(j, prob + 3, f'{prob:.0f}%', 
                       ha='center', fontsize=8, fontweight='bold')
        
        # Format axis
        ax.set_ylim(0, 110)
        ax.set_xticks(range(5))
        ax.set_xticklabels([f'"{t[:8]}"' if len(t) <= 8 else f'"{t[:6]}.."' 
                            for t in top_5_tokens], 
                           rotation=45, ha='right', fontsize=7)
        ax.set_title(f'Token {i+1}\n"{selected_token}"', 
                    fontsize=9, fontweight='bold', color=colors['persona'], pad=8)
        
        if i == 0:
            ax.set_ylabel('Probability (%)', fontsize=9, fontweight='bold')
        else:
            ax.set_yticklabels([])
        
        ax.grid(True, alpha=0.2, axis='y')
    
    # Add "Persona AI" label
    fig.text(0.02, 0.28, 'PERSONA AI', rotation=90, va='center', ha='center',
            fontsize=14, fontweight='bold', color=colors['persona'])
    
    # Add summary statistics
    without_text = data['without_persona']['full_text']
    with_text = data['with_persona']['full_text']
    
    summary_text = (
        f"PROMPT: '{data['prompt']}'\n\n"
        f"Generic AI: '{without_text}'\n"
        f"   Avg Prob: {data['statistics']['avg_prob_without']*100:.1f}% | "
        f"Avg Entropy: {data['statistics']['avg_entropy_without']:.2f} bits\n\n"
        f"Persona AI: '{with_text}'\n"
        f"   Avg Prob: {data['statistics']['avg_prob_with']*100:.1f}% | "
        f"Avg Entropy: {data['statistics']['avg_entropy_with']:.2f} bits\n\n"
        f"💡 Each column shows the top-5 alternatives at that token position.\n"
        f"Yellow bars = selected token | Red/Teal bars = alternatives not chosen"
    )
    
    fig.text(0.5, 0.015, summary_text, ha='center', va='bottom',
            fontsize=9, family='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='#FFE66D', alpha=0.2, 
                     edgecolor='black', linewidth=1.5))
    
    plt.savefig('visualizations/all_token_distributions_complete.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/all_token_distributions_complete.png")
    plt.close()

def create_entropy_heatmap():
    """
    Create a heatmap showing entropy (distribution spread) at each position.
    """
    data = load_data()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 8))
    fig.suptitle('Probability Distribution Entropy Across Token Sequence\n'
                '(Higher entropy = more spread probability, lower = more focused)', 
                fontsize=16, fontweight='bold')
    
    # Entropy per token
    entropy_without = data['statistics']['entropy_per_token_without']
    entropy_with = data['statistics']['entropy_per_token_with']
    positions = range(1, len(entropy_without) + 1)
    
    # Top: Line plot
    ax1.plot(positions, entropy_without, 'o-', color='#FF6B6B', 
            linewidth=3, markersize=10, label='Generic AI', alpha=0.8)
    ax1.plot(positions, entropy_with, 's-', color='#4ECDC4',
            linewidth=3, markersize=10, label='Persona AI', alpha=0.8)
    
    ax1.set_xlabel('Token Position', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Entropy (bits)', fontsize=12, fontweight='bold')
    ax1.set_xticks(positions)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=11, loc='upper right')
    ax1.set_title('Entropy Per Token Position', fontsize=13, fontweight='bold', pad=10)
    
    # Add average lines
    avg_without = np.mean(entropy_without)
    avg_with = np.mean(entropy_with)
    ax1.axhline(y=avg_without, color='#FF6B6B', linestyle='--', linewidth=2, alpha=0.5)
    ax1.axhline(y=avg_with, color='#4ECDC4', linestyle='--', linewidth=2, alpha=0.5)
    ax1.text(len(positions), avg_without, f'Avg: {avg_without:.2f}', 
            ha='right', va='bottom', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    ax1.text(len(positions), avg_with, f'Avg: {avg_with:.2f}', 
            ha='right', va='top', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Bottom: Heatmap comparison
    entropy_matrix = np.array([entropy_without, entropy_with])
    im = ax2.imshow(entropy_matrix, cmap='RdYlGn_r', aspect='auto', 
                    vmin=0, vmax=max(max(entropy_without), max(entropy_with)))
    
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Generic AI', 'Persona AI'], fontsize=11)
    ax2.set_xticks(range(len(positions)))
    ax2.set_xticklabels([f'{p}' for p in positions], fontsize=10)
    ax2.set_xlabel('Token Position', fontsize=12, fontweight='bold')
    ax2.set_title('Entropy Heatmap (Red = High Spread, Green = Focused)', 
                 fontsize=13, fontweight='bold', pad=10)
    
    # Add value annotations
    for i in range(2):
        for j in range(len(positions)):
            value = entropy_matrix[i, j]
            color = 'white' if value > 1.0 else 'black'
            ax2.text(j, i, f'{value:.2f}', ha='center', va='center',
                    fontsize=9, fontweight='bold', color=color)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax2, orientation='horizontal', pad=0.1)
    cbar.set_label('Entropy (bits)', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('visualizations/entropy_heatmap.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/entropy_heatmap.png")
    plt.close()

def main():
    print("\n" + "="*70)
    print("Creating Complete Token Distribution Visualizations")
    print("="*70)
    
    print("\n1. Creating all token distributions visualization...")
    create_all_token_distributions_viz()
    
    print("\n2. Creating entropy heatmap...")
    create_entropy_heatmap()
    
    print("\n" + "="*70)
    print("✓ All visualizations complete!")
    print("="*70)
    print("\nThese visualizations show:")
    print("  - Top-5 probability distribution for ALL 10 tokens")
    print("  - How probability mass is spread vs concentrated at each position")
    print("  - Entropy (distribution spread) across the sequence")
    print("  - Direct comparison of Generic AI vs Persona AI decision-making")

if __name__ == "__main__":
    main()
