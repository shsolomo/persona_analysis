"""
Token Probability Distribution Analysis Experiment

This script demonstrates how personas reshape token probability distributions
in large language models by comparing outputs with and without persona context.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Tuple, Dict

# Load environment variables
load_dotenv()

class PersonaProbabilityExperiment:
    """Analyzes token probability distributions with and without personas."""
    
    def __init__(self, model_name: str = None, top_logprobs: int = 20):
        """
        Initialize the experiment.
        
        Args:
            model_name: OpenAI model to use (defaults to env variable)
            top_logprobs: Number of top token probabilities to retrieve
        """
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model_name = model_name or os.getenv('MODEL_NAME', 'gpt-4')
        self.top_logprobs = top_logprobs
        
    def get_azure_architect_persona(self) -> str:
        """Returns a simplified Azure Architect persona."""
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

    def get_token_probabilities(
        self, 
        prompt: str, 
        system_message: str = None,
        max_tokens: int = 1
    ) -> Dict:
        """
        Get token probabilities from the model.
        
        Args:
            prompt: User prompt
            system_message: Optional system message (persona)
            max_tokens: Number of tokens to generate
            
        Returns:
            Dictionary with response and logprobs data
        """
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            logprobs=True,
            top_logprobs=self.top_logprobs,
            max_tokens=max_tokens,
            temperature=1.0  # Use default sampling for realistic probabilities
        )
        
        return response

    def extract_probabilities(self, response) -> Tuple[List[str], List[float]]:
        """
        Extract tokens and probabilities from response.
        
        Args:
            response: OpenAI API response with logprobs
            
        Returns:
            Tuple of (tokens, probabilities)
        """
        logprobs_data = response.choices[0].logprobs.content[0].top_logprobs
        tokens = [lp.token for lp in logprobs_data]
        probs = [np.exp(lp.logprob) for lp in logprobs_data]
        return tokens, probs

    def calculate_entropy(self, probs: List[float]) -> float:
        """
        Calculate Shannon entropy of probability distribution.
        
        Args:
            probs: List of probabilities
            
        Returns:
            Entropy in bits
        """
        # Filter out zero probabilities
        probs = [p for p in probs if p > 0]
        return -sum(p * np.log2(p) for p in probs)

    def run_single_token_experiment(self, prompt: str) -> Dict:
        """
        Run experiment comparing first token probabilities.
        
        Args:
            prompt: Test prompt
            
        Returns:
            Dictionary with results
        """
        print(f"Running single token experiment...")
        print(f"Prompt: {prompt}\n")
        
        # Without persona
        print("Querying without persona...")
        response_without = self.get_token_probabilities(prompt)
        tokens_without, probs_without = self.extract_probabilities(response_without)
        
        # With persona
        print("Querying with persona...")
        persona = self.get_azure_architect_persona()
        response_with = self.get_token_probabilities(prompt, system_message=persona)
        tokens_with, probs_with = self.extract_probabilities(response_with)
        
        # Calculate metrics
        entropy_without = self.calculate_entropy(probs_without)
        entropy_with = self.calculate_entropy(probs_with)
        
        top5_mass_without = sum(sorted(probs_without, reverse=True)[:5])
        top5_mass_with = sum(sorted(probs_with, reverse=True)[:5])
        
        results = {
            'without_persona': {
                'tokens': tokens_without,
                'probabilities': probs_without,
                'entropy': entropy_without,
                'top5_mass': top5_mass_without,
                'max_prob': max(probs_without),
                'selected_token': response_without.choices[0].message.content
            },
            'with_persona': {
                'tokens': tokens_with,
                'probabilities': probs_with,
                'entropy': entropy_with,
                'top5_mass': top5_mass_with,
                'max_prob': max(probs_with),
                'selected_token': response_with.choices[0].message.content
            }
        }
        
        return results

    def run_multi_token_experiment(self, prompt: str, max_tokens: int = 5) -> Dict:
        """
        Run experiment analyzing multiple token sequence.
        
        Args:
            prompt: Test prompt
            max_tokens: Number of tokens to generate
            
        Returns:
            Dictionary with sequential token data
        """
        print(f"\nRunning multi-token experiment ({max_tokens} tokens)...")
        
        # Without persona
        print("Generating sequence without persona...")
        response_without = self.get_token_probabilities(prompt, max_tokens=max_tokens)
        
        # With persona
        print("Generating sequence with persona...")
        persona = self.get_azure_architect_persona()
        response_with = self.get_token_probabilities(
            prompt, 
            system_message=persona, 
            max_tokens=max_tokens
        )
        
        # Extract token-by-token data
        def extract_sequence_data(response):
            tokens = []
            probs = []
            second_tokens = []
            second_probs = []
            
            for content in response.choices[0].logprobs.content:
                tokens.append(content.token)
                probs.append(np.exp(content.logprob))
                
                if len(content.top_logprobs) > 1:
                    second_tokens.append(content.top_logprobs[1].token)
                    second_probs.append(np.exp(content.top_logprobs[1].logprob))
                else:
                    second_tokens.append("N/A")
                    second_probs.append(0.0)
                    
            return tokens, probs, second_tokens, second_probs
        
        tokens_without, probs_without, second_without, second_probs_without = \
            extract_sequence_data(response_without)
        tokens_with, probs_with, second_with, second_probs_with = \
            extract_sequence_data(response_with)
        
        results = {
            'without_persona': {
                'tokens': tokens_without,
                'probabilities': probs_without,
                'second_choice_tokens': second_without,
                'second_choice_probs': second_probs_without,
                'full_text': response_without.choices[0].message.content
            },
            'with_persona': {
                'tokens': tokens_with,
                'probabilities': probs_with,
                'second_choice_tokens': second_with,
                'second_choice_probs': second_probs_with,
                'full_text': response_with.choices[0].message.content
            }
        }
        
        return results

    def print_results(self, results: Dict, experiment_type: str = 'single'):
        """Print formatted experiment results."""
        print("\n" + "="*80)
        print(f"EXPERIMENT RESULTS: {experiment_type.upper()}")
        print("="*80)
        
        if experiment_type == 'single':
            self._print_single_token_results(results)
        else:
            self._print_multi_token_results(results)

    def _print_single_token_results(self, results: Dict):
        """Print single token experiment results."""
        without = results['without_persona']
        with_p = results['with_persona']
        
        print("\nWITHOUT PERSONA - Top 10 Token Probabilities:")
        print("-" * 60)
        for i, (token, prob) in enumerate(zip(without['tokens'][:10], 
                                               without['probabilities'][:10]), 1):
            print(f"  {i:2d}. '{token:15s}' → {prob:.6f} ({prob*100:6.2f}%)")
        
        print(f"\n  Selected token: '{without['selected_token']}'")
        print(f"  Entropy: {without['entropy']:.3f} bits")
        print(f"  Max probability: {without['max_prob']:.6f} ({without['max_prob']*100:.2f}%)")
        print(f"  Top-5 probability mass: {without['top5_mass']:.6f} ({without['top5_mass']*100:.2f}%)")
        
        print("\n" + "="*80)
        print("\nWITH PERSONA - Top 10 Token Probabilities:")
        print("-" * 60)
        for i, (token, prob) in enumerate(zip(with_p['tokens'][:10], 
                                               with_p['probabilities'][:10]), 1):
            print(f"  {i:2d}. '{token:15s}' → {prob:.6f} ({prob*100:6.2f}%)")
        
        print(f"\n  Selected token: '{with_p['selected_token']}'")
        print(f"  Entropy: {with_p['entropy']:.3f} bits")
        print(f"  Max probability: {with_p['max_prob']:.6f} ({with_p['max_prob']*100:.2f}%)")
        print(f"  Top-5 probability mass: {with_p['top5_mass']:.6f} ({with_p['top5_mass']*100:.2f}%)")
        
        # Print comparison
        print("\n" + "="*80)
        print("COMPARISON:")
        print("-" * 60)
        entropy_reduction = ((without['entropy'] - with_p['entropy']) / without['entropy']) * 100
        max_prob_increase = ((with_p['max_prob'] - without['max_prob']) / without['max_prob']) * 100
        
        print(f"  Entropy reduction: {entropy_reduction:.1f}%")
        print(f"  Max probability increase: {max_prob_increase:.1f}%")
        print(f"  Top-5 mass increase: {(with_p['top5_mass'] - without['top5_mass'])*100:.1f} percentage points")

    def _print_multi_token_results(self, results: Dict):
        """Print multi-token experiment results."""
        without = results['without_persona']
        with_p = results['with_persona']
        
        print("\nTOKEN-BY-TOKEN GENERATION:")
        print("="*80)
        
        print("\nWITHOUT PERSONA:")
        print("-" * 60)
        print(f"Full text: '{without['full_text']}'")
        print("\nToken sequence:")
        for i, (token, prob, second, second_prob) in enumerate(
            zip(without['tokens'], without['probabilities'], 
                without['second_choice_tokens'], without['second_choice_probs']), 1):
            print(f"  Token {i}: '{token}' (p={prob:.3f})")
            print(f"           2nd choice: '{second}' (p={second_prob:.3f})")
        
        print("\n" + "="*80)
        print("\nWITH PERSONA:")
        print("-" * 60)
        print(f"Full text: '{with_p['full_text']}'")
        print("\nToken sequence:")
        for i, (token, prob, second, second_prob) in enumerate(
            zip(with_p['tokens'], with_p['probabilities'],
                with_p['second_choice_tokens'], with_p['second_choice_probs']), 1):
            print(f"  Token {i}: '{token}' (p={prob:.3f})")
            print(f"           2nd choice: '{second}' (p={second_prob:.3f})")
        
        # Average confidence comparison
        avg_confidence_without = np.mean(without['probabilities'])
        avg_confidence_with = np.mean(with_p['probabilities'])
        
        print("\n" + "="*80)
        print("COMPARISON:")
        print("-" * 60)
        print(f"  Average token confidence without persona: {avg_confidence_without:.3f}")
        print(f"  Average token confidence with persona: {avg_confidence_with:.3f}")
        print(f"  Confidence increase: {((avg_confidence_with - avg_confidence_without) / avg_confidence_without * 100):.1f}%")

    def save_results(self, results: Dict, filename: str = 'results.json'):
        """Save results to JSON file."""
        # Convert numpy types to native Python types for JSON serialization
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
        
        with open(filename, 'w') as f:
            json.dump(results_serializable, f, indent=2)
        print(f"\n✓ Results saved to {filename}")


def main():
    """Run the complete experiment."""
    print("="*80)
    print("PERSONA PROBABILITY DISTRIBUTION EXPERIMENT")
    print("="*80)
    print("\nThis experiment demonstrates how personas reshape token probability")
    print("distributions in large language models.\n")
    
    # Initialize experiment
    experiment = PersonaProbabilityExperiment()
    
    # Test prompt
    prompt = "How should I design the system?"
    
    # Run single token experiment
    results_single = experiment.run_single_token_experiment(prompt)
    experiment.print_results(results_single, 'single')
    experiment.save_results(results_single, 'results_single_token.json')
    
    # Run multi-token experiment
    max_tokens = int(os.getenv('MAX_TOKENS', 5))
    results_multi = experiment.run_multi_token_experiment(prompt, max_tokens)
    experiment.print_results(results_multi, 'multi')
    experiment.save_results(results_multi, 'results_multi_token.json')
    
    print("\n" + "="*80)
    print("EXPERIMENT COMPLETE")
    print("="*80)
    print("\nNext steps:")
    print("  1. Run: python visualize.py to create visualizations")
    print("  2. Check results_single_token.json and results_multi_token.json")
    print("  3. View generated plots in the output directory")


if __name__ == "__main__":
    main()
