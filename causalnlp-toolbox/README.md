# CausalNLP Toolbox

Developed by Zhijing Jin (MPI & ETH) and Zhiheng Lyu (HKU).

## Causal Effect Estimation
### Method 1: Matching
**Function We Provide:** Matching two datasets to obtain semantically similar pairs of data (by SentenceBERT embedding)
- Code: ______
- How to Run:

### Method 2: Do-Calculus
- Step 1. Get the estimand
- Step 2. Statistical estimation of the estimand

**Function We Provide:** For each data sample, given text embedding `text_emb` and a set of features `feats`, we want to learn `P(effect | text_emb, feats)` by a neural network model.
- Code: ______
- How to Run:
