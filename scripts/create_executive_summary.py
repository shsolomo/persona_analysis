"""
Executive Summary: How Personas Work - Three Key Insights

Creates a single, concise visualization explaining personas to any audience
"""

import json
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

def load_data():
    """Load the 50-token distribution results."""
    with open('results/results_full_distributions.json', 'r') as f:
        return json.load(f)

def create_executive_summary():
    """Create a single-page summary of how personas work."""
    data = load_data()
    
    fig = plt.figure(figsize=(20, 14))
    ax = fig.add_subplot(111)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Main title
    title = "How AI Personas Work: Three Key Insights"
    ax.text(5, 9.5, title, ha='center', fontsize=28, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='#4A90E2', 
                    edgecolor='black', linewidth=3, alpha=0.9),
           color='white')
    
    subtitle = "Understanding what personas actually do to AI responses"
    ax.text(5, 9.0, subtitle, ha='center', fontsize=14, style='italic', color='gray')
    
    # Insight 1: Directive & Action-Oriented
    insight1_box = FancyBboxPatch((0.2, 6.5), 9.6, 2.0,
                                 boxstyle="round,pad=0.15",
                                 facecolor='#E8F5E9', edgecolor='#4CAF50',
                                 linewidth=3)
    ax.add_patch(insight1_box)
    
    ax.text(0.5, 8.2, "1", ha='center', va='center', fontsize=40, fontweight='bold',
           color='#4CAF50',
           bbox=dict(boxstyle='circle,pad=0.3', facecolor='white', 
                    edgecolor='#4CAF50', linewidth=3))
    
    ax.text(5, 8.2, "Personas Make Responses More DIRECTIVE & ACTION-ORIENTED", 
           ha='center', fontsize=18, fontweight='bold', color='#2E7D32')
    
    comparison1 = """Generic AI:                                    Persona AI (Azure Architect):
"If your application is running slowly..."    "To address the slowness, we'll follow..."
"There are several steps you can take..."     "Phase 1: Discovery - Analyze Performance Metrics"
"Here's a guide on what to do..."             "Start by collecting data... Use Azure Monitor..."

DIFFERENCE: Generic = conversational suggestions | Persona = structured action plan"""
    
    ax.text(5, 7.2, comparison1, ha='center', va='top', fontsize=11,
           family='monospace',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.95))
    
    # Insight 2: Entropy (WHAT vs HOW)
    insight2_box = FancyBboxPatch((0.2, 3.8), 9.6, 2.3,
                                 boxstyle="round,pad=0.15",
                                 facecolor='#FFF3E0', edgecolor='#FF9800',
                                 linewidth=3)
    ax.add_patch(insight2_box)
    
    ax.text(0.5, 5.7, "2", ha='center', va='center', fontsize=40, fontweight='bold',
           color='#FF9800',
           bbox=dict(boxstyle='circle,pad=0.3', facecolor='white',
                    edgecolor='#FF9800', linewidth=3))
    
    ax.text(5, 5.7, "Personas Shift AI Thinking from HOW → WHAT", 
           ha='center', fontsize=18, fontweight='bold', color='#E65100')
    
    entropy_explanation = """Entropy Analysis = Measuring AI "uncertainty" at each word choice

Generic AI Percolates On:                     Persona AI Percolates On:
├─ HOW to phrase things                       ├─ WHAT domain terms to use
├─ Sentence structure ("If" vs "When")        ├─ Technical precision ("Performance" vs "Metrics")
├─ Word alternatives (similar meanings)       ├─ Domain terminology ("methodology" vs "approach")
└─ Conversational style                       └─ Expert communication patterns

Both have ~0.59 entropy volatility (similar uncertainty frequency)
BUT uncertainty occurs at DIFFERENT words = thinking about DIFFERENT things

INSIGHT: Personas don't make AI "more confident" - they redirect deliberation
from generic phrasing → domain-specific expertise"""
    
    ax.text(5, 5.0, entropy_explanation, ha='center', va='top', fontsize=10.5,
           family='monospace',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.95))
    
    # Insight 3: Probability Distributions
    insight3_box = FancyBboxPatch((0.2, 1.0), 9.6, 2.4,
                                 boxstyle="round,pad=0.15",
                                 facecolor='#E3F2FD', edgecolor='#2196F3',
                                 linewidth=3)
    ax.add_patch(insight3_box)
    
    ax.text(0.5, 3.0, "3", ha='center', va='center', fontsize=40, fontweight='bold',
           color='#2196F3',
           bbox=dict(boxstyle='circle,pad=0.3', facecolor='white',
                    edgecolor='#2196F3', linewidth=3))
    
    ax.text(5, 3.0, "Personas Guide Models Down Domain-Focused Paths", 
           ha='center', fontsize=18, fontweight='bold', color='#0D47A1')
    
    probability_explanation = """Probability Distributions = What words the AI considers and their chances

Example - First Word Choice:
Generic AI:  If (46%), When (36%), Improve (8%), There (6%), A (2%)
             → Spread across generic conversation starters
             
Persona AI:  To (99%), Let's (0.3%), Phase (0.1%), Certainly (0.1%)
             → STRONGLY focused on directive "To address..."

Example - Response Structure:
Generic AI:  "guide" (2%) vs many alternatives: general, structured, systematic...
             → Uncertain about what TYPE of response to give
             
Persona AI:  "structured methodology" (99%+) → IMMEDIATELY knows the approach
             → Domain vocabulary is pre-activated

INSIGHT: Personas create strong "attractor" paths toward domain-appropriate
language, reducing wandering through generic alternatives"""
    
    ax.text(5, 2.3, probability_explanation, ha='center', va='top', fontsize=10.5,
           family='monospace',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.95))
    
    # Bottom summary box
    summary_box = FancyBboxPatch((1.0, 0.05), 8.0, 0.85,
                                boxstyle="round,pad=0.1",
                                facecolor='#FFFDE7', edgecolor='black',
                                linewidth=3)
    ax.add_patch(summary_box)
    
    summary_text = """THE BOTTOM LINE: What Personas Actually Do

Personas are NOT just "system prompts" - they fundamentally reshape how AI generates text:
✓ Create directive, action-oriented responses (not passive suggestions)
✓ Shift thinking from generic phrasing → domain expertise  
✓ Guide probability distributions toward focused, domain-appropriate paths

For Users: Get expert-level responses tailored to specific domains
For Designers: Focus personas on domain terminology, frameworks, and action patterns"""
    
    ax.text(5, 0.5, summary_text, ha='center', va='center', fontsize=11.5,
           family='monospace')
    
    plt.tight_layout()
    plt.savefig('visualizations/executive_summary.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/executive_summary.png")
    plt.close()

def create_simple_diagram():
    """Create a simple before/after diagram."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Generic AI
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    
    ax1.text(5, 9, "Generic AI", ha='center', fontsize=20, fontweight='bold',
            color='#FF6B6B')
    
    # Show scattered thinking
    thoughts_generic = [
        (2, 7, "How to\nstart?"),
        (8, 7, "What\ntone?"),
        (2, 4.5, "Which\nwords?"),
        (8, 4.5, "How to\nstructure?"),
        (5, 2, "What\nstyle?")
    ]
    
    for x, y, text in thoughts_generic:
        circle = Circle((x, y), 0.8, facecolor='#FFE5E5', edgecolor='#FF6B6B', 
                       linewidth=2)
        ax1.add_patch(circle)
        ax1.text(x, y, text, ha='center', va='center', fontsize=9,
                fontweight='bold')
        # Add question marks
        ax1.text(x, y-1.3, "?", ha='center', fontsize=30, color='#FF6B6B', 
                alpha=0.5)
    
    ax1.text(5, 0.5, "Scattered focus on\nHOW to say things", 
            ha='center', fontsize=12, style='italic', color='#666')
    
    # Persona AI
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    ax2.text(5, 9, "Persona AI", ha='center', fontsize=20, fontweight='bold',
            color='#4ECDC4')
    
    # Show focused thinking
    thoughts_persona = [
        (5, 7.5, "Domain\nTerminology"),
        (5, 5.5, "Technical\nPrecision"),
        (5, 3.5, "Expert\nFramework"),
        (5, 1.5, "Action\nSteps")
    ]
    
    for i, (x, y, text) in enumerate(thoughts_persona):
        circle = Circle((x, y), 0.9, facecolor='#E5F5F5', edgecolor='#4ECDC4',
                       linewidth=3)
        ax2.add_patch(circle)
        ax2.text(x, y, text, ha='center', va='center', fontsize=10,
                fontweight='bold')
        
        # Add arrows showing flow
        if i < len(thoughts_persona) - 1:
            arrow = FancyArrowPatch((x, y-1.0), (x, thoughts_persona[i+1][1]+1.0),
                                   arrowstyle='->', mutation_scale=30, 
                                   linewidth=3, color='#4ECDC4')
            ax2.add_patch(arrow)
    
    ax2.text(5, 0.3, "Focused path on\nWHAT to communicate", 
            ha='center', fontsize=12, style='italic', color='#666')
    
    plt.tight_layout()
    plt.savefig('visualizations/simple_before_after.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/simple_before_after.png")
    plt.close()

def main():
    print("\n" + "="*70)
    print("Creating Executive Summary - Concise Explanation")
    print("="*70)
    print("\nGenerating audience-friendly visualizations that explain:")
    print("  1. Directive & Action-Oriented responses")
    print("  2. Entropy shift (HOW → WHAT)")
    print("  3. Domain-focused probability paths\n")
    
    create_executive_summary()
    create_simple_diagram()
    
    print("\n" + "="*70)
    print("SUMMARY COMPLETE")
    print("="*70)
    print("\nCreated two visualizations:")
    print("  • executive_summary.png - Detailed three-insight explanation")
    print("  • simple_before_after.png - Simple visual metaphor")
    print("\nThese distill all findings into concise, shareable formats")
    print("suitable for any audience level.")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
