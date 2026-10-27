<div align="center">

# 🐐 DL_Assignment-02

### Emotion Classification — Dataset Proposal & Experiments

**Group Goat** · CO3133 Deep Learning · Semester 261

![Milestone](https://img.shields.io/badge/Milestone-M1%20Proposal-blue)
![Status](https://img.shields.io/badge/Status-Draft%20%E2%80%94%20not%20submitted-orange)
![Dataset](https://img.shields.io/badge/Dataset-dair--ai%2Femotion-purple)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Deadline](https://img.shields.io/badge/M1%20Due-07%20Oct%202026%2023%3A59%20(UTC%2B7)-red)

[📄 M1 Proposal](assignment02-m1.html) · [📓 Notebook](notebooks/m1_dataset_check.ipynb) · [🌐 Assignment 02 Page](index.html) · [✅ Readiness Report](outputs/m1/readiness_report.md)

</div>

---

## 🗺️ Milestone Overview

| Milestone | Deliverables | Status |
| :--- | :--- | :---: |
| 🟦 **M1 — Proposal** | Dataset Proposal (task, data, split, metrics, baseline, compute estimate). Main experiments may begin **only after _Approved_ or _Approved with conditions_**. | 📝 Draft |
| 🟨 **M2 — Draft** | Simple baseline + pretrained model in progress; EDA; preliminary metrics. | ⏳ Not started |
| 🟩 **M3 — Final** | Controlled experiment; error analysis; report; slides; video; assignment. | ⏳ Not started |

## 📅 Deadlines

| Week | Milestone | Due (23:59, UTC+7) | Weight of A2 |
| :---: | :--- | :---: | :---: |
| **7** | 🟦 M1 Proposal | **07 Oct 2026** | `15%` of Assignment 2 |
| **10** | 🟨 M2 Draft | **28 Oct 2026** | `25%` of Assignment 2 |
| **12** | 🟩 M3 Final | **11 Nov 2026** | `60%` of Assignment 2 |

> [!IMPORTANT]
> Dates follow the course handbook unless a milestone-specific LMS announcement differs.

## 👥 Project Authorship & Individual Contribution

| Member Name | Student ID | Assignment 02 Contribution (%) | Role & Responsibilities |
| :--- | :---: | :---: | :--- |
| Hoàng Trọng Huy Minh | 2452743 | **0%** | Assignment 1. |
| **Võ Lê Thành Triệu** | **2453297** | **100%** | **M1 Dataset Proposal — wait for approval** |
| Nguyễn Huỳnh Nam Quốc | 2453089 | **0%** | Assignment 3. |

---

## 📌 Current Status

The [M1 Dataset Proposal](https://github.com/volethanhtrieu/DL_Assignment-02/blob/main/M1_Dataset_Proposal_01.md) is **Draft — not submitted**. No instructor decision has been received. The deadline is **7 October 2026, 23:59 Asia/Ho_Chi_Minh (UTC+7)** unless a milestone-specific LMS announcement differs. Aim to finish human review by 6 October. No models were trained, no later milestones implemented, and nothing was pushed, published, or submitted.


---

## 🔄 Plan Update — 27 Oct 2026

Because time remained before M3, the group added two things to the experiments. The [M1 Dataset Proposal](docs/M1_Dataset_Proposal_01.md) is **not changed**; this note records the update.

| Change | What | Why |
| :--- | :--- | :--- |
| ➕ **BERT** (`bert-base-uncased`) | Full fine-tune with exactly the same recipe as DistilBERT (`text_min`, MAX_LEN 128, batch 16, 3 epochs, LR 2e-5 / 1e-4, warmup 10%, balanced class weights, checkpoint by validation Macro-F1) and the same seeds 42, 43, 44 (`bert_full_min`, `bert_full_min_s43`, `bert_full_min_s44`) | To see how BERT (12 layers, about 1.6× the parameters) differs from the DistilBERT full fine-tune in accuracy and cost. This is a **second controlled experiment**: only the pretrained model changes, everything else is fixed |
| 🔁 **3 seeds for DistilBERT** | DistilBERT full fine-tune repeated with seeds 42, 43, 44 (`distil_full_min`, `distil_full_min_s43`, `distil_full_min_s44`); the frozen-backbone runs will use the same three seeds | One run cannot show run-to-run variation; mean ± std over seeds is the yardstick for every comparison |

There are now two controlled experiments, each changing one factor:

| | Changed factor | Kept fixed |
| :--- | :--- | :--- |
| **Main** | DistilBERT frozen backbone vs full fine-tune | model, data, text, recipe, seeds |
| **Second** | Pretrained model: BERT vs DistilBERT (both full fine-tune, 3 seeds each) | data, `text_min`, MAX_LEN 128, identical token ids, batch order, learning rates, epochs, warmup, class weights, seeds |

The second experiment changes the model as a whole (depth, pretrained pooler, distillation), so it shows *whether* BERT differs, not *which* of those parts causes it. All model selection uses the validation set; the test set is evaluated once, after selection.
