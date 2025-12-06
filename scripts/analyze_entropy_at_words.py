"""
Analyze Entropy at Specific Words

Shows WHERE entropy occurs - which words cause high/low entropy
in Generic AI vs Persona AI, revealing what each "percolates on"
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

def load_data():
    """Load the 50-token distribution results."""
    with open('results/results_full_distributions.json', 'r') as f:
        return json.load(f)

def analyze_entropy_by_token_type(tokens, entropies):
    """Categorize tokens and analyze entropy patterns."""
    categories = {
        'technical': [],
        'methodological': [],
        'generic': [],
        'structural': []
    }
    
    technical_words = ['Azure', 'Monitor', 'Application', 'Insights', 'Performance', 
                       'Metrics', 'CPU', 'resources', 'infrastructure']
    method_words = ['Phase', 'Discovery', 'analyze', 'structured', 'methodology', 
                   'collecting', 'data', 'Start']
    structural_words = ['**', ':', '\n', '-', '1', '2', '.', ',']
    
    for i, (token, entropy) in enumerate(zip(tokens, entropies)):
        token_clean = token.strip()
        
        if any(word.lower() in token_clean.lower() for word in technical_words):
            categories['technical'].append((i, token, entropy))
        elif any(word.lower() in token_clean.lower() for word in method_words):
            categories['methodological'].append((i, token, entropy))
        elif token in structural_words or token.startswith('**') or token.startswith('\n'):
            categories['structural'].append((i, token, entropy))
        else:
            categories['generic'].append((i, token, entropy))
    
    return categories

def create_word_entropy_comparison():
    """Show which specific words have high/low entropy in each approach."""
    data = load_data()
    
    # Get data
    tokens_without = [t['selected_token'] for t in data['without_persona']['tokens']]
    entropy_without = data['statistics']['entropy_per_token_without']
    
    tokens_with = [t['selected_token'] for t in data['with_persona']['tokens']]
    entropy_with = data['statistics']['entropy_per_token_with']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 12))
    
    colors_entropy = {
        'low': '#4CAF50',    # Green - confident
        'medium': '#FFC107',  # Yellow - moderate uncertainty
        'high': '#F44336'     # Red - high uncertainty
    }
    
    def get_entropy_color(entropy):
        if entropy < 0.4:
            return colors_entropy['low']
        elif entropy < 0.8:
            return colors_entropy['medium']
        else:
            return colors_entropy['high']
    
    # Generic AI
    ax1.set_xlim(0, len(tokens_without))
    ax1.set_ylim(0, 1.5)
    
    for i, (token, entropy) in enumerate(zip(tokens_without, entropy_without)):
        # Draw bar
        color = get_entropy_color(entropy)
        ax1.bar(i, entropy, width=0.8, color=color, alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Add token label
        ax1.text(i, entropy + 0.05, token, rotation=90, ha='center', va='bottom', 
                fontsize=8, fontweight='bold')
    
    ax1.axhline(y=0.4, color='green', linestyle='--', linewidth=1, alpha=0.5)
    ax1.axhline(y=0.8, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax1.set_ylabel('Entropy (bits)', fontsize=12, fontweight='bold')
    ax1.set_title('Generic AI: Entropy at Each Word (Green=Confident, Yellow=Moderate, Red=Uncertain)',
                 fontsize=14, fontweight='bold', pad=10)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add legend
    legend_elements = [
        Rectangle((0, 0), 1, 1, fc=colors_entropy['low'], label='Low Entropy (<0.4) - Confident'),
        Rectangle((0, 0), 1, 1, fc=colors_entropy['medium'], label='Medium Entropy (0.4-0.8) - Moderate'),
        Rectangle((0, 0), 1, 1, fc=colors_entropy['high'], label='High Entropy (>0.8) - Uncertain')
    ]
    ax1.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Persona AI
    ax2.set_xlim(0, len(tokens_with))
    ax2.set_ylim(0, 1.5)
    
    for i, (token, entropy) in enumerate(zip(tokens_with, entropy_with)):
        # Draw bar
        color = get_entropy_color(entropy)
        ax2.bar(i, entropy, width=0.8, color=color, alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Add token label
        ax2.text(i, entropy + 0.05, token, rotation=90, ha='center', va='bottom',
                fontsize=8, fontweight='bold')
    
    ax2.axhline(y=0.4, color='green', linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(y=0.8, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax2.set_xlabel('Token Position', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Entropy (bits)', fontsize=12, fontweight='bold')
    ax2.set_title('Persona AI: Entropy at Each Word (Green=Confident, Yellow=Moderate, Red=Uncertain)',
                 fontsize=14, fontweight='bold', pad=10)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('visualizations/entropy_at_words.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/entropy_at_words.png")
    plt.close()

def create_high_entropy_word_analysis():
    """Identify and compare high-entropy moments."""
    data = load_data()
    
    # Get data
    tokens_without = [t['selected_token'] for t in data['without_persona']['tokens']]
    entropy_without = data['statistics']['entropy_per_token_without']
    probs_without = [t['selected_prob'] for t in data['without_persona']['tokens']]
    
    tokens_with = [t['selected_token'] for t in data['with_persona']['tokens']]
    entropy_with = data['statistics']['entropy_per_token_with']
    probs_with = [t['selected_prob'] for t in data['with_persona']['tokens']]
    
    # Find high entropy moments (> 0.7)
    high_entropy_threshold = 0.7
    
    high_without = [(i, tok, ent, prob) for i, (tok, ent, prob) in 
                    enumerate(zip(tokens_without, entropy_without, probs_without)) 
                    if ent > high_entropy_threshold]
    
    high_with = [(i, tok, ent, prob) for i, (tok, ent, prob) in 
                 enumerate(zip(tokens_with, entropy_with, probs_with)) 
                 if ent > high_entropy_threshold]
    
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.axis('off')
    
    title = "High-Entropy Moments: What Are They 'Percolating On'?"
    ax.text(0.5, 0.97, title, ha='center', fontsize=20, fontweight='bold',
           transform=ax.transAxes)
    
    subtitle = f"(Entropy > {high_entropy_threshold} bits = uncertain, considering multiple options)"
    ax.text(0.5, 0.94, subtitle, ha='center', fontsize=12, style='italic',
           transform=ax.transAxes, color='gray')
    
    # Generic AI high entropy moments
    generic_text = "GENERIC AI - High Entropy Moments:\n\n"
    if high_without:
        for i, tok, ent, prob in high_without[:10]:  # Show first 10
            context_start = max(0, i-2)
            context_end = min(len(tokens_without), i+3)
            context = ''.join(tokens_without[context_start:context_end])
            generic_text += f"  Position {i}: '{tok}' (H={ent:.2f}, P={prob:.0%})\n"
            generic_text += f"    Context: ...{context}...\n\n"
    else:
        generic_text += "  (No high-entropy moments)\n"
    
    ax.text(0.05, 0.85, generic_text, ha='left', va='top', fontsize=10,
           transform=ax.transAxes, family='monospace',
           bbox=dict(boxstyle='round,pad=1', facecolor='#FFE5E5', edgecolor='#FF6B6B', linewidth=2))
    
    # Persona AI high entropy moments
    persona_text = "PERSONA AI - High Entropy Moments:\n\n"
    if high_with:
        for i, tok, ent, prob in high_with[:10]:  # Show first 10
            context_start = max(0, i-2)
            context_end = min(len(tokens_with), i+3)
            context = ''.join(tokens_with[context_start:context_end])
            persona_text += f"  Position {i}: '{tok}' (H={ent:.2f}, P={prob:.0%})\n"
            persona_text += f"    Context: ...{context}...\n\n"
    else:
        persona_text += "  (No high-entropy moments)\n"
    
    ax.text(0.55, 0.85, persona_text, ha='left', va='top', fontsize=10,
           transform=ax.transAxes, family='monospace',
           bbox=dict(boxstyle='round,pad=1', facecolor='#E5F5F5', edgecolor='#4ECDC4', linewidth=2))
    
    # Analysis
    analysis = f"""PATTERN ANALYSIS:

Generic AI High-Entropy Count: {len(high_without)} tokens
Persona AI High-Entropy Count: {len(high_with)} tokens

What this reveals:
• High entropy = Model is uncertain, multiple viable options exist
• The WORDS where high entropy occurs show what each approach struggles with
• Generic AI percolates on: {', '.join([tok for _, tok, _, _ in high_without[:5]]) if high_without else 'N/A'}
• Persona AI percolates on: {', '.join([tok for _, tok, _, _ in high_with[:5]]) if high_with else 'N/A'}

Key Insight: Compare the CONTEXTS of high entropy moments to see where each
approach faces decisions. Persona AI should percolate on domain-specific choices
while Generic AI percolates on general language patterns."""
    
    ax.text(0.5, 0.15, analysis, ha='center', va='top', fontsize=11,
           transform=ax.transAxes, family='monospace',
           bbox=dict(boxstyle='round,pad=1', facecolor='#FFFACD', edgecolor='black', linewidth=2))
    
    plt.savefig('visualizations/high_entropy_words.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/high_entropy_words.png")
    plt.close()
    
    return high_without, high_with

def create_token_alternatives_comparison():
    """Show what alternatives were considered at key decision points."""
    data = load_data()
    
    tokens_without = data['without_persona']['tokens']
    tokens_with = data['with_persona']['tokens']
    
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    fig.suptitle('Top 5 Token Alternatives at Key Decision Points', 
                fontsize=16, fontweight='bold')
    
    # Show first 5 tokens for each
    for i in range(5):
        # Generic AI
        ax = axes[0, i]
        token_data = tokens_without[i]
        selected = token_data['selected_token']
        top_5_tokens = token_data['top_5_tokens']
        top_5_probs = token_data['top_5_probs']
        
        colors = ['#FF6B6B' if tok == selected else '#CCCCCC' for tok in top_5_tokens]
        bars = ax.barh(range(5), top_5_probs, color=colors, edgecolor='black', linewidth=1)
        
        # Add probability labels
        for j, (prob, tok) in enumerate(zip(top_5_probs, top_5_tokens)):
            ax.text(prob + 0.01, j, f'{prob:.1%}', va='center', fontsize=8)
            # Token labels
            ax.text(-0.02, j, tok[:20], va='center', ha='right', fontsize=8, fontweight='bold')
        
        ax.set_xlim(0, 1.0)
        ax.set_ylim(-0.5, 4.5)
        ax.set_xlabel('Probability', fontsize=9)
        ax.set_title(f'Generic AI\nToken {i+1}: "{selected}"', fontsize=10, fontweight='bold')
        ax.set_yticks([])
        ax.grid(True, alpha=0.3, axis='x')
        
        # Persona AI
        ax = axes[1, i]
        token_data = tokens_with[i]
        selected = token_data['selected_token']
        top_5_tokens = token_data['top_5_tokens']
        top_5_probs = token_data['top_5_probs']
        
        colors = ['#4ECDC4' if tok == selected else '#CCCCCC' for tok in top_5_tokens]
        bars = ax.barh(range(5), top_5_probs, color=colors, edgecolor='black', linewidth=1)
        
        for j, (prob, tok) in enumerate(zip(top_5_probs, top_5_tokens)):
            ax.text(prob + 0.01, j, f'{prob:.1%}', va='center', fontsize=8)
            ax.text(-0.02, j, tok[:20], va='center', ha='right', fontsize=8, fontweight='bold')
        
        ax.set_xlim(0, 1.0)
        ax.set_ylim(-0.5, 4.5)
        ax.set_xlabel('Probability', fontsize=9)
        ax.set_title(f'Persona AI\nToken {i+1}: "{selected}"', fontsize=10, fontweight='bold')
        ax.set_yticks([])
        ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('visualizations/token_alternatives_comparison.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/token_alternatives_comparison.png")
    plt.close()

def main():
    print("\n" + "="*70)
    print("Analyzing WHERE Entropy Occurs: Word-Level Analysis")
    print("="*70)
    print("\nThis reveals WHICH WORDS cause high vs low entropy")
    print("and what each approach is 'percolating on'.\n")
    
    print("1. Creating word-by-word entropy visualization...")
    create_word_entropy_comparison()
    
    print("\n2. Identifying high-entropy moments...")
    high_without, high_with = create_high_entropy_word_analysis()
    
    print("\n3. Comparing token alternatives at decision points...")
    create_token_alternatives_comparison()
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nGeneric AI: {len(high_without)} high-entropy words")
    print(f"Persona AI: {len(high_with)} high-entropy words")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
