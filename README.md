<div align="center">

# 🐐 DL_Assignment-02

### Emotion Classification — Dataset Proposal & Experiments

**Group Goat** · CO3133 Deep Learning and Its Applications · Semester 261

**Instructor:** Lê Thành Sách · Ho Chi Minh City University of Technology — VNU-HCM

![Milestone](https://img.shields.io/badge/Milestone-M2%20Draft-yellow)
![M1](https://img.shields.io/badge/M1-Approved-brightgreen)
![M2](https://img.shields.io/badge/M2-Done%20(validation%20results)-brightgreen)
![Dataset](https://img.shields.io/badge/Dataset-dair--ai%2Femotion-purple)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Deadline](https://img.shields.io/badge/M2%20Due-28%20Oct%202026%2023%3A59%20(UTC%2B7)-red)

[📄 M1 Proposal](docs/M1_Dataset_Proposal_01.md) · [📓 Notebook](notebooks/A2_emotion.ipynb) · [▶️ Open in Colab](https://colab.research.google.com/drive/1_lOO_rj4URPZd1rPW23bUQWONaKKatt6?usp=sharing) · [🌐 Assignment 02 Page](https://volethanhtrieu.github.io/DL_Assignment-02/) · [📊 W&B Project](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion)

</div>

---

## 🗺️ Milestone Overview

| Milestone | Deliverables | Status |
| :--- | :--- | :---: |
| 🟦 **M1 — Proposal** | Dataset Proposal (task, data, split, metrics, baseline, compute estimate). Main experiments may begin **only after _Approved_ or _Approved with conditions_**. | ✅ Approved |
| 🟨 **M2 — Draft** | Simple baseline + pretrained model in progress; EDA; preliminary metrics. | ✅ Done |
| 🟩 **M3 — Final** | Controlled experiment; error analysis; report; slides; video; assignment. | 🔄 In progress |

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

  Result files are in [`results/`](results/), the report page is the [Assignment 02 Page](https://volethanhtrieu.github.io/DL_Assignment-02/). The test set has not been used yet.
- **M3 — Final:** 🔄 In progress: freeze vs full fine-tune (main controlled experiment), test evaluation, error analysis, report, slides, video.


---

## ▶️ Run on Google Colab

1. Open the notebook: **[A2_emotion.ipynb on Colab](https://colab.research.google.com/drive/1_lOO_rj4URPZd1rPW23bUQWONaKKatt6?usp=sharing)**.
2. `Runtime → Change runtime type → T4 GPU`.
3. Run the cells from top to bottom. The config cell mounts Google Drive: checkpoints and `results/` are written there, and the last cell zips `results/` into `results_export.zip`.
4. Weights & Biases is optional. Without an API key the notebook prints `wandb login failed, continuing with USE_WANDB = False` and still runs; training curves are always saved as `results/history_<run>.csv`.

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
4. **View the runs.** Open the project page **[goat-a2-emotion](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion)**. Each run logs its config and, per epoch, `train_loss`, `val_loss`, `val_acc`, `val_macro_f1` and `lr`. The run IDs of the M2 runs (also in [`results/wandb_ids.json`](results/wandb_ids.json)):

   | Run | W&B run ID |
   | :--- | :--- |
   | `tfidf_lr_min_nocw` | [`qj08wkz3`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/qj08wkz3) |
   | `tfidf_lr_min_cw` | [`tsa2peq3`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/tsa2peq3) |
   | `distil_full_min` | [`jzslvovw`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/jzslvovw) |
   | `distil_full_min_s43` | [`y27wmzlf`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/y27wmzlf) |
   | `distil_full_min_s44` | [`0fm9vcsi`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/0fm9vcsi) |
   | `bert_full_min` | [`85r9a9tm`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/85r9a9tm) |
   | `bert_full_min_s43` | [`ru9xve8b`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/ru9xve8b) |
   | `bert_full_min_s44` | [`mx3x8w6f`](https://wandb.ai/trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/runs/mx3x8w6f) |

5. **Read the runs with the W&B Python API** (optional, after `wandb.login(...)`):
   ```python
   import wandb
   api = wandb.Api()
   runs = api.runs("trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion")
   for run in runs:
       print(run.name, run.id, run.summary.get("val_macro_f1"))
   history = api.run("trieu-vo1301-ho-chi-minh-city-university-of-technology/goat-a2-emotion/jzslvovw").history()
   ```

> [!NOTE]
> A logged-in user who runs the notebook with their own key logs to **their own** W&B account (same project name `goat-a2-emotion`). The group's project page above is only visible to others if its visibility is set to **Public** (W&B project → Settings).

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
