"""
Enhanced Persona Probability Experiment - Full Top-5 Distributions

Captures top-5 token distributions for EVERY token in the sequence,
not just the first token. This allows us to visualize how probability
mass is distributed at each decision point.
"""

import os
import json
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Tuple
from pathlib import Path

load_dotenv()

class FullDistributionExperiment:
    """Captures complete probability distributions for all tokens."""
    
    def __init__(self, model_name: str = None, top_logprobs: int = 5):
        """Initialize the experiment."""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model_name = model_name or os.getenv('MODEL_NAME', 'gpt-4')
        self.top_logprobs = top_logprobs  # We want top-5 for visualization
        
    def get_azure_architect_persona(self) -> str:
        """Returns Azure Architect persona."""
        return """You are an Azure Architect specializing in cloud architecture design.

Core Competencies:
- Azure Well-Architected Framework principles
- Multi-region deployment strategies
- Microservices and distributed systems
- Infrastructure as Code (Bicep, Terraform)
- Cost optimization and resource management

Workflow Methodology:
Phase 1: Discovery - Analyze requirements, search documentation, understand constraints
Phase 2: Planning - Design architecture, choose Azure services, validate against WAF
Phase 3: Execution - Implement infrastructure, configure resources, deploy solutions

Communication Style:
- Begin with structured methodology (Discovery → Planning → Execution)
- Reference Azure documentation and best practices
- Apply Well-Architected Framework principles
- Provide specific, actionable recommendations with rationale
- Use precise Azure terminology and service names"""

    def get_token_sequence_with_distributions(
        self, 
        prompt: str, 
        system_message: str = None,
        max_tokens: int = 10
    ) -> Dict:
        """Get token sequence with full top-5 distributions at each position."""
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            logprobs=True,
            top_logprobs=self.top_logprobs,  # Get top-5 for each token
            max_tokens=max_tokens,
            temperature=1.0
        )
        
        return response

    def extract_full_distribution_data(self, response) -> Dict:
        """Extract complete distribution data for all tokens."""
        full_text = response.choices[0].message.content
        tokens_data = []
        
        for content in response.choices[0].logprobs.content:
            # Get selected token
            selected_token = content.token
            selected_logprob = content.logprob
            selected_prob = np.exp(selected_logprob)
            
            # Get top-5 alternatives
            top_tokens = []
            top_probs = []
            for lp in content.top_logprobs:
                top_tokens.append(lp.token)
                top_probs.append(np.exp(lp.logprob))
            
            token_data = {
                'selected_token': selected_token,
                'selected_prob': selected_prob,
                'top_5_tokens': top_tokens,
                'top_5_probs': top_probs
            }
            tokens_data.append(token_data)
        
        return {
            'full_text': full_text,
            'tokens': tokens_data
        }

    def run_comparison(self, prompt: str, max_tokens: int = 10) -> Dict:
        """Run comparison with and without persona."""
        print(f"\nPrompt: '{prompt}'")
        print(f"Capturing {max_tokens} tokens with full top-5 distributions...")
        
        # Without persona
        print("  → Without persona...")
        response_without = self.get_token_sequence_with_distributions(prompt, max_tokens=max_tokens)
        data_without = self.extract_full_distribution_data(response_without)
        
        # With persona
        print("  → With persona...")
        response_with = self.get_token_sequence_with_distributions(
            prompt, 
            system_message=self.get_azure_architect_persona(),
            max_tokens=max_tokens
        )
        data_with = self.extract_full_distribution_data(response_with)
        
        # Calculate statistics
        avg_prob_without = np.mean([t['selected_prob'] for t in data_without['tokens']])
        avg_prob_with = np.mean([t['selected_prob'] for t in data_with['tokens']])
        
        # Calculate entropy for each position
        def calculate_entropy(probs):
            return -sum(p * np.log2(p) if p > 0 else 0 for p in probs)
        
        entropy_without = [calculate_entropy(t['top_5_probs']) for t in data_without['tokens']]
        entropy_with = [calculate_entropy(t['top_5_probs']) for t in data_with['tokens']]
        
        print(f"  ✓ Without: '{data_without['full_text']}'")
        print(f"     Avg prob: {avg_prob_without:.1%}, Avg entropy: {np.mean(entropy_without):.2f}")
        print(f"  ✓ With:    '{data_with['full_text']}'")
        print(f"     Avg prob: {avg_prob_with:.1%}, Avg entropy: {np.mean(entropy_with):.2f}")
        
        return {
            'prompt': prompt,
            'without_persona': data_without,
            'with_persona': data_with,
            'statistics': {
                'avg_prob_without': avg_prob_without,
                'avg_prob_with': avg_prob_with,
                'avg_entropy_without': float(np.mean(entropy_without)),
                'avg_entropy_with': float(np.mean(entropy_with)),
                'entropy_per_token_without': entropy_without,
                'entropy_per_token_with': entropy_with
            }
        }

    def save_results(self, results: Dict, filename: str = 'results/results_full_distributions.json'):
        """Save results to JSON file."""
        def convert_types(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, dict):
                return {k: convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            return obj
        
        results_serializable = convert_types(results)
        
        # Ensure results directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(results_serializable, f, indent=2)
        print(f"\n✓ Results saved to {filename}")

def main():
    """Run the full distribution experiment."""
    max_tokens = int(os.getenv('MAX_TOKENS', 50))
    
    # Test with the Problem Solving scenario (most dramatic difference)
    prompt = "My application is slow. What should I do?"
    
    print("="*80)
    print("FULL DISTRIBUTION PROBABILITY EXPERIMENT")
    print("="*80)
    print("\nThis experiment captures the TOP-5 token probability distribution")
    print("at EVERY position in the sequence, not just the first token.")
    print("\nThis allows us to see how probability mass is distributed across")
    print("all possible choices at each decision point.")
    print("="*80)
    
    experiment = FullDistributionExperiment()
    results = experiment.run_comparison(prompt, max_tokens)
    
    experiment.save_results(results)
    
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    print(f"\nWithout Persona:")
    print(f"  Text: '{results['without_persona']['full_text']}'")
    print(f"  Avg Selected Prob: {results['statistics']['avg_prob_without']:.1%}")
    print(f"  Avg Entropy: {results['statistics']['avg_entropy_without']:.2f} bits")
    
    print(f"\nWith Persona:")
    print(f"  Text: '{results['with_persona']['full_text']}'")
    print(f"  Avg Selected Prob: {results['statistics']['avg_prob_with']:.1%}")
    print(f"  Avg Entropy: {results['statistics']['avg_entropy_with']:.2f} bits")
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. Review results/results_full_distributions.json for complete data")
    print("2. Each token has its own top-5 distribution showing probability spread")
    print("3. Create visualizations showing the full probability landscape")

if __name__ == "__main__":
    main()
