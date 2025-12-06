"""
Creates a simple, clear diagram showing how personas shift probabilities.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

def create_simple_explanation_diagram():
    """Create a clear, simple diagram showing the core concept."""
    
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('How Personas Change AI Responses', fontsize=20, fontweight='bold', y=0.98)
    
    # Create main grid
    gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3, 
                          left=0.08, right=0.92, top=0.92, bottom=0.08)
    
    colors = {
        'generic': '#FF6B6B',
        'persona': '#4ECDC4',
        'highlight': '#FFE66D',
        'text': '#2C3E50'
    }
    
    # ============================================================================
    # Panel 1: The Question
    # ============================================================================
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axis('off')
    
    # Question box
    question_box = FancyBboxPatch((0.2, 0.3), 0.6, 0.4,
                                  boxstyle="round,pad=0.1",
                                  facecolor='#F0F0F0',
                                  edgecolor=colors['text'],
                                  linewidth=3)
    ax1.add_patch(question_box)
    ax1.text(0.5, 0.5, 'Question: "My application is slow. What should I do?"',
            ha='center', va='center', fontsize=16, fontweight='bold',
            transform=ax1.transAxes)
    
    ax1.text(0.5, 0.1, 'We ask the SAME question to two different AIs...',
            ha='center', va='center', fontsize=12, style='italic',
            transform=ax1.transAxes)
    
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    
    # ============================================================================
    # Panel 2: Generic AI Word Choices
    # ============================================================================
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_title('Generic AI (No Persona)', fontsize=14, fontweight='bold', 
                 color=colors['generic'], pad=20)
    
    # Word probabilities
    words = ['If', 'When', 'Impro', 'There', 'A']
    probs = [46, 36, 8, 6, 2]
    
    bars = ax2.barh(range(len(words)), probs, color=colors['generic'], alpha=0.7)
    
    # Highlight the chosen word
    bars[0].set_color(colors['generic'])
    bars[0].set_alpha(1.0)
    bars[0].set_linewidth(3)
    bars[0].set_edgecolor('black')
    
    ax2.set_yticks(range(len(words)))
    ax2.set_yticklabels([f'"{w}"' for w in words], fontsize=12)
    ax2.set_xlabel('Probability (%)', fontsize=11)
    ax2.set_xlim(0, 105)
    ax2.invert_yaxis()
    ax2.grid(True, alpha=0.3, axis='x')
    
    # Add annotation
    ax2.annotate('CHOSEN ✓\n(Uncertain,\nConditional)',
                xy=(probs[0], 0), xytext=(probs[0] + 25, 0),
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=colors['generic'], alpha=0.3),
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['generic']))
    
    ax2.text(0.5, -0.15, 'Probabilities are SPREAD OUT\n(No clear winner)',
            ha='center', va='top', fontsize=10, style='italic',
            transform=ax2.transAxes,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.2))
    
    # ============================================================================
    # Panel 3: Persona AI Word Choices
    # ============================================================================
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_title('Azure Architect AI (With Persona)', fontsize=14, fontweight='bold',
                 color=colors['persona'], pad=20)
    
    # Word probabilities (dramatically different!)
    words_persona = ['To', "Let's", 'When', 'Phase', 'Impro']
    probs_persona = [99, 0.1, 0.1, 0.09, 0.07]
    
    bars_p = ax3.barh(range(len(words_persona)), probs_persona, 
                     color=colors['persona'], alpha=0.7)
    
    # Highlight the chosen word
    bars_p[0].set_color(colors['persona'])
    bars_p[0].set_alpha(1.0)
    bars_p[0].set_linewidth(3)
    bars_p[0].set_edgecolor('black')
    
    ax3.set_yticks(range(len(words_persona)))
    ax3.set_yticklabels([f'"{w}"' for w in words_persona], fontsize=12)
    ax3.set_xlabel('Probability (%)', fontsize=11)
    ax3.set_xlim(0, 105)
    ax3.invert_yaxis()
    ax3.grid(True, alpha=0.3, axis='x')
    
    # Add annotation
    ax3.annotate('CHOSEN ✓\n(Confident,\nDirective)',
                xy=(probs_persona[0], 0), xytext=(probs_persona[0] - 30, 0.5),
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=colors['persona'], alpha=0.3),
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['persona']))
    
    ax3.text(0.5, -0.15, 'Probabilities are CONCENTRATED\n(Clear expert direction)',
            ha='center', va='top', fontsize=10, style='italic',
            transform=ax3.transAxes,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.2))
    
    # ============================================================================
    # Panel 4: The Results
    # ============================================================================
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('off')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    
    # Left response (Generic)
    generic_box = FancyBboxPatch((0.02, 0.35), 0.44, 0.55,
                                boxstyle="round,pad=0.02",
                                facecolor='white',
                                edgecolor=colors['generic'],
                                linewidth=3)
    ax4.add_patch(generic_box)
    
    ax4.text(0.24, 0.85, 'Generic Response:', ha='center', va='top',
            fontsize=12, fontweight='bold', color=colors['generic'],
            transform=ax4.transAxes)
    
    generic_text = (
        '"If your application is slow,\n'
        'there could be many reasons.\n'
        'You might want to check your\n'
        'database queries, network latency,\n'
        'or server resources..."'
    )
    ax4.text(0.24, 0.65, generic_text, ha='center', va='top',
            fontsize=10, transform=ax4.transAxes,
            bbox=dict(boxstyle='round,pad=0.8', facecolor=colors['generic'], 
                     alpha=0.1, edgecolor=colors['generic']))
    
    ax4.text(0.24, 0.15, '❌ Uncertain\n❌ Exploratory\n❌ Non-committal',
            ha='center', va='center', fontsize=10, transform=ax4.transAxes,
            style='italic')
    
    # Right response (Persona)
    persona_box = FancyBboxPatch((0.54, 0.35), 0.44, 0.55,
                                boxstyle="round,pad=0.02",
                                facecolor='white',
                                edgecolor=colors['persona'],
                                linewidth=3)
    ax4.add_patch(persona_box)
    
    ax4.text(0.76, 0.85, 'Architect Response:', ha='center', va='top',
            fontsize=12, fontweight='bold', color=colors['persona'],
            transform=ax4.transAxes)
    
    persona_text = (
        '"To improve performance, we\'ll\n'
        'analyze three key areas:\n'
        '1. Database query optimization\n'
        '2. Caching strategy\n'
        '3. Resource scaling..."'
    )
    ax4.text(0.76, 0.65, persona_text, ha='center', va='top',
            fontsize=10, transform=ax4.transAxes,
            bbox=dict(boxstyle='round,pad=0.8', facecolor=colors['persona'],
                     alpha=0.1, edgecolor=colors['persona']))
    
    ax4.text(0.76, 0.15, '✓ Confident\n✓ Action-oriented\n✓ Structured',
            ha='center', va='center', fontsize=10, transform=ax4.transAxes,
            style='italic')
    
    # Add the key finding
    key_finding_box = FancyBboxPatch((0.15, 0.02), 0.7, 0.12,
                                    boxstyle="round,pad=0.01",
                                    facecolor=colors['highlight'],
                                    edgecolor='black',
                                    linewidth=2,
                                    alpha=0.3)
    ax4.add_patch(key_finding_box)
    
    ax4.text(0.5, 0.08, '🔑 KEY FINDING: Persona increased "To" confidence from <5% to 99% (+118%)',
            ha='center', va='center', fontsize=13, fontweight='bold',
            transform=ax4.transAxes)
    
    plt.savefig('visualizations/simple_explanation_diagram.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/simple_explanation_diagram.png")
    plt.close()


def create_word_choice_journey():
    """Show how the first word choice affects everything after."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('How the First Word Shapes the Entire Response', 
                fontsize=18, fontweight='bold')
    
    colors = {'generic': '#FF6B6B', 'persona': '#4ECDC4'}
    
    # Left path: Starting with "If"
    ax1.set_title('Path 1: Starting with "If"', fontsize=14, 
                 fontweight='bold', color=colors['generic'])
    ax1.axis('off')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    
    # Create branching tree
    y_positions = [0.9, 0.7, 0.5, 0.3, 0.1]
    
    # First word
    ax1.text(0.5, y_positions[0], '"If"', ha='center', va='center',
            fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=colors['generic'], alpha=0.5))
    
    # Likely next words
    next_words_if = [
        'your/the',
        'experiencing/having',
        'issues/problems',
        'might/could/should',
        'consider/try/check'
    ]
    
    for i, words in enumerate(next_words_if):
        if i >= len(y_positions) - 1:
            break
        ax1.arrow(0.5, y_positions[i] - 0.05, 0, -0.1,
                 head_width=0.03, head_length=0.02, fc=colors['generic'], 
                 ec=colors['generic'], alpha=0.5)
        ax1.text(0.5, y_positions[i+1], words, ha='center', va='center',
                fontsize=12,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor=colors['generic'], alpha=0.7))
    
    ax1.text(0.5, 0.02, 'Leads to: Exploratory, conditional response',
            ha='center', va='bottom', fontsize=11, style='italic',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=colors['generic'], alpha=0.2))
    
    # Right path: Starting with "To"
    ax2.set_title('Path 2: Starting with "To"', fontsize=14,
                 fontweight='bold', color=colors['persona'])
    ax2.axis('off')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    
    # First word
    ax2.text(0.5, y_positions[0], '"To"', ha='center', va='center',
            fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=colors['persona'], alpha=0.5))
    
    # Likely next words
    next_words_to = [
        'improve/fix/resolve',
        'performance/this',
        "we'll/I'll",
        'analyze/implement',
        'three/specific'
    ]
    
    for i, words in enumerate(next_words_to):
        if i >= len(y_positions) - 1:
            break
        ax2.arrow(0.5, y_positions[i] - 0.05, 0, -0.1,
                 head_width=0.03, head_length=0.02, fc=colors['persona'],
                 ec=colors['persona'], alpha=0.5)
        ax2.text(0.5, y_positions[i+1], words, ha='center', va='center',
                fontsize=12,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                         edgecolor=colors['persona'], alpha=0.7))
    
    ax2.text(0.5, 0.02, 'Leads to: Directive, action-oriented response',
            ha='center', va='bottom', fontsize=11, style='italic',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=colors['persona'], alpha=0.2))
    
    plt.tight_layout()
    plt.savefig('visualizations/word_choice_journey.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/word_choice_journey.png")
    plt.close()


def create_analogy_diagram():
    """Create visual analogies to explain the concept."""
    
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle('Understanding Personas Through Analogies',
                fontsize=18, fontweight='bold')
    
    # Create 2x2 grid
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Analogy 1: Restaurant
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    
    ax1.text(0.5, 0.95, '🍽️ Restaurant Analogy', ha='center', va='top',
            fontsize=14, fontweight='bold', transform=ax1.transAxes)
    
    ax1.text(0.1, 0.7, 'Random Person:', ha='left', va='top',
            fontsize=11, fontweight='bold', color='#FF6B6B',
            transform=ax1.transAxes)
    ax1.text(0.15, 0.6, '"Well, the menu has\nmany options..."',
            ha='left', va='top', fontsize=10, style='italic',
            transform=ax1.transAxes)
    
    ax1.text(0.1, 0.4, 'Expert Chef:', ha='left', va='top',
            fontsize=11, fontweight='bold', color='#4ECDC4',
            transform=ax1.transAxes)
    ax1.text(0.15, 0.3, '"Get the salmon,\nmedium-rare."',
            ha='left', va='top', fontsize=10, style='italic',
            transform=ax1.transAxes)
    
    ax1.text(0.5, 0.05, 'Same question, different confidence!',
            ha='center', va='bottom', fontsize=9, style='italic',
            transform=ax1.transAxes,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.2))
    
    # Analogy 2: Doctor
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis('off')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    
    ax2.text(0.5, 0.95, '🏥 Doctor Analogy', ha='center', va='top',
            fontsize=14, fontweight='bold', transform=ax2.transAxes)
    
    ax2.text(0.1, 0.7, 'Medical Student:', ha='left', va='top',
            fontsize=11, fontweight='bold', color='#FF6B6B',
            transform=ax2.transAxes)
    ax2.text(0.15, 0.6, '"Headaches can have\nmany causes..."',
            ha='left', va='top', fontsize=10, style='italic',
            transform=ax2.transAxes)
    
    ax2.text(0.1, 0.4, 'Experienced Doctor:', ha='left', va='top',
            fontsize=11, fontweight='bold', color='#4ECDC4',
            transform=ax2.transAxes)
    ax2.text(0.15, 0.3, '"Take 400mg ibuprofen.\nCall if it persists."',
            ha='left', va='top', fontsize=10, style='italic',
            transform=ax2.transAxes)
    
    ax2.text(0.5, 0.05, 'Experience breeds confidence!',
            ha='center', va='bottom', fontsize=9, style='italic',
            transform=ax2.transAxes,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.2))
    
    # Analogy 3: Mechanic
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.axis('off')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    
    ax3.text(0.5, 0.95, '🔧 Mechanic Analogy', ha='center', va='top',
            fontsize=14, fontweight='bold', transform=ax3.transAxes)
    
    ax3.text(0.1, 0.7, 'Random Person:', ha='left', va='top',
            fontsize=11, fontweight='bold', color='#FF6B6B',
            transform=ax3.transAxes)
    ax3.text(0.15, 0.6, '"If your car is making\na noise, it could be..."',
            ha='left', va='top', fontsize=10, style='italic',
            transform=ax3.transAxes)
    
    ax3.text(0.1, 0.4, 'Expert Mechanic:', ha='left', va='top',
            fontsize=11, fontweight='bold', color='#4ECDC4',
            transform=ax3.transAxes)
    ax3.text(0.15, 0.3, '"To fix that noise,\ncheck the brake pads."',
            ha='left', va='top', fontsize=10, style='italic',
            transform=ax3.transAxes)
    
    ax3.text(0.5, 0.05, 'Experts give directions, not explanations!',
            ha='center', va='bottom', fontsize=9, style='italic',
            transform=ax3.transAxes,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.2))
    
    # Analogy 4: Voting
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    
    ax4.text(0.5, 0.95, '🗳️ Voting Analogy', ha='center', va='top',
            fontsize=14, fontweight='bold', transform=ax4.transAxes)
    
    ax4.text(0.1, 0.7, 'Committee (Generic):', ha='left', va='top',
            fontsize=11, fontweight='bold', color='#FF6B6B',
            transform=ax4.transAxes)
    ax4.text(0.15, 0.6, 'Option A: 46 votes\nOption B: 36 votes\nOption C: 8 votes',
            ha='left', va='top', fontsize=10, style='italic',
            transform=ax4.transAxes)
    ax4.text(0.15, 0.45, '→ Close race!', ha='left', va='top',
            fontsize=9, transform=ax4.transAxes)
    
    ax4.text(0.1, 0.3, 'Expert (Persona):', ha='left', va='top',
            fontsize=11, fontweight='bold', color='#4ECDC4',
            transform=ax4.transAxes)
    ax4.text(0.15, 0.2, 'Option A: 99 votes\nAll others: <1 vote',
            ha='left', va='top', fontsize=10, style='italic',
            transform=ax4.transAxes)
    ax4.text(0.15, 0.08, '→ Landslide!', ha='left', va='top',
            fontsize=9, transform=ax4.transAxes)
    
    plt.tight_layout()
    plt.savefig('visualizations/analogy_diagram.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/analogy_diagram.png")
    plt.close()


def main():
    print("\n" + "="*60)
    print("Creating Simple Explanation Diagrams")
    print("="*60)
    
    print("\n1. Creating main explanation diagram...")
    create_simple_explanation_diagram()
    
    print("\n2. Creating word choice journey...")
    create_word_choice_journey()
    
    print("\n3. Creating analogy diagrams...")
    create_analogy_diagram()
    
    print("\n" + "="*60)
    print("✓ All explanation diagrams complete!")
    print("="*60)
    print("\nThese diagrams will help you explain:")
    print("  - How probabilities shift")
    print("  - Why the first word matters")
    print("  - Real-world analogies")


if __name__ == "__main__":
    main()
