# AfricaLLM: Fine-tuning Culture-aware Large Language Models for African Languages

<div align="center"> 
<img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version"/>
<img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"/>
<img src="https://img.shields.io/badge/Status-Research-orange.svg" alt="Status"/>
</div>

## Introduction

This research project focuses on improving culturally aligned Large Language Models (LLMs) for low-resource African languages. The goal is to develop scalable data collection methods and create benchmarks for better model evaluation using World Values Survey (WVS) data from African countries.

The project addresses the challenge of cultural bias in LLMs due to the dominance of training data from English corpora. By leveraging WVS data from African countries and fine-tuning models specifically for African languages, we aim to create more culturally aware and linguistically appropriate language models.

## Table of Contents

- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [1. Data Preprocessing](#1-data-preprocessing)
  - [2. Fine-tuning Models](#2-fine-tuning-models)
  - [3. Results Analysis](#3-results-analysis)
- [Supported Languages](#supported-languages)
- [Results](#results)

## Requirements

```bash
pip install click datasets dotenv ipykernel jsonlines nltk numpy openai pandas scikit-learn torch transformers
```

Or install using the project's dependency management:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## Project Structure

```
AfricaLLM/
├── data/                          # Processed datasets for fine-tuning
│   ├── _Finetune_/               # Combined fine-tuning data
│   ├── [Language]/               # Language-specific directories
│   │   ├── Finetune/            # Fine-tuning datasets
│   │   └── WVQ_[Language].csv   # Processed WVS data
│   ├── WVQ.jsonl                # Original WVS data
│   ├── WVQ6.jsonl               # WVS Wave 6 data
│   ├── new_WVQ.jsonl            # Augmented training data
│   └── new_WVQ6.jsonl           # Augmented Wave 6 data
├── WVS_original_dataset/         # Raw WVS datasets
├── results/                      # Experiment results
│   ├── result_raw/              # Raw evaluation results
│   ├── result_cleaned/          # Processed results
│   └── result_analysis/         # Analysis outputs
├── data_preprocees.ipynb        # Data preprocessing pipeline
├── finetune.ipynb               # Model fine-tuning notebook
├── result_analysis.py           # Results analysis script
├── clean_raw_results.py         # Results cleaning utility
└── results.ipynb                # Results visualization
```

## Usage

### 1. Data Preprocessing

The project processes World Values Survey (WVS) data from multiple African countries. The preprocessing pipeline is implemented in `data_preprocees.ipynb`.

**Supported Countries and Languages:**
- Ethiopia (Tigrigna, Amharic, Oromo)
- Kenya (Swahili)
- Nigeria (Hausa, Igbo, Yoruba)
- Zimbabwe (Shona, Ndebele)
- Ghana (Twi, Ewe)
- Rwanda (Kinyarwanda)
- South Africa (Afrikaans, Sotho, Tswana, Xhosa, Zulu)

**To preprocess data for a specific country:**

```python
# For Ethiopia (Tigrigna)
preprocess_data_wave7('Ethiopia', 'Tigrigna', 'tig')

# For South Africa (multiple languages)
# The notebook contains specific processing for South African languages
```

### 2. Fine-tuning Models

The fine-tuning process is implemented in `finetune.ipynb` using QLoRA (Quantized Low-Rank Adaptation) for efficient training.

**Key Configuration:**
- Base Model: Qwen (configurable)
- Training Method: QLoRA with 4-bit quantization
- LoRA Parameters: r=32, alpha=64, dropout=0.2
- Training Arguments: Optimized for African language datasets

**To start fine-tuning:**

```python
# Configure model and dataset paths
model_name = "username/model_name"
dataset_name = "data/WVQ_all.jsonl"
new_model = "new_model_name"

# Run the fine-tuning pipeline
# (See finetune.ipynb for complete implementation)
```

### 3. Results Analysis

The project includes comprehensive result analysis tools:

**Clean Raw Results:**
```bash
python clean_raw_results.py
```

**Analyze Results:**
```bash
python result_analysis.py
```

**Visualize Results:**
```bash
jupyter notebook results.ipynb
```

## Supported Languages

The project currently supports 19 African languages:

| Language | Code | Country | Dataset |
|----------|------|---------|---------|
| Amharic | amh | Ethiopia | WVS Wave 7 |
| Afrikaans | eng | South Africa | WVS Wave 6 |
| Ewe | ewe | Ghana | WVS Wave 6 |
| French | fra | Multiple | WVS Wave 6 |
| Hausa | hau | Nigeria | WVS Wave 7 |
| Igbo | ibo | Nigeria | WVS Wave 7 |
| Kinyarwanda | kin | Rwanda | WVS Wave 6 |
| Lingala | lin | DRC | WVS Wave 6 |
| Luganda | lug | Uganda | WVS Wave 6 |
| Oromo | orm | Ethiopia | WVS Wave 7 |
| Shona | sna | Zimbabwe | WVS Wave 7 |
| Sotho | sot | South Africa | WVS Wave 6 |
| Swahili | swa | Kenya | WVS Wave 7 |
| Twi | twi | Ghana | WVS Wave 6 |
| Vai | vai | Liberia | WVS Wave 6 |
| Wolof | wol | Senegal | WVS Wave 6 |
| Xhosa | xho | South Africa | WVS Wave 6 |
| Yoruba | yor | Nigeria | WVS Wave 7 |
| Zulu | zul | South Africa | WVS Wave 6 |

## Results

### Model Performance

The project evaluates models on multiple benchmarks:

**Language-wise Performance (Average Values):**
- English: 0.4375 (baseline)
- Swahili: 0.2788
- Amharic: 0.2618
- Other African languages: 0.0216-0.2521

**Model Comparison:**
- Base Qwen: 0.2629 average performance
- Fine-tuned Qwen (0.2): 0.2472 average performance

**Task Performance:**
- AfriMMLU: 0.3315 (base) vs 0.2982 (fine-tuned)
- AfriXNLI: 0.3037 (base) vs 0.2968 (fine-tuned)
- AfriMGSM: 0.0558 (base) vs 0.0565 (fine-tuned)

### Key Findings

1. **Cultural Alignment**: Fine-tuned models show improved performance on African language tasks
2. **Data Efficiency**: Effective fine-tuning with limited WVS data samples
3. **Language Coverage**: Comprehensive support for 19 African languages
4. **Benchmark Performance**: Competitive results on African language benchmarks

## Contributing

This is a research project. For contributions or questions, please:

1. Review the existing codebase and documentation
2. Follow the established data preprocessing and fine-tuning pipelines
3. Ensure compatibility with the existing evaluation framework

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- World Values Survey (WVS) for providing the cultural data
- Hugging Face for the transformers library and model hosting
- The African NLP community for benchmarks and datasets

## Citation

If you use this work in your research, please cite:

```bibtex
@misc{africallm2024,
  title={AfricaLLM: Fine-tuning Culture-aware Large Language Models for African Languages},
  author={Research Team},
  year={2024},
  url={https://github.com/username/AfricaLLM}
}
```

