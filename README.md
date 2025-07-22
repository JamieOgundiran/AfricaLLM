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


Install using the project's dependency management:

```bash
# Using uv (recommended)
uv sync

```

## Project Structure

```
AfricaLLM/
├── data/                          
│   ├── _Finetune_/               
│   ├── [Language]/               
│   │   ├── Finetune/            
│   │   └── WVQ_[Language].csv   
│   ├── WVQ.jsonl                
│   ├── WVQ6.jsonl               
│   ├── new_WVQ.jsonl            
│   └── new_WVQ6.jsonl           
├── WVS_original_dataset/        
├── results/                     
│   ├── result_raw/              
│   ├── result_cleaned/          
│   └── result_analysis/         
├── data_preprocees.ipynb        
├── finetune.ipynb               
├── result_analysis.py           
├── clean_raw_results.py         
└── results.ipynb                
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

