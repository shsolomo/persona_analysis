"""
Create a Summary of What Each Approach "Percolates On"

Shows the key insight: WHERE entropy occurs reveals WHAT matters to each approach
"""

import json
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

def load_data():
    """Load the 50-token distribution results."""
    with open('results/results_full_distributions.json', 'r') as f:
        return json.load(f)

def create_percolation_summary():
    """Create a clear summary of what each approach percolates on."""
    data = load_data()
    
    # Get high entropy moments
    tokens_without = data['without_persona']['tokens']
    tokens_with = data['with_persona']['tokens']
    entropy_without = data['statistics']['entropy_per_token_without']
    entropy_with = data['statistics']['entropy_per_token_with']
    
    # Identify high entropy words (>0.7)
    high_entropy_threshold = 0.7
    
    high_without = [(i, t['selected_token'], e) for i, (t, e) in 
                    enumerate(zip(tokens_without, entropy_without)) if e > high_entropy_threshold]
    high_with = [(i, t['selected_token'], e) for i, (t, e) in 
                 enumerate(zip(tokens_with, entropy_with)) if e > high_entropy_threshold]
    
    fig = plt.figure(figsize=(20, 12))
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    # Title
    title = "What Are They 'Percolating On'? Understanding WHERE Entropy Occurs"
    ax.text(0.5, 0.97, title, ha='center', fontsize=22, fontweight='bold',
           transform=ax.transAxes)
    
    subtitle = "High entropy = uncertainty = multiple viable options being weighed"
    ax.text(0.5, 0.94, subtitle, ha='center', fontsize=14, style='italic',
           transform=ax.transAxes, color='gray')
    
    # Generic AI section
    generic_box = FancyBboxPatch((0.02, 0.55), 0.46, 0.35,
                                boxstyle="round,pad=0.02", 
                                facecolor='#FFE5E5', edgecolor='#FF6B6B', 
                                linewidth=3, transform=ax.transAxes)
    ax.add_patch(generic_box)
    
    generic_title = "GENERIC AI\nPercolates On: General Language Patterns"
    ax.text(0.25, 0.87, generic_title, ha='center', fontsize=16, fontweight='bold',
           transform=ax.transAxes, color='#FF6B6B')
    
    generic_high_entropy = f"""High Entropy Moments ({len(high_without)} total):

First Token: "If" (H=1.69) - Choosing how to start
  Alternatives: When, Improve, There, A
  
"potentially" (H=1.95) vs "improve" (H=0.90)
  Wrestling with: address, improve, resolve, fix
  
"guide" (H=1.71) - What type of response?
  Alternatives: general, structured, systematic, comprehensive
  
"what" (H=1.54) vs "do" (H=1.29)
  Deciding conversational structure

PATTERN: Percolates on HOW TO SAY IT
• Sentence structure ("If" vs "When")
• Word choice for similar meanings
• Generic language decisions
• Conversational style"""
    
    ax.text(0.04, 0.85, generic_high_entropy, ha='left', va='top', fontsize=11,
           transform=ax.transAxes, family='monospace',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))
    
    # Persona AI section
    persona_box = FancyBboxPatch((0.52, 0.55), 0.46, 0.35,
                                boxstyle="round,pad=0.02",
                                facecolor='#E5F5F5', edgecolor='#4ECDC4',
                                linewidth=3, transform=ax.transAxes)
    ax.add_patch(persona_box)
    
    persona_title = "PERSONA AI (Azure Architect)\nPercolates On: Domain-Specific Choices"
    ax.text(0.75, 0.87, persona_title, ha='center', fontsize=16, fontweight='bold',
           transform=ax.transAxes, color='#4ECDC4')
    
    persona_high_entropy = f"""High Entropy Moments ({len(high_with)} total):

"we'll" (H=1.74) - Collaborative approach decision
  Alternatives: we, let's, I, I'll
  
"methodology" (H=1.56) vs "structured" (H=1.91)
  Domain terminology: methodology, approach, workflow, process
  
"Performance" (H=1.97) vs "Metrics" (H=1.12)
  Technical precision: Performance, Requirements, Current
  
"Analyze" (H=1.74) - Domain-specific action
  Alternatives: Requirements, Current, Performance, Application

PATTERN: Percolates on WHAT TO SAY
• Domain terminology choices
• Professional framing ("methodology")
• Technical precision ("Metrics" vs "Requirements")
• Expert communication style"""
    
    ax.text(0.54, 0.85, persona_high_entropy, ha='left', va='top', fontsize=11,
           transform=ax.transAxes, family='monospace',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))
    
    # Key insight box
    insight_box = FancyBboxPatch((0.1, 0.1), 0.8, 0.40,
                                boxstyle="round,pad=0.02",
                                facecolor='#FFFACD', edgecolor='black',
                                linewidth=3, transform=ax.transAxes)
    ax.add_patch(insight_box)
    
    insight_title = "🔑 KEY INSIGHT: Personas Don't Reduce Entropy - They Redirect It"
    ax.text(0.5, 0.47, insight_title, ha='center', fontsize=18, fontweight='bold',
           transform=ax.transAxes)
    
    insight_text = """WHAT WE LEARNED:

Volatility Similar: Both σ ≈ 0.59 (nearly identical entropy volatility)
High-Entropy Count Similar: Generic=17, Persona=19 (comparable uncertainty frequency)

BUT - They Percolate on DIFFERENT Things:

Generic AI:                                  Persona AI:
├─ Percolates on HOW to say things          ├─ Percolates on WHAT to say
├─ Uncertainty about sentence structure      ├─ Uncertainty about domain terms
├─ Generic word alternatives                 ├─ Technical precision choices
├─ Conversational style decisions            ├─ Professional framing decisions
└─ "How do I phrase this?"                   └─ "Which technical term is best?"

═══════════════════════════════════════════════════════════════════════════

FOR PERSONA DESIGNERS:

✓ Personas WORK - but not by making AI "more confident"
✓ They redirect deliberation from style → substance
✓ Good personas should cause percolation on:
  • Domain-specific terminology
  • Technical precision
  • Professional communication patterns
  • Expert decision frameworks

✗ Don't expect personas to reduce entropy volatility
✗ Uncertainty is natural and necessary for quality
✓ The LOCATION of uncertainty matters more than the AMOUNT"""
    
    ax.text(0.12, 0.44, insight_text, ha='left', va='top', fontsize=11,
           transform=ax.transAxes, family='monospace')
    
    plt.savefig('visualizations/percolation_summary.png',
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: visualizations/percolation_summary.png")
    plt.close()

def main():
    print("\n" + "="*70)
    print("Creating Percolation Summary")
    print("="*70)
    print("\nGenerating final visualization of what each approach")
    print("'percolates on' - revealing the true difference...\n")
    
    create_percolation_summary()
    
    print("\n" + "="*70)
    print("KEY TAKEAWAY")
    print("="*70)
    print("\nPersonas don't reduce entropy - they REDIRECT it!")
    print("\n  Generic AI → Percolates on HOW to say things")
    print("  Persona AI → Percolates on WHAT to say")
    print("\nThis is EXACTLY what you want in a good persona:")
    print("  • Less deliberation about generic phrasing")
    print("  • More deliberation about domain-specific choices")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
