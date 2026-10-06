# M1 — Dataset Proposal 01

**Assignment 02 — Text Classification Track**  
**Status: Draft for submission; instructor approval pending.**

We propose emotion classification using the six-class `split` configuration of `dair-ai/emotion`. We will retain its official train/validation/test splits, perform preliminary EDA on each split, and audit duplicates across splits. Training data will guide preprocessing decisions. Main experiments and the proposed filtering will begin only after instructor approval.

Section 4 reports measurements from our existing EDA audit. Model methods, filtering rules, and compute resources below are proposed plans. The supporting audit is `outputs/m1/audit_summary.json`; it and the EDA notebook will be made accessible in the submitted repository.

## 1. Dataset name, source, version, and license

We propose **[Emotion (`dair-ai/emotion`)](https://huggingface.co/datasets/dair-ai/emotion)**, using its six-class **`split` configuration**. Its academic reference is [Saravia et al., *CARER: Contextualized Affect Representations for Emotion Recognition*, EMNLP 2018](https://aclanthology.org/D18-1404/).

For reproducibility, we will use Hugging Face revision [`cab853a1dbdf4c42c2b3ef2173804746df8825fe`](https://huggingface.co/datasets/dair-ai/emotion/tree/cab853a1dbdf4c42c2b3ef2173804746df8825fe).

The [pinned dataset card](https://huggingface.co/datasets/dair-ai/emotion/blob/cab853a1dbdf4c42c2b3ef2173804746df8825fe/README.md) lists the license as **`other`**. The card and [authors' repository](https://github.com/dair-ai/emotion_dataset) restrict usage to **educational and research purposes**. Our use is for an academic course assignment.

## 2. Task, input, and output definitions

The task is **single-label multiclass text classification**: predict one emotion from an English text. Each record contains two fields:

| Field | Type | Meaning |
|---|---|---|
| `text` | String | The English text supplied to the classifier |
| `label` | Integer, 0–5 | One categorical emotion label |

The label mapping is **0 = sadness, 1 = joy, 2 = love, 3 = anger, 4 = fear, 5 = surprise**.

The **input** is one text. The **output** is one of these six emotions. The prediction unit is an individual text record. The main difficulties identified so far are class imbalance and inconsistent labels for some identical texts.

## 3. Number of samples and annotation types

The published `split` configuration contains **20,000 examples**:

| Official split | Number of examples | Planned purpose |
|---|---:|---|
| Training | 16,000 | Fit preprocessing and train models |
| Validation | 2,000 | Select hyperparameters and model checkpoints |
| Test | 2,000 | Evaluate the selected models after model selection |

Each example has one categorical emotion label. The pinned dataset-card metadata identifies annotations as **machine-generated**, while the annotation-process description is incomplete. Possible annotation noise is therefore a limitation; conflicting labels will be documented without assuming which label is correct.

We will use all 20,000 examples in this configuration as the starting dataset. The separate **`unsplit` configuration with 416,809 examples** is outside this proposal.

## 4. Preliminary distribution analysis

We loaded the official splits without merging or randomly re-splitting them. Preliminary EDA checked class distributions, text lengths, missing or invalid values, and duplicate texts within and across splits.

| Emotion | Train count (%) | Validation count | Test count |
|---|---:|---:|---:|
| Sadness | 4,666 (29.16%) | 550 | 581 |
| Joy | 5,362 (33.51%) | 704 | 695 |
| Love | 1,304 (8.15%) | 178 | 159 |
| Anger | 2,159 (13.49%) | 275 | 275 |
| Fear | 1,937 (12.11%) | 212 | 224 |
| Surprise | 572 (3.58%) | 81 | 66 |

All three splits contain all six classes. Training is imbalanced: joy is the largest class and surprise is the smallest. The training imbalance ratio is **5,362 / 572 ≈ 9.37**. No missing, blank, non-string texts or invalid labels were detected.

| Training length unit | Min | Median | Mean | P95 | Max |
|---|---:|---:|---:|---:|---:|
| Characters | 7 | 86 | 96.85 | 207.05 | 300 |
| Whitespace-separated words | 2 | 17 | 19.17 | 41 | 66 |

Whitespace-separated words are not model tokens. DistilBERT token lengths will be checked separately on training data before confirming a truncation limit.

Exact-text and normalized-text duplicate checks gave the same group counts:

| Duplicate-check scope | Repeated or shared text groups |
|---|---:|
| Within training | 31 |
| Within validation | 2 |
| Within test | 0 |
| Training–validation overlap | 5 |
| Training–test overlap | 11 |
| Validation–test overlap | 3 |

Across the complete 20,000-example configuration, **51 of 52 repeated-text groups have conflicting labels**, involving **102 rows**. A repeated-text group contains at least two records sharing the same text key; it is not a count of excess rows to remove. These findings identify potential leakage and label inconsistency. They do not establish which label is correct.

These statistics describe the original release. **The EDA notebook has not applied the proposed filtering policy.**

## 5. Data-splitting plan

We will **retain the official train/validation/test splits**. Loading the complete configuration means loading all three splits while preserving their membership.

Our workflow is:

1. Load and retain the official splits.
2. Audit each split and identify duplicate groups across splits.
3. Use training EDA to guide preprocessing decisions.
4. Obtain approval for the dataset and proposed filtering rules.
5. Apply the approved rules and record final split sizes and class counts before experiments.

We propose the following filtering rules, applied in this order:

1. **Preserve the official test set**, including its released labels. Remove every training or validation record whose normalized text occurs in the test set.
2. For remaining training–validation overlaps, **retain validation records and remove matching training records**.
3. Within each remaining training or validation split, **remove all records belonging to a repeated-text group with conflicting labels**. Do not choose or invent a replacement label.
4. For remaining same-label duplicates within training or validation, **retain one record per group**, selected deterministically by original row order.

These are proposed rules for instructor review. Test-associated label conflicts will remain documented as a limitation, and any instructor conditions will be recorded. We will report removal counts by reason and verify that all six classes remain represented and at least 5,000 training examples remain.

The same approved splits will be used for both model methods. Test predictions and performance will not guide preprocessing, hyperparameter selection, or checkpoint selection.

## 6. Split unit used to prevent leakage

The operational grouping unit is **a group of records with the same normalized text**. The normalization used to identify duplicate groups is:

**Unicode NFC → lowercasing → trimming leading/trailing whitespace → collapsing consecutive whitespace.**

Although predictions are made for individual records, records in the same normalized-text group must not cross the final splits. After approved filtering, we will verify that no normalized text is shared between training, validation, and test.

This check addresses exact and normalized duplicates; near-duplicate leakage remains a limitation unless further audited. The release provides no author IDs, so author overlap cannot be verified.

Learned preprocessing, including the TF-IDF vocabulary and IDF weights, will be fitted **only on training data**. Validation and test data will use the fitted preprocessing unchanged.

## 7. Evaluation metrics

Following **course handbook §20.1**, we will report **accuracy and macro-F1**:

- **Accuracy:** the overall proportion of correctly classified texts.
- **Macro-F1:** the mean of the six class-specific F1 scores, giving each emotion equal weight despite unequal class sizes.

**Validation macro-F1** will be the primary model-selection criterion. Accuracy will be reported alongside it. Final test evaluation will occur after model selection, using the same test set for both methods.

## 8. Baseline plan

We will use **TF-IDF + logistic regression** as the simple baseline.

TF-IDF converts individual words and two-word combinations into numerical importance weights. Logistic regression uses these features to predict one of the six emotions. This method is inexpensive and provides a clear comparison for the pretrained model.

Planned preprocessing includes Unicode NFC normalization, trimming/collapsing whitespace, and lowercase word tokenization. The vocabulary and IDF weights will be fitted only on the approved training split. Validation data will guide any hyperparameter selection.

## 9. Planned pretrained model

We will fine-tune **[DistilBERT (`distilbert-base-uncased`)](https://huggingface.co/distilbert/distilbert-base-uncased)** with a six-class prediction layer, updating the pretrained encoder and classification layer.

DistilBERT uses learned contextual language representations. Its smaller architecture reduces computational demands compared with BERT while supporting text classification ([Sanh et al., 2019](https://arxiv.org/abs/1910.01108)).

We will use its own **WordPiece tokenizer**, with padding and truncation. The initial maximum sequence length is **128 tokens, including special tokens**. We will measure token lengths and the proportion exceeding this limit on training data before confirming it.

The initial training budget is **batch size 16 and three epochs**. Checkpoints will be selected by validation macro-F1. Both methods will use the same approved data splits and evaluation metrics.

## 10. Compute estimate

Planned hardware is **Google Colab with an NVIDIA T4 GPU, approximately 15 GB usable GPU memory**, for DistilBERT fine-tuning, subject to availability. A Colab CPU runtime will be used for the TF-IDF baseline.

We plan for **8–12 GB system RAM** and **2–4 GB free storage** for model/tokenizer files, logs, and limited checkpoints. Actual GPU assignment, available RAM, and disk capacity will be confirmed before training.

The unbenchmarked baseline estimate is **2–6 minutes per fit**. For DistilBERT, the original 16,000 training examples, batch size 16, three epochs, and no gradient accumulation give:

**Optimizer steps = ceil(16,000 / 16) × 3 = 3,000.**

At an assumed **0.1–0.4 seconds per step**, the training portion is approximately **5–20 minutes**. We reserve **10–35 minutes end to end** for loading, tokenization, training, validation, and checkpointing.

These are planning estimates, not measured results. After approval and filtering, we will recalculate the step count using the actual training size and refine the estimate with a timed run.

## 11. Subset selection rules

We plan to use **all examples in the official `split` configuration**, subject to approved data-quality filtering. No additional random subset is planned.

Any later subset will have a documented purpose, use a fixed recorded seed, preserve all six classes, and retain **at least 5,000 training examples**. Any change affecting the approved dataset protocol will be documented and submitted for instructor review before use.

