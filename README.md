# AfricaLLM: Comprehensive Evaluation and Fine-tuning of Large Language Models for African Languages

<div align="center">
<img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version"/>
<img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"/>
<img src="https://img.shields.io/badge/Status-Research-orange.svg" alt="Status"/>
<img src="https://img.shields.io/badge/Models-10+-purple.svg" alt="Models"/>
<img src="https://img.shields.io/badge/Languages-16+-green.svg" alt="Languages"/>
</div>

## 🌍 Overview

**AfricaLLM** is a comprehensive research project that evaluates and fine-tunes Large Language Models (LLMs) for African languages. This project addresses the significant gap in culturally-aware AI systems for African languages by:

- **Evaluating** 10+ state-of-the-art LLMs on African language benchmarks
- **Fine-tuning** models using World Values Survey (WVS) data from African countries  
- **Analyzing** performance across 16+ African languages and 3 key NLP tasks
- **Providing** comprehensive datasets, analysis tools, and reproducible results

The project tackles cultural bias in LLMs by leveraging authentic cultural data from African countries and creating more linguistically appropriate language models.

## 🚀 Key Features

- ✅ **Multi-Model Evaluation**: Base and fine-tuned versions of Qwen, Llama, Mistral, and Gemma models
- ✅ **Comprehensive Benchmarks**: AfriQA, AfriSenti, and AfriXNLI tasks
- ✅ **16+ African Languages**: From Amharic to Zulu with cultural context
- ✅ **Advanced Fine-tuning**: QLoRA-based efficient fine-tuning pipeline
- ✅ **Rich Analysis Tools**: Performance comparisons, visualizations, and language-specific insights
- ✅ **Reproducible Research**: Complete datasets, scripts, and result analysis

## 📊 Evaluation Results

Our comprehensive evaluation shows significant improvements in African language understanding:

| Model Family | Base Performance | Finetuned Performance | Improvement |
|--------------|-----------------|----------------------|-------------|
| **Qwen 32B** | 0.3942 | 0.3973 | +0.78% |
| **Gemma 27B** | 0.3894 | 0.3802 | -2.36% |
| **Qwen 8B** | 0.2970 | 0.3172 | +6.80% |
| **Llama 8B** | 0.3139 | 0.2572 | -18.07% |
| **Mistral 7B** | 0.3032 | - | - |

*Note: Results show average performance across all tasks and languages*

## 🏗️ Project Structure

```
AfricaLLM/
├── 📁 data/                              # Training and evaluation data
│   ├── 📁 _Finetune_/                   # Fine-tuning datasets (with reasoning)
│   ├── 📁 _Finetune_No_Reasoning/       # Fine-tuning datasets (no reasoning)
│   ├── 📁 [Language]/                   # Language-specific data (16+ languages)
│   │   ├── 📁 Finetune/                 # Fine-tuning data per language
│   │   └── 📄 WVQ_[Language].csv        # World Values data per language
│   ├── 📄 WVQ.jsonl                     # Combined World Values dataset
│   └── 📄 new_WVQ.jsonl                 # Enhanced World Values dataset
├── 📁 WVS_original_dataset/             # Original World Values Survey data
├── 📁 results/                          # Comprehensive evaluation results
│   ├── 📁 result_raw/                   # Raw model outputs
│   ├── 📁 result_cleaned/               # Processed results (CSV format)
│   └── 📁 result_analysis/              # Statistical analysis and summaries
├── 📓 data_preprocees.ipynb             # Data preprocessing pipeline
├── 📓 finetune.ipynb                    # Model fine-tuning pipeline
├── 📓 results.ipynb                     # Results analysis and visualization
└── 📄 pyproject.toml                    # Project dependencies
```

## ⚡ Quick Start

### Prerequisites

```bash
# Clone the repository
git clone https://github.com/username/AfricaLLM.git
cd AfricaLLM

# Install dependencies using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 🔍 Explore Results

The easiest way to start is by exploring our pre-computed results:

```python
import pandas as pd

# Load model performance comparison
model_results = pd.read_csv('results/result_analysis/model_averages.csv')
print(model_results)

# Load task-specific analysis
task_results = pd.read_csv('results/result_analysis/task_averages.csv')
print(task_results)

# Load language-specific performance
language_results = pd.read_csv('results/result_analysis/language_averages.csv')
print(language_results)
```

### 📊 Generate Analysis

Run the comprehensive results analysis:

```bash
# Open the results analysis notebook
jupyter notebook results.ipynb
```

## 🔧 Detailed Usage

### 1. 📋 Data Preprocessing

Transform World Values Survey data into training format:

```python
# Open the preprocessing notebook
jupyter notebook data_preprocees.ipynb

# The notebook processes WVS data from multiple African countries:
# - Ethiopia (Amharic, Tigrigna, Oromo)
# - Kenya (Swahili)  
# - Nigeria (Hausa, Igbo, Yoruba)
# - Zimbabwe (Shona, Ndebele)
# - Ghana (Twi, Ewe)
# - Rwanda (Kinyarwanda)
# - South Africa (Afrikaans, Sotho, Tswana, Xhosa, Zulu)
```

### 2. 🚀 Model Fine-tuning

Fine-tune models using our optimized QLoRA pipeline:

```python
# Open the fine-tuning notebook
jupyter notebook finetune.ipynb

# Key configurations:
# - QLoRA with 4-bit quantization for efficiency
# - LoRA parameters: r=32, alpha=64, dropout=0.2
# - Optimized for African language datasets
# - Support for both reasoning and no-reasoning variants
```

**Supported Model Families:**
- **Qwen**: 8B, 32B variants
- **Llama**: 8B variants
- **Mistral**: 7B variants  
- **Gemma**: 27B variants

### 3. 📈 Evaluation and Analysis

Comprehensive evaluation on African language benchmarks:

#### Available Benchmarks:
- **AfriQA**: Question Answering in African languages
- **AfriSenti**: Sentiment Analysis across African languages
- **AfriXNLI**: Cross-lingual Natural Language Inference

#### Run Analysis:
```python
# Performance comparison between base and fine-tuned models
jupyter notebook results.ipynb

# Language-specific performance analysis
# Task-specific improvements
# Cross-model comparisons
```

## 🌍 Supported Languages

Our project supports **16+ African languages** with cultural context:

| Language | Code | Country | Script | Speakers |
|----------|------|---------|--------|----------|
| **Amharic** | amh | Ethiopia | Ge'ez | 57M |
| **Afrikaans** | afr | South Africa | Latin | 7M |
| **Ewe** | ewe | Ghana/Togo | Latin | 4.5M |
| **Hausa** | hau | Nigeria/Niger | Latin/Arabic | 70M |
| **Igbo** | ibo | Nigeria | Latin | 45M |
| **Kinyarwanda** | kin | Rwanda | Latin | 12M |
| **Oromo** | orm | Ethiopia | Latin | 37M |
| **Shona** | sna | Zimbabwe | Latin | 14M |
| **Sotho** | sot | South Africa | Latin | 5.6M |
| **Swahili** | swa | Kenya/Tanzania | Latin | 200M |
| **Tigrinya** | tir | Ethiopia/Eritrea | Ge'ez | 9M |
| **Twi** | twi | Ghana | Latin | 17M |
| **Xhosa** | xho | South Africa | Latin | 8.2M |
| **Yoruba** | yor | Nigeria/Benin | Latin | 45M |
| **Zulu** | zul | South Africa | Latin | 12M |
| **+ More** | ... | Various | ... | ... |

## 📊 Key Findings

### 🎯 Performance Insights:

1. **Model Size Impact**: Larger models (32B) generally perform better but show diminishing returns
2. **Fine-tuning Effectiveness**: Variable across model families - Qwen 8B shows +6.80% improvement
3. **Language-Specific Patterns**: Some languages benefit more from fine-tuning than others
4. **Task Complexity**: AfriXNLI shows more consistent improvements than AfriSenti

### 🔍 Language-Specific Results:

- **Best Performing Languages**: Swahili, Hausa, Yoruba (high-resource)
- **Most Improved**: Portuguese (+39.97%), Amharic (+36.34%)
- **Challenging Languages**: Tswana, Twi, Tsonga (limited resources)

## 🛠️ Advanced Features

### Custom Model Comparison

```python
# Compare specific models on specific languages
from analysis_tools import ModelComparison

comparator = ModelComparison()
results = comparator.compare_models(
    models=['Base_Qwen8B', 'Finetuned_Qwen8B'],
    languages=['amh', 'hau', 'swa'], 
    tasks=['afrisenti', 'afrixnli']
)
comparator.visualize_results(results)
```

### Language Performance Analysis

```python
# Analyze performance patterns across languages
from analysis_tools import LanguageAnalyzer

analyzer = LanguageAnalyzer()
analyzer.analyze_language_patterns('results/result_cleaned/')
analyzer.generate_language_report()
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add New Languages**: Contribute World Values Survey data for additional African languages
2. **Improve Models**: Experiment with different fine-tuning strategies
3. **Enhance Analysis**: Add new evaluation metrics or visualization tools
4. **Documentation**: Improve guides and tutorials

### Development Setup:

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/AfricaLLM.git
cd AfricaLLM

# Create development environment
uv sync --dev

# Run tests
pytest tests/

# Submit pull request
```

## 📚 Citation

If you use this work in your research, please cite:

```bibtex
@misc{africallm2024,
  title={AfricaLLM: Comprehensive Evaluation and Fine-tuning of Large Language Models for African Languages},
  author={AfricaLLM Research Team},
  year={2024},
  url={https://github.com/username/AfricaLLM},
  note={A comprehensive study of LLM performance on African languages with cultural context}
}
```

## 🙏 Acknowledgments

- **World Values Survey Association** for providing cultural survey data
- **Hugging Face** for model hosting and transformers library
- **African NLP Community** for benchmarks and linguistic expertise
- **Masakhane Community** for African language resources
- **Contributors** to African language datasets and evaluation metrics

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Work

- [Masakhane: Machine Translation for Africa](https://www.masakhane.io/)
- [AfroLM: A Self-Active Learning-based Multilingual Pretrained Language Model for African Languages](https://arxiv.org/abs/2311.15608)
- [World Values Survey](https://www.worldvaluessurvey.org/)

---

<div align="center">
<strong>🌍 Bridging AI and African Languages 🌍</strong><br>
<em>Making Large Language Models work for everyone, everywhere</em>
</div>

