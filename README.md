# Persona Probability Experiment

**How do AI personas actually work?** This research provides empirical evidence through probability distribution analysis, revealing that personas don't just change *what* an AI says—they fundamentally reshape *how* it thinks.

## 🎯 Key Finding

Personas **redirect uncertainty**, not reduce it. Both generic and persona-conditioned AI have similar entropy volatility (~0.59), but uncertainty occurs at different words:

| Generic AI | Persona AI |
|------------|------------|
| Deliberates on **HOW** to phrase things | Deliberates on **WHAT** domain terms to use |
| "If" vs "When" vs "Improve" (sentence structure) | "methodology" vs "approach" (domain vocabulary) |
| 46% confidence on first token | 99% confidence on first token |

## 📊 What This Proves

Using OpenAI's `logprobs` parameter, we captured probability distributions for every token generated, revealing three key insights:

1. **Directive Starts** — Personas create sharp first-token predictions (99% vs 46%)
2. **Redirected Thinking** — Same uncertainty frequency, different focus (style → domain)
3. **Expert Language** — Probability mass concentrates on domain-specific vocabulary

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- [UV package manager](https://github.com/astral-sh/uv)
- OpenAI API key

### Setup & Run

```bash
# Clone and enter directory
cd persona-probability-experiment

# Install dependencies
uv sync

# Configure API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the experiment
uv run scripts/experiment_full_distributions.py
```

## 📁 Project Structure

```
persona-probability-experiment/
├── README.md                 # You are here
├── FINDINGS.md               # Detailed research findings
├── BLOG_POST.md              # Narrative format of findings
├── LICENSE                   # MIT License
│
├── docs/
│   ├── ANALYSIS.md           # Technical deep-dive
│   └── EXPLAIN_LIKE_IM_5.md  # Simple explanation
│
├── scripts/
│   └── experiment_full_distributions.py  # Main experiment
│
├── results/
│   └── results_full_distributions.json   # Experiment data
│
└── visualizations/           # Generated charts
```

## 📖 Documentation

| Document | Audience | Description |
|----------|----------|-------------|
| [FINDINGS.md](FINDINGS.md) | Everyone | Key insights and takeaways |
| [BLOG_POST.md](BLOG_POST.md) | General | Narrative discovery journey |
| [docs/ANALYSIS.md](docs/ANALYSIS.md) | Technical | Deep-dive into methodology |
| [docs/EXPLAIN_LIKE_IM_5.md](docs/EXPLAIN_LIKE_IM_5.md) | Anyone | Simple analogies |

## 🔬 Methodology

- **Model**: GPT-4 via OpenAI API
- **Analysis**: 50 tokens with `top_logprobs=5`
- **Prompt**: "My application is slow. What should I do?"
- **Comparison**: Generic AI vs Azure SaaS Architect persona
- **Metrics**: Entropy (H = -Σ p(x) × log₂(p(x))), probability distributions

## 📈 Sample Results

**First Token Probability:**
```
Generic:  "If" (46%) | "When" (36%) | "Improve" (8%)
Persona:  "To" (99%) | "Let's" (0.3%) | "Phase" (0.1%)
```

**Key Metrics:**
| Metric | Generic | Persona |
|--------|---------|---------|
| First-Token Confidence | 46% | 99% |
| Average Probability | 0.756 | 0.781 |
| Entropy Volatility (σ) | 0.585 | 0.604 |

## 🛠️ Extend This Research

Want to test your own personas? Modify `scripts/experiment_full_distributions.py`:

```python
def get_custom_persona(self) -> str:
    return """You are a [Your Role].
    
Core Competencies:
- [Competency 1]
- [Competency 2]

Communication Style:
- [Style guidelines]"""
```

## 📚 References

- [OpenAI API - Logprobs](https://platform.openai.com/docs/api-reference/chat/create#chat-create-logprobs)
- [Shannon Entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory))

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

## 👤 Author

Shane Solomon ([@shsolomo](https://github.com/shsolomo))

---

*Built with Python, OpenAI API, NumPy, and Matplotlib*
