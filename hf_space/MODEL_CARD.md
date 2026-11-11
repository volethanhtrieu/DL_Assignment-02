---
language: en
library_name: transformers
pipeline_tag: text-classification
base_model: distilbert-base-uncased
datasets:
- dair-ai/emotion
tags:
- text-classification
- emotion
- distilbert
- co3133
---

# Group Goat · Emotion classification (CO3133 Assignment 02)

Checkpoints of CO3133 Deep Learning and Its Applications, Assignment 02 (HCMUT, Semester 261), Group Goat.
Task: classify a short English text into one of six emotions of
[`dair-ai/emotion`](https://huggingface.co/datasets/dair-ai/emotion) (config `split`, revision
`cab853a1dbdf4c42c2b3ef2173804746df8825fe`): 0 sadness, 1 joy, 2 love, 3 anger, 4 fear, 5 surprise.

| File | Model | Test accuracy | Test Macro-F1 |
| :--- | :--- | :---: | :---: |
| `distil_full_min/` | DistilBERT (`distilbert-base-uncased`), full fine-tune, seed 42 (**selected model**) | 0.9270 | 0.8902 |
| `tfidf_lr_aggr_cw.joblib` | TF-IDF (uni + bigrams) + Logistic Regression, stopwords removed, balanced class weights (**selected baseline**) | 0.8905 | 0.8548 |

Both were selected on the validation set before the test set was used; test = the 2,000 official test texts.
Training recipe of DistilBERT: minimal text (NFC, lowercase, single spaces), MAX_LEN 128, batch 16, 3 epochs,
AdamW (encoder 2e-5, head 1e-4), 10% linear warmup, class-weighted loss, checkpoint = epoch with the best
validation Macro-F1 (epoch 3), Colab Tesla T4.

## Use

```python
import re, unicodedata
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer, AutoModelForSequenceClassification

root = snapshot_download("REPO_ID")
tokenizer = AutoTokenizer.from_pretrained(f"{root}/distil_full_min")
model = AutoModelForSequenceClassification.from_pretrained(f"{root}/distil_full_min").eval()

def text_min(text):   # same preprocessing as in training
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text).lower().strip())

enc = tokenizer(text_min("i feel so lucky today"), truncation=True, max_length=128, return_tensors="pt")
print(model.config.id2label[model(**enc).logits.argmax(dim=1).item()])
```

The baseline file is a `joblib` dict `{"vectorizer", "model", "train_time_s"}` saved with scikit-learn 1.6.1;
it expects the aggressive text (stopwords removed, see `clean_aggr` in the demo's `app.py`).

## Limitations

The dataset texts are lowercase, without punctuation, and most start with "i feel ...". Labels follow emotion
words closely, so negated sentences ("i am not happy ...") are often classified by the emotion word. Part of
the remaining errors point to doubtful labels in the dataset.

Links: [code and report page](https://github.com/volethanhtrieu/DL_Assignment-02) ·
[assignment page](https://volethanhtrieu.github.io/DL_Assignment-02/) · demo: SPACE_URL
