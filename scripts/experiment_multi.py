"""
Multi-Scenario Persona Probability Experiment

Runs multiple test cases to demonstrate how personas reshape probability
distributions across different types of questions and contexts.
"""

import os
import json
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Tuple
from pathlib import Path

load_dotenv()

class MultiScenarioExperiment:
    """Runs comprehensive persona experiments across multiple scenarios."""
    
    def __init__(self, model_name: str = None, top_logprobs: int = 20):
        """Initialize the multi-scenario experiment."""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model_name = model_name or os.getenv('MODEL_NAME', 'gpt-4')
        self.top_logprobs = top_logprobs
        
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

    def get_test_scenarios(self) -> List[Dict[str, str]]:
        """Define test scenarios with different question types."""
        return [
            {
                "name": "System Design Question",
                "prompt": "How should I design the system?",
                "category": "architecture"
            },
            {
                "name": "Problem Solving",
                "prompt": "My application is slow. What should I do?",
                "category": "troubleshooting"
            },
            {
                "name": "Technology Selection",
                "prompt": "What database should I use for this project?",
                "category": "decision-making"
            },
            {
                "name": "Best Practices",
                "prompt": "How can I improve my infrastructure?",
                "category": "optimization"
            },
            {
                "name": "Security Question",
                "prompt": "How do I secure my application?",
                "category": "security"
            },
            {
                "name": "Cost Question",
                "prompt": "How can I reduce my cloud costs?",
                "category": "cost-optimization"
            }
        ]

    def get_token_probabilities(
        self, 
        prompt: str, 
        system_message: str = None,
        max_tokens: int = 1
    ) -> Dict:
        """Get token probabilities from the model."""
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
            temperature=1.0
        )
        
        return response

    def extract_first_token_data(self, response) -> Tuple[str, float, List[str], List[float]]:
        """Extract first token and top alternatives."""
        logprobs_data = response.choices[0].logprobs.content[0].top_logprobs
        
        selected_token = logprobs_data[0].token
        selected_prob = np.exp(logprobs_data[0].logprob)
        
        tokens = [lp.token for lp in logprobs_data[:5]]
        probs = [np.exp(lp.logprob) for lp in logprobs_data[:5]]
        
        return selected_token, selected_prob, tokens, probs

    def extract_multi_token_data(self, response) -> Tuple[str, List[str], List[float]]:
        """Extract multi-token sequence data."""
        tokens = []
        probs = []
        
        for content in response.choices[0].logprobs.content:
            tokens.append(content.token)
            probs.append(np.exp(content.logprob))
        
        full_text = response.choices[0].message.content
        return full_text, tokens, probs

    def run_scenario(self, scenario: Dict, max_tokens: int = 5) -> Dict:
        """Run a single scenario test."""
        print(f"\nTesting: {scenario['name']}")
        print(f"Prompt: {scenario['prompt']}")
        
        # Single token test
        print("  → First token analysis...")
        response_without_single = self.get_token_probabilities(scenario['prompt'])
        response_with_single = self.get_token_probabilities(
            scenario['prompt'], 
            system_message=self.get_azure_architect_persona()
        )
        
        token_without, prob_without, top_without, probs_without = \
            self.extract_first_token_data(response_without_single)
        token_with, prob_with, top_with, probs_with = \
            self.extract_first_token_data(response_with_single)
        
        # Multi-token test
        print("  → Multi-token sequence...")
        response_without_multi = self.get_token_probabilities(
            scenario['prompt'], max_tokens=max_tokens
        )
        response_with_multi = self.get_token_probabilities(
            scenario['prompt'], 
            system_message=self.get_azure_architect_persona(),
            max_tokens=max_tokens
        )
        
        text_without, tokens_without, probs_seq_without = \
            self.extract_multi_token_data(response_without_multi)
        text_with, tokens_with, probs_seq_with = \
            self.extract_multi_token_data(response_with_multi)
        
        # Calculate metrics
        avg_without = np.mean(probs_seq_without)
        avg_with = np.mean(probs_seq_with)
        confidence_change = ((avg_with - avg_without) / avg_without) * 100
        first_token_change = ((prob_with - prob_without) / prob_without) * 100
        
        results = {
            'scenario': scenario,
            'first_token': {
                'without': {
                    'selected': token_without,
                    'probability': prob_without,
                    'top_5_tokens': top_without,
                    'top_5_probs': probs_without
                },
                'with': {
                    'selected': token_with,
                    'probability': prob_with,
                    'top_5_tokens': top_with,
                    'top_5_probs': probs_with
                },
                'first_token_confidence_change': first_token_change
            },
            'sequence': {
                'without': {
                    'text': text_without,
                    'tokens': tokens_without,
                    'probabilities': probs_seq_without,
                    'avg_confidence': avg_without
                },
                'with': {
                    'text': text_with,
                    'tokens': tokens_with,
                    'probabilities': probs_seq_with,
                    'avg_confidence': avg_with
                },
                'avg_confidence_change': confidence_change
            }
        }
        
        print(f"  ✓ First token: '{token_without}' → '{token_with}'")
        print(f"  ✓ First token confidence: {prob_without:.1%} → {prob_with:.1%} ({first_token_change:+.1f}%)")
        print(f"  ✓ Avg confidence: {avg_without:.1%} → {avg_with:.1%} ({confidence_change:+.1f}%)")
        
        return results

    def run_all_scenarios(self, max_tokens: int = 5) -> List[Dict]:
        """Run all test scenarios."""
        scenarios = self.get_test_scenarios()
        results = []
        
        print("="*80)
        print("MULTI-SCENARIO PERSONA PROBABILITY EXPERIMENT")
        print("="*80)
        print(f"\nRunning {len(scenarios)} test scenarios...\n")
        
        for scenario in scenarios:
            try:
                result = self.run_scenario(scenario, max_tokens)
                results.append(result)
            except Exception as e:
                print(f"  ✗ Error: {e}")
                continue
        
        return results

    def print_summary(self, results: List[Dict]):
        """Print summary of all results."""
        print("\n" + "="*80)
        print("EXPERIMENT SUMMARY")
        print("="*80)
        
        print("\n📊 FIRST TOKEN ANALYSIS")
        print("-" * 80)
        print(f"{'Scenario':<30} {'Without':<20} {'With Persona':<20} {'Change':<10}")
        print("-" * 80)
        
        for result in results:
            name = result['scenario']['name']
            without = result['first_token']['without']['selected']
            with_p = result['first_token']['with']['selected']
            change = result['first_token']['first_token_confidence_change']
            
            print(f"{name:<30} '{without[:15]}'{'...' if len(without) > 15 else '':<5} "
                  f"'{with_p[:15]}'{'...' if len(with_p) > 15 else '':<5} "
                  f"{change:>+6.1f}%")
        
        print("\n📈 AVERAGE CONFIDENCE ACROSS SEQUENCE")
        print("-" * 80)
        print(f"{'Scenario':<30} {'Without':<12} {'With':<12} {'Change':<10}")
        print("-" * 80)
        
        for result in results:
            name = result['scenario']['name']
            without = result['sequence']['without']['avg_confidence']
            with_p = result['sequence']['with']['avg_confidence']
            change = result['sequence']['avg_confidence_change']
            
            print(f"{name:<30} {without:>10.1%}  {with_p:>10.1%}  {change:>+6.1f}%")
        
        # Overall statistics
        first_token_changes = [r['first_token']['first_token_confidence_change'] 
                               for r in results]
        avg_confidence_changes = [r['sequence']['avg_confidence_change'] 
                                  for r in results]
        
        print("\n🎯 OVERALL STATISTICS")
        print("-" * 80)
        print(f"First Token Confidence Change:")
        print(f"  Average: {np.mean(first_token_changes):+.1f}%")
        print(f"  Median:  {np.median(first_token_changes):+.1f}%")
        print(f"  Range:   {np.min(first_token_changes):+.1f}% to {np.max(first_token_changes):+.1f}%")
        
        print(f"\nSequence Average Confidence Change:")
        print(f"  Average: {np.mean(avg_confidence_changes):+.1f}%")
        print(f"  Median:  {np.median(avg_confidence_changes):+.1f}%")
        print(f"  Range:   {np.min(avg_confidence_changes):+.1f}% to {np.max(avg_confidence_changes):+.1f}%")
        
        # Key insight
        positive_first = sum(1 for x in first_token_changes if x > 0)
        negative_avg = sum(1 for x in avg_confidence_changes if x < 0)
        
        print(f"\n💡 KEY INSIGHT:")
        print(f"  {positive_first}/{len(results)} scenarios: First token confidence INCREASED")
        print(f"  {negative_avg}/{len(results)} scenarios: Average confidence DECREASED")
        print(f"\n  This pattern shows personas consistently reshape probabilities:")
        print(f"  → Higher confidence in initial approach (expert direction)")
        print(f"  → Lower average due to deliberation at decision points")

    def save_results(self, results: List[Dict], filename: str = 'results_multi_scenario.json'):
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
        
        with open(filename, 'w') as f:
            json.dump(results_serializable, f, indent=2)
        print(f"\n✓ Results saved to {filename}")

def main():
    """Run the multi-scenario experiment."""
    max_tokens = int(os.getenv('MAX_TOKENS', 5))
    
    experiment = MultiScenarioExperiment()
    results = experiment.run_all_scenarios(max_tokens)
    
    experiment.print_summary(results)
    experiment.save_results(results)
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. Review results_multi_scenario.json for detailed data")
    print("2. Run: python visualize_multi.py to create visualizations")
    print("3. Check visualizations/ directory for comparative charts")

if __name__ == "__main__":
    main()
