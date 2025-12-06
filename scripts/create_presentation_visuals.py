"""
Create presentation visualizations for AI Summit slides 7 and 8
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def load_data():
    """Load the results data."""
    with open('results/results_full_distributions.json', 'r') as f:
        return json.load(f)

def create_first_token_breakdown():
    """Slide 7: First-Token Probability Breakdown visualization."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Generic AI first token probabilities
    generic_tokens = ['If', 'When', 'Improve', 'There', 'A']
    generic_probs = [46, 36, 8, 6, 2]
    generic_colors = ['#FF6B6B', '#FF8E8E', '#FFB4B4', '#FFD4D4', '#FFECEC']
    
    ax1 = axes[0]
    bars1 = ax1.barh(generic_tokens[::-1], generic_probs[::-1], color=generic_colors[::-1], 
                     edgecolor='#CC5555', linewidth=2)
    ax1.set_xlabel('Probability (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Generic AI\nFirst Token Options', fontsize=16, fontweight='bold', color='#CC5555')
    ax1.set_xlim(0, 100)
    ax1.axvline(x=50, color='gray', linestyle='--', alpha=0.5, label='50% threshold')
    
    # Add percentage labels
    for bar, prob in zip(bars1, generic_probs[::-1]):
        ax1.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, 
                f'{prob}%', va='center', fontsize=11, fontweight='bold')
    
    ax1.text(50, -0.8, 'Spread across 5+ options\n"Which way should I start?"', 
            ha='center', fontsize=10, style='italic', color='#666')
    
    # Persona AI first token probabilities
    persona_tokens = ['To', "Let's", 'Phase', 'Other']
    persona_probs = [99, 0.3, 0.1, 0.6]
    persona_colors = ['#4ECDC4', '#B8E8E4', '#D4F1EF', '#E8F8F7']
    
    ax2 = axes[1]
    bars2 = ax2.barh(persona_tokens[::-1], persona_probs[::-1], color=persona_colors[::-1],
                     edgecolor='#3BA99F', linewidth=2)
    ax2.set_xlabel('Probability (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Persona AI\nFirst Token Options', fontsize=16, fontweight='bold', color='#3BA99F')
    ax2.set_xlim(0, 100)
    ax2.axvline(x=50, color='gray', linestyle='--', alpha=0.5)
    
    # Add percentage labels
    for bar, prob in zip(bars2, persona_probs[::-1]):
        label = f'{prob}%' if prob >= 1 else f'{prob:.1f}%'
        ax2.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, 
                label, va='center', fontsize=11, fontweight='bold')
    
    ax2.text(50, -0.8, '99% locked on directive\n"To address..."', 
            ha='center', fontsize=10, style='italic', color='#666')
    
    # Add main title
    fig.suptitle('First-Token Probability Breakdown\nHow Personas Create Confident Starts', 
                fontsize=18, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig('visualizations/slide7_first_token_breakdown.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/slide7_first_token_breakdown.png")
    plt.close()


def create_key_metrics_table():
    """Slide 8: Key Metrics visualization as a styled table."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis('off')
    
    # Data for the table
    columns = ['Metric', 'Generic AI', 'Persona AI', 'Interpretation']
    data = [
        ['Average Probability', '0.756', '0.781', 'Slightly higher focus'],
        ['Average Entropy', '0.557', '0.581', 'Similar uncertainty levels'],
        ['Entropy Volatility (σ)', '0.585', '0.604', 'Same amount of "thinking"'],
        ['High-Entropy Words (H>0.7)', '17', '19', 'Similar deliberation frequency'],
    ]
    
    # Create table
    table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2)
    
    # Style header
    for i in range(len(columns)):
        cell = table[(0, i)]
        cell.set_facecolor('#2C3E50')
        cell.set_text_props(color='white', fontweight='bold')
    
    # Style data rows with alternating colors
    for i in range(1, len(data) + 1):
        for j in range(len(columns)):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#ECF0F1')
            else:
                cell.set_facecolor('#FFFFFF')
            
            # Highlight the interpretation column
            if j == 3:
                cell.set_text_props(style='italic', color='#27AE60')
    
    ax.set_title('Key Metrics from Probability Analysis\nComparing Generic vs Persona AI', 
                fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('visualizations/slide8_key_metrics_table.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/slide8_key_metrics_table.png")
    plt.close()


def create_critical_insight():
    """Slide 8: The Critical Insight - WHERE entropy occurs."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Generic AI - entropy on sentence structure
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    
    # Title
    ax1.text(5, 9.5, 'Generic AI', fontsize=18, fontweight='bold', ha='center', color='#CC5555')
    ax1.text(5, 8.8, 'High Entropy at: Sentence Structure', fontsize=12, ha='center', color='#666')
    
    # Show the deliberation
    options = ['"If"', '"When"', '"Improve"']
    probs = ['46%', '36%', '8%']
    y_positions = [6.5, 5, 3.5]
    
    for opt, prob, y in zip(options, probs, y_positions):
        box = mpatches.FancyBboxPatch((2, y-0.4), 6, 0.8,
                                      boxstyle="round,pad=0.1",
                                      facecolor='#FFE5E5', edgecolor='#FF6B6B',
                                      linewidth=2)
        ax1.add_patch(box)
        ax1.text(5, y, f'{opt}  →  {prob}', ha='center', va='center', 
                fontsize=13, fontweight='bold')
    
    ax1.text(5, 2, 'Entropy H = 1.69', fontsize=14, ha='center', 
            fontweight='bold', color='#CC5555',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='#CC5555'))
    
    ax1.text(5, 0.8, '"How should I start\nthis sentence?"', fontsize=11, 
            ha='center', style='italic', color='#888')
    
    # Persona AI - entropy on domain terminology
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    # Title
    ax2.text(5, 9.5, 'Persona AI', fontsize=18, fontweight='bold', ha='center', color='#3BA99F')
    ax2.text(5, 8.8, 'High Entropy at: Domain Terminology', fontsize=12, ha='center', color='#666')
    
    # Show the deliberation
    options2 = ['"Performance"', '"Metrics"', '"Monitoring"']
    probs2 = ['45%', '35%', '15%']
    
    for opt, prob, y in zip(options2, probs2, y_positions):
        box = mpatches.FancyBboxPatch((2, y-0.4), 6, 0.8,
                                      boxstyle="round,pad=0.1",
                                      facecolor='#E5F5F5', edgecolor='#4ECDC4',
                                      linewidth=2)
        ax2.add_patch(box)
        ax2.text(5, y, f'{opt}  →  {prob}', ha='center', va='center',
                fontsize=13, fontweight='bold')
    
    ax2.text(5, 2, 'Entropy H = 1.97', fontsize=14, ha='center',
            fontweight='bold', color='#3BA99F',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='#3BA99F'))
    
    ax2.text(5, 0.8, '"Which technical term\nis most precise?"', fontsize=11,
            ha='center', style='italic', color='#888')
    
    # Main title
    fig.suptitle('The Critical Insight: Same Uncertainty, Different Focus\n' +
                'Both have σ ≈ 0.59 entropy volatility — but deliberate on DIFFERENT things',
                fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig('visualizations/slide8_critical_insight.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/slide8_critical_insight.png")
    plt.close()


def create_combined_slide8():
    """Create a combined visual for slide 8 with metrics and insight."""
    fig = plt.figure(figsize=(16, 10))
    
    # Top half: Key metrics table
    ax_table = fig.add_axes([0.1, 0.55, 0.8, 0.35])
    ax_table.axis('off')
    
    columns = ['Metric', 'Generic AI', 'Persona AI', 'Meaning']
    data = [
        ['Average Probability', '0.756', '0.781', '↑ Slightly higher focus'],
        ['Average Entropy', '0.557', '0.581', '≈ Similar uncertainty'],
        ['Entropy Volatility (σ)', '0.585', '0.604', '≈ Same "thinking" amount'],
        ['High-Entropy Words', '17', '19', '≈ Similar deliberation frequency'],
    ]
    
    table = ax_table.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 2.2)
    
    for i in range(len(columns)):
        cell = table[(0, i)]
        cell.set_facecolor('#2C3E50')
        cell.set_text_props(color='white', fontweight='bold')
    
    for i in range(1, len(data) + 1):
        for j in range(len(columns)):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#ECF0F1')
            if j == 3:
                cell.set_text_props(color='#27AE60', fontweight='bold')
    
    ax_table.set_title('Key Metrics: Similar Patterns, Different Focus', 
                       fontsize=16, fontweight='bold', pad=10)
    
    # Bottom half: Critical insight comparison
    ax_left = fig.add_axes([0.05, 0.05, 0.42, 0.42])
    ax_right = fig.add_axes([0.53, 0.05, 0.42, 0.42])
    
    for ax in [ax_left, ax_right]:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
    
    # Generic side
    ax_left.text(5, 9, 'Generic AI Deliberates On:', fontsize=14, fontweight='bold', 
                ha='center', color='#CC5555')
    
    generic_items = ['"If" vs "When" vs "Improve"', 'Sentence structure', 'Conversational style']
    for i, item in enumerate(generic_items):
        y = 7 - i * 1.5
        box = mpatches.FancyBboxPatch((1, y-0.4), 8, 0.8,
                                      boxstyle="round,pad=0.1",
                                      facecolor='#FFE5E5', edgecolor='#FF6B6B', linewidth=2)
        ax_left.add_patch(box)
        ax_left.text(5, y, item, ha='center', va='center', fontsize=12)
    
    ax_left.text(5, 1.5, 'HOW to phrase things', fontsize=14, fontweight='bold',
                ha='center', color='#CC5555',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='#CC5555', linewidth=2))
    
    # Persona side
    ax_right.text(5, 9, 'Persona AI Deliberates On:', fontsize=14, fontweight='bold',
                 ha='center', color='#3BA99F')
    
    persona_items = ['"Performance" vs "Metrics"', '"methodology" vs "approach"', 'Technical precision']
    for i, item in enumerate(persona_items):
        y = 7 - i * 1.5
        box = mpatches.FancyBboxPatch((1, y-0.4), 8, 0.8,
                                      boxstyle="round,pad=0.1",
                                      facecolor='#E5F5F5', edgecolor='#4ECDC4', linewidth=2)
        ax_right.add_patch(box)
        ax_right.text(5, y, item, ha='center', va='center', fontsize=12)
    
    ax_right.text(5, 1.5, 'WHAT domain terms to use', fontsize=14, fontweight='bold',
                 ha='center', color='#3BA99F',
                 bbox=dict(boxstyle='round', facecolor='white', edgecolor='#3BA99F', linewidth=2))
    
    # Main title
    fig.suptitle('Metrics That Prove It: Entropy Analysis\n' +
                'Same amount of thinking — about DIFFERENT things',
                fontsize=18, fontweight='bold', y=0.98)
    
    plt.savefig('visualizations/slide8_combined.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/slide8_combined.png")
    plt.close()


def main():
    print("\n" + "="*60)
    print("Creating Presentation Visualizations")
    print("="*60)
    
    print("\nSlide 7: First-Token Probability Breakdown...")
    create_first_token_breakdown()
    
    print("\nSlide 8: Key Metrics Table...")
    create_key_metrics_table()
    
    print("\nSlide 8: Critical Insight Comparison...")
    create_critical_insight()
    
    print("\nSlide 8: Combined Visualization...")
    create_combined_slide8()
    
    print("\n" + "="*60)
    print("COMPLETE! Created visualizations:")
    print("  • slide7_first_token_breakdown.png")
    print("  • slide8_key_metrics_table.png")
    print("  • slide8_critical_insight.png")
    print("  • slide8_combined.png")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
