# CausalNLP Toolbox

Developed by [Zhijing Jin](https://zhijing-jin.com/) (MPI & ETH) and [Zhiheng Lyu](https://cn.linkedin.com/in/zhiheng-lyu-b022861ba) (HKU).

## Causal Effect Estimation

### Method 1: Matching

**Function We Provide:** Matching two datasets to obtain semantically similar pairs of data (by SentenceBERT embedding)

- Code: [`causalnlp/causal_effect_estimation/get_similar_text_pairs.py`](causalnlp/causal_effect_estimation/get_similar_text_pairs.py)
- How to Run:

### Method 2: Do-Calculus

- Step 1. Get the estimand
- Step 2. Statistical estimation of the estimand

**Function We Provide:** For each data sample, given text embedding `text_emb` and a set of features `feats`, we want to learn `P(effect | text_emb, feats)` by a neural network model.

- Code: [`causalnlp/statistical_estimator/predict_by_neural_networks.py`](causalnlp/statistical_estimator/predict_by_neural_networks.py)
- How to Run: