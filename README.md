<div align="center">

# 🐐 DL_Assignment-02

### Emotion Classification — Dataset Proposal & Experiments

**Group Goat** · CO3133 Deep Learning and Its Applications · Semester 261

**Instructor:** Lê Thành Sách · Ho Chi Minh City University of Technology — VNU-HCM

![Milestone](https://img.shields.io/badge/Milestone-M3%20Final-blue)
![M1](https://img.shields.io/badge/M1-Approved-brightgreen)
![M2](https://img.shields.io/badge/M2-Done-brightgreen)
![M3](https://img.shields.io/badge/M3-Done-brightgreen)
![Dataset](https://img.shields.io/badge/Dataset-dair--ai%2Femotion-purple)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Deadline](https://img.shields.io/badge/M3%20Due-11%20Nov%202026%2023%3A59%20(UTC%2B7)-red)

[📄 M1 Proposal](docs/M1_Dataset_Proposal_01.md) · [📓 Notebook](notebooks/A2_emotion.ipynb) · [▶️ Open in Colab](https://colab.research.google.com/drive/1F15lvbEVO81kwdqBB7uy2gbuvXwpHDBy?usp=sharing) · [🌐 Assignment 02 Page](https://volethanhtrieu.github.io/DL_Assignment-02/) · [📊 W&B Project](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion) · [💾 Checkpoints (Drive)](https://drive.google.com/drive/folders/1WttjY7wrF5sedQDN2Oqnfmd_Hs6dLFk4?usp=drive_link) · [🤗 Model](https://huggingface.co/TrieuVo/goat-a2-emotion) · [🎮 Live Demo](https://huggingface.co/spaces/TrieuVo/goat-a2-emotion-demo) · [📑 Report (PDF)](report/Goat_A2_Report.pdf) · [🖼️ Slides (PDF)](slides/Goat_A2_Slides.pdf) · [🎬 Video (YouTube)](https://www.youtube.com/watch?v=ok-hF_vicjc)

</div>

---

## 🗺️ Milestone Overview

| Milestone | Deliverables | Status |
| :--- | :--- | :---: |
| 🟦 **M1 — Proposal** | Dataset Proposal (task, data, split, metrics, baseline, compute estimate). Main experiments may begin **only after _Approved_ or _Approved with conditions_**. | ✅ Approved |
| 🟨 **M2 — Draft** | Simple baseline + pretrained model in progress; EDA; preliminary metrics. | ✅ Done |
| 🟩 **M3 — Final** | Controlled experiment; error analysis; report; slides; video; assignment page; checkpoints. | ✅ Done |

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
| **Võ Lê Thành Triệu** | **2453297** | **100%** | **Assignment 02** |
| Nguyễn Huỳnh Nam Quốc | 2453089 | **0%** | Assignment 3. |

---

## 📌 Current Status

- **M1 — Proposal:** ✅ **Approved.** [M1 Dataset Proposal](docs/M1_Dataset_Proposal_01.md).
- **M2 — Draft:** ✅ **Done.** Full run of [`notebooks/A2_emotion.ipynb`](notebooks/A2_emotion.ipynb) on Colab (Tesla T4): EDA, filtering (15,923 / 1,993 / 2,000), TF-IDF + Logistic Regression baseline, DistilBERT and BERT full fine-tune with 3 seeds each. Preliminary results on **validation only** (Macro-F1):

  | Model | Runs | Val Macro-F1 |
  | :--- | :---: | :---: |
  | TF-IDF + LR (balanced class weights) | 1 | 0.8489 |
  | DistilBERT, full fine-tune | 3 seeds | 0.9155 ± 0.0020 |
  | BERT, full fine-tune | 3 seeds | 0.9163 ± 0.0032 |

  Result files are in [`results/`](results/), the report page is the [Assignment 02 Page](https://volethanhtrieu.github.io/DL_Assignment-02/). At M2 the test set had not been used yet.
- **M3 — Final:** ✅ **Done.** Notebook, experiments, test evaluation, error analysis, compute cost, export, checkpoints, assignment page, [report](report/Goat_A2_Report.pdf) (the same file is submitted on the LMS as `Goat_A2_Report.pdf`), [slides](slides/Goat_A2_Slides.pdf) and the [presentation video](https://www.youtube.com/watch?v=ok-hF_vicjc).
  - **Controlled experiments (validation, 3 seeds where trained):** DistilBERT frozen encoder vs full fine-tune (main): 0.4191 ± 0.0061 vs 0.9155 ± 0.0020, full fine-tune is needed. BERT vs DistilBERT: 0.9163 ± 0.0032 vs 0.9155 ± 0.0020, a tie (gap below the seed std), so the smaller DistilBERT is kept. Baseline: stopwords removed beat kept (0.8758 vs 0.8489), class weights on beat off (0.8489 vs 0.7527).
  - **Model selection** was made on validation with rules fixed before any test result: DistilBERT full fine-tune, seed-42 run (`distil_full_min`), and baseline `tfidf_lr_aggr_cw`. The test set was then used once for all 12 runs:

  | Model | Runs | Test Acc (seed 42) | Test Macro-F1 (seed 42) | Test Macro-F1 over seeds |
  | :--- | :---: | :---: | :---: | :---: |
  | **DistilBERT, full fine-tune (selected)** | 3 seeds | **0.9270** | **0.8902** | 0.8861 ± 0.0038 |
  | BERT, full fine-tune | 3 seeds | 0.9280 | 0.8881 | 0.8878 ± 0.0004 |
  | TF-IDF + LR, stopwords removed, class weights (selected baseline) | 1 | 0.8905 | 0.8548 | – |
  | DistilBERT, frozen encoder | 3 seeds | 0.5010 | 0.4199 | 0.4210 ± 0.0020 |
  | Majority class (always joy) | – | 0.3475 | 0.0860 | – |

  - **Error analysis (test):** DistilBERT makes 146 errors (baseline 219, BERT 144), mostly between close emotions: joy ↔ love, within sadness / anger / fear, fear ↔ surprise. 50 texts are given the same wrong label by all three models, and the 9 disputed test texts DistilBERT gets wrong all match the label of their train/val copy, a sign of label noise.
  - **Cost:** BERT needs 1.89× the training time and 2.00× the CPU latency of DistilBERT for +0.0016 test Macro-F1; the baseline is about 45× faster than DistilBERT on the same CPU.
  - Full write-up: the [Assignment 02 Page](https://volethanhtrieu.github.io/DL_Assignment-02/). Every number comes from [`results/`](results/).


---

## 📁 Repository Structure

```
DL_Assignment-02/
├── index.html                      ← Assignment 02 page served by GitHub Pages (copy of site/assignment02.html)
├── README.md                       ← this file: status, results, how to run, checkpoints, demo
├── AI_USAGE.md                     ← AI usage disclosure (handbook §5)
│
├── docs/
│   ├── M1_Dataset_Proposal_01.md   ← approved dataset proposal (data, split, metrics, models)
│   └── handbook.pdf                ← course handbook
│
├── notebooks/
│   └── A2_emotion.ipynb            ← the whole pipeline, run on Colab: EDA → filtering → baseline →
│                                     DistilBERT / BERT → experiments → test → error analysis → cost → export
│
├── results/                        ← every number and figure of the report and page comes from here
│   ├── results.csv                 ← one row per run and split (val + test): accuracy, Macro-F1, time, params
│   ├── history_<run>.csv           ← per-epoch train/val loss, val accuracy, val Macro-F1, LR (9 transformer runs)
│   ├── per_class_{val,test}_<run>.csv ← precision / recall / F1 per class
│   ├── test_predictions.csv        ← test predictions of the 4 main runs
│   ├── errors_<run>.csv            ← misclassified test texts with error group flags
│   ├── cost.csv, timing.csv        ← compute cost table and repeated inference timings
│   ├── split_stats.csv             ← split sizes and class shares after filtering
│   ├── checkpoints.csv             ← Drive path, size, best epoch and W&B id of each run
│   ├── config.json, hardware.json  ← all settings, selection rules, library versions, GPU/CPU
│   ├── wandb_ids.json              ← W&B run ids
│   └── figures/                    ← EDA plots, training curves, confusion matrices, cost plot
│
├── site/
│   ├── assignment02.html           ← source of the assignment page (edited here, then copied to /index.html)
│   ├── index.html                  ← Assignment 02 overview cards
│   └── assets/images/              ← figures and architecture diagrams used by the page
│
├── report/
│   ├── Goat_A2_Report.tex          ← LaTeX report (compile with XeLaTeX)
│   ├── hcmut.png, figures/         ← logo and figures copied from results/figures/
│   └── Goat_A2_Report.pdf          ← final PDF (same file is submitted on the LMS)
│
├── slides/
│   ├── Goat_A2_Slides.tex          ← Beamer slides (compile with XeLaTeX)
│   └── Goat_A2_Slides.pdf          ← slides used in the video
│
└── hf_space/                       ← Hugging Face model repo + live demo
    ├── export_web.py               ← DistilBERT → ONNX, baseline → baseline.json, check on the 2,000 test texts
    ├── upload_to_hf.py             ← uploads the model repo and the static Space
    ├── MODEL_CARD.md, SPACE_README.md
    └── static/index.html, goat.js  ← the demo page (runs both models in the browser)
```

Not in the repository: model checkpoints (Google Drive folder and Hugging Face model repo, see below) and the
dataset (downloaded by the notebook from the Hugging Face Hub at a pinned revision).

## ▶️ Run on Google Colab

1. Open the notebook: **[A2_emotion.ipynb on Colab](https://colab.research.google.com/drive/1F15lvbEVO81kwdqBB7uy2gbuvXwpHDBy?usp=sharing)**.
2. `Runtime → Change runtime type → T4 GPU`.
3. Run the cells from top to bottom. The config cell mounts Google Drive: checkpoints and `results/` are written there, and the last cell zips `results/` into `results_export.zip`.
4. Weights & Biases is optional. Without an API key the notebook prints `wandb login failed, continuing with USE_WANDB = False` and still runs; training curves are always saved as `results/history_<run>.csv`.

## 🔁 Reproducibility: install, prepare data, train, evaluate

Everything runs inside the one notebook on Google Colab; there is no separate script to install or call.

| Step | What to do |
| :--- | :--- |
| **Install** | Run the first code cell. Colab already has PyTorch, transformers and scikit-learn; the cell installs the two pinned extras: `pip install -q datasets==4.8.5 wandb==0.28.1`. |
| **Prepare the data** | Run the `# EDA` section of the notebook (from *Load dataset* to *Preprocessing*). It downloads `dair-ai/emotion` (config `split`) from the Hugging Face Hub at the pinned revision `cab853a1dbdf4c42c2b3ef2173804746df8825fe`, applies the 4 filtering rules of the proposal (15,923 / 1,993 / 2,000 texts) and builds the two text versions (`text_min`, `text_aggr`). No manual download is needed. |
| **Train** | Set `LOAD_CKPT = False` in the config cell, then `Runtime → Run all` on a T4 GPU. All 12 runs are trained (about 45 minutes in total) and each keeps its best-validation epoch in `MyDrive/DL/A2/checkpoints/`. |
| **Evaluate** | Keep `LOAD_CKPT = True` with the checkpoints in `MyDrive/DL/A2/checkpoints/` (see [Checkpoints](#-checkpoints)), then `Run all`. Saved runs are loaded instead of trained; section `# Final Evaluation (Test)` selects the models on validation and evaluates all 12 runs on test once. Results are written to `MyDrive/DL/A2/results/` and zipped into `results_export.zip`. |
| **Configuration** | One config cell holds every setting (dataset revision, `MAX_LEN = 128`, batch 16, 3 epochs, learning rates 2e-5 / 1e-4, warmup 0.1, class weights, switches). The values used are exported to `results/config.json`. |
| **Seeds** | `SEED = 42`, `SEEDS = [42, 43, 44]` for the transformer runs; the training batch order depends only on the seed. |
| **Dependency versions** (final run, `results/hardware.json`) | Python 3.13.16 · torch 2.14.1+cu130 · transformers 5.22.1 · scikit-learn 1.6.1 · datasets 4.8.5 · wandb 0.28.1 · CUDA 13.0 |
| **Hardware** | Colab Tesla T4 (14.6 GB), Intel Xeon @ 2.00 GHz × 2 vCPU, 12.7 GB RAM |
| **Submitted version** | Git tag [`a2-final`](https://github.com/volethanhtrieu/DL_Assignment-02/tree/a2-final): the commit submitted for Assignment 02 (M3 Final, 11 Nov 2026). Check it out with `git checkout a2-final`. |

## 💾 Checkpoints

Each run saves the epoch with the best **validation Macro-F1** to `MyDrive/DL/A2/checkpoints/<run>/` on Google Drive (Hugging Face folder: weights, config with label names, tokenizer, `train_info.json`). Baselines are saved as `MyDrive/DL/A2/checkpoints/<run>.joblib` (fitted TF-IDF vectorizer + logistic regression).

- **Google Drive folder (all checkpoints):** **[DL on Google Drive](https://drive.google.com/drive/folders/1WttjY7wrF5sedQDN2Oqnfmd_Hs6dLFk4?usp=drive_link)**: the whole `DL` folder used by the notebook, view only, no sign-in needed. Its layout (paths from the notebook config cell):

  ```
  DL/
  └── A2/
      ├── checkpoints/
      │   ├── distil_full_min/            ← selected model (DistilBERT full fine-tune, seed 42, best epoch 3)
      │   ├── distil_full_min_s43/   distil_full_min_s44/
      │   ├── bert_full_min/   bert_full_min_s43/   bert_full_min_s44/
      │   ├── distil_freeze_min/   distil_freeze_min_s43/   distil_freeze_min_s44/
      │   ├── tfidf_lr_aggr_cw.joblib     ← selected baseline
      │   └── tfidf_lr_min_cw.joblib   tfidf_lr_min_nocw.joblib
      ├── results/                        ← same files as results/ in this repository
      ├── results_export.zip
      └── checkpoints_final.zip           ← distil_full_min/ + tfidf_lr_aggr_cw.joblib (257.3 MB)
  ```
- **How to get a checkpoint:**
  1. Open the folder link and go to `A2 → checkpoints`.
  2. Selected model and baseline only: download `A2/checkpoints_final.zip` (one file) and unzip it.
  3. Any other run: right-click its folder (for example `bert_full_min`) → **Download**. Drive zips the folder; unzip it and load it as below.
- **Hugging Face:** the selected model and baseline are also on the Hub, **[TrieuVo/goat-a2-emotion](https://huggingface.co/TrieuVo/goat-a2-emotion)** (`distil_full_min/` + `tfidf_lr_aggr_cw.joblib`, with a model card).
- **Every run:** the list (Drive path, size, best epoch, train time, wandb run id) is in `results/checkpoints.csv`, written by the last notebook cell.
- **Load the selected model:** `AutoModelForSequenceClassification.from_pretrained("distil_full_min")` plus `AutoTokenizer.from_pretrained("distil_full_min")`. Input text must get the same preprocessing as in training: NFC, lowercase, single spaces. Example code is in section 10 of the report page.
- **Rebuild all checkpoints:** set `LOAD_CKPT = False` in the config cell and choose `Runtime → Run all` on a T4. Training takes about 45 minutes in total. Dataset revision, seeds (42 / 43 / 44) and library versions (`results/hardware.json`) are pinned. On 8 Nov 2026 a run from scratch, with the old checkpoints deleted, reproduced every validation metric of the earlier runs exactly; only the timings changed.
- **Evaluate without retraining:** download the run folders and upload them to your own Drive as `MyDrive/DL/A2/checkpoints/`, then keep `LOAD_CKPT = True`. Runs with a checkpoint are loaded, and the others are trained. Copy the folders rather than adding a shortcut: the shared folder is read-only, and the notebook writes its results next to the checkpoints.

## 🤗 Hugging Face: Model Repo and Live Demo

The selected model and baseline are published on Hugging Face through two links with different roles:

| Link | What it is | Role in this project | Use it to |
| :--- | :--- | :--- | :--- |
| **[TrieuVo/goat-a2-emotion](https://huggingface.co/TrieuVo/goat-a2-emotion)** | **Model repository** (public): `distil_full_min/` (DistilBERT full fine-tune, seed 42: `model.safetensors`, config with the 6 label names, tokenizer, `train_info.json`) + `tfidf_lr_aggr_cw.joblib` (TF-IDF + Logistic Regression) + a model card | Stores the **checkpoints** of the selected model and the selected baseline (handbook: link to checkpoints), next to the full set of 12 runs in the [Drive folder](https://drive.google.com/drive/folders/1WttjY7wrF5sedQDN2Oqnfmd_Hs6dLFk4?usp=drive_link) | Download the weights or load them in Python without retraining (code below) |
| **[TrieuVo/goat-a2-emotion-demo](https://huggingface.co/spaces/TrieuVo/goat-a2-emotion-demo)** | **Space** (interactive web page) | **Live demo**: shows how the two selected models behave on sentences that are not in the dataset. Also embedded in section 12 "Live Demo" of the [Assignment 02 Page](https://volethanhtrieu.github.io/DL_Assignment-02/#live-demo), so it runs directly inside the site | Type a sentence and compare DistilBERT with the baseline (probability of each emotion, text each model receives after preprocessing). No account, installation or GPU needed |

**Load the checkpoints from the model repo:**

```python
import re, unicodedata
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer, AutoModelForSequenceClassification

root = snapshot_download("TrieuVo/goat-a2-emotion")
tokenizer = AutoTokenizer.from_pretrained(f"{root}/distil_full_min")
model = AutoModelForSequenceClassification.from_pretrained(f"{root}/distil_full_min").eval()

text = re.sub(r"\s+", " ", unicodedata.normalize("NFC", "I feel so lucky today").lower().strip())  # text_min, as in training
enc = tokenizer(text, truncation=True, max_length=128, return_tensors="pt")
print(model.config.id2label[model(**enc).logits.argmax(dim=1).item()])
```

**How the demo works:**

- Free Hugging Face accounts can only host **static** Spaces, so both models run in the visitor's browser: DistilBERT as ONNX with [transformers.js](https://huggingface.co/docs/transformers.js) (downloaded on the first prediction), the baseline from its saved TF-IDF and Logistic Regression weights in plain JavaScript.
- DistilBERT runs with its **float32 weights unchanged** (ONNX, 255 MB, downloaded once on the first prediction). Checked on the 2,000 test texts: same class as the original checkpoint on all 2,000 (accuracy 0.9270, Macro-F1 0.8902); the JavaScript baseline also on all 2,000.
- The training texts are lowercase English without punctuation, mostly "i feel ...", so sentences written that way are closest to what the models learned. A typed sentence is new data: the demo shows behaviour, not a score (the scores are the test results above).
- Source in [`hf_space/`](hf_space/): `export_web.py` (ONNX + `baseline.json` export and the test check), `static/index.html` + `static/goat.js` (the page), `upload_to_hf.py` (model repo + Space upload), `MODEL_CARD.md`.

## 📊 Weights & Biases: log in with your API key on Colab

The API key is **never written in the notebook** (the repo is public). It is read from Colab Secrets.

1. **Get the key.** Sign in at [wandb.ai](https://wandb.ai), then open [wandb.ai/authorize](https://wandb.ai/authorize) and copy the API key.
2. **Store it in Colab Secrets.** In the Colab notebook, click the 🔑 **Secrets** icon in the left sidebar → **Add new secret**:
   - Name: `WANDB_API_KEY`
   - Value: the key from step 1
   - Turn on **Notebook access** for this notebook.
3. **Run the notebook.** The config cell keeps `USE_WANDB = True` and logs in with:
   ```python
   from google.colab import userdata
   wandb.login(key=userdata.get("WANDB_API_KEY"))
   ```
   It prints `USE_WANDB = True` when the login works. Each training run then prints its own run link.
> [!WARNING]
> **The W&B links printed in the notebook output are out of date.** They point to `wandb.ai/ngcminh0410-hcmut/goat-a2-emotion/...`, the account the runs were logged to on 8 Nov 2026. The runs were moved afterwards (same run IDs) to the project below, so **use the links in this README**, not the ones in the notebook.

4. **View the runs.** Open the project page **[goat-a2-emotion](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion)**. Each run logs its config and, per epoch, `train_loss`, `val_loss`, `val_acc`, `val_macro_f1` and `lr`. The 12 runs behind every reported number come from the full rerun of 8 Nov 2026. Their IDs are also in [`results/wandb_ids.json`](results/wandb_ids.json) and [`results/checkpoints.csv`](results/checkpoints.csv), and each run's Summary holds its `test_acc` and `test_macro_f1`. For transformer runs, compare `best_val_macro_f1`, not `val_macro_f1` (last epoch):

   | Run | W&B run ID |
   | :--- | :--- |
   | `tfidf_lr_min_nocw` | [`7wlsxtx8`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/7wlsxtx8) |
   | `tfidf_lr_min_cw` | [`pwfi016q`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/pwfi016q) |
   | `tfidf_lr_aggr_cw` | [`3ojjzuey`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/3ojjzuey) |
   | `distil_full_min` | [`lnuy747a`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/lnuy747a) |
   | `distil_full_min_s43` | [`psflj88c`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/psflj88c) |
   | `distil_full_min_s44` | [`llw3bte9`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/llw3bte9) |
   | `bert_full_min` | [`ulss79nz`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/ulss79nz) |
   | `bert_full_min_s43` | [`pil00scg`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/pil00scg) |
   | `bert_full_min_s44` | [`noxjos1c`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/noxjos1c) |
   | `distil_freeze_min` | [`7rugvdvg`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/7rugvdvg) |
   | `distil_freeze_min_s43` | [`83s806pr`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/83s806pr) |
   | `distil_freeze_min_s44` | [`k1uomhhg`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/k1uomhhg) |

5. **Read the runs with the W&B Python API** (optional, after `wandb.login(...)`):
   ```python
   import wandb
   api = wandb.Api()
   runs = api.runs("trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion")
   for run in runs:
       print(run.name, run.id, run.summary.get("val_macro_f1"))
   history = api.run("trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/lnuy747a").history()   # distil_full_min
   ```

> [!NOTE]
> A logged-in user who runs the notebook with their own key logs to **their own** W&B account (same project name `goat-a2-emotion`). The group's project page above is **public**, so it can be viewed without an account.

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
