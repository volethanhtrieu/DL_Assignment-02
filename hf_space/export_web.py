"""Export the two selected models so they can run in a web browser (static Hugging Face Space).

Usage:
    python hf_space/export_web.py <folder with distil_full_min/ and tfidf_lr_aggr_cw.joblib> <output folder>

Writes into <output folder>:
    model/config.json, model/tokenizer.json, model/tokenizer_config.json
    model/onnx/model.onnx             DistilBERT, float32 (same weights as model.safetensors)
    baseline.json                     TF-IDF vocabulary + idf, Logistic Regression coef + intercept
Then checks on the 2,000 test texts of results/test_predictions.csv that the exported models give the
same predicted class as the original checkpoints.
"""
import json
import os
import re
import shutil
import sys

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd
import torch
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from transformers import AutoModelForSequenceClassification, AutoTokenizer

ckpt_root, out_dir = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
distil_dir = os.path.join(ckpt_root, "distil_full_min")
model_dir = os.path.join(out_dir, "model")
onnx_dir = os.path.join(model_dir, "onnx")
os.makedirs(onnx_dir, exist_ok=True)

# ---------- 1) DistilBERT -> ONNX ----------
tokenizer = AutoTokenizer.from_pretrained(distil_dir)
model = AutoModelForSequenceClassification.from_pretrained(distil_dir).eval()
for name in ["config.json", "tokenizer.json", "tokenizer_config.json"]:
    shutil.copy(os.path.join(distil_dir, name), os.path.join(model_dir, name))


class LogitsOnly(torch.nn.Module):
    # ONNX graph with two inputs (input_ids, attention_mask) and one output (logits)
    def __init__(self, m):
        super().__init__()
        self.m = m

    def forward(self, input_ids, attention_mask):
        return self.m(input_ids=input_ids, attention_mask=attention_mask).logits


example = tokenizer(["i feel so lucky today", "i am sad"], padding=True, return_tensors="pt")
fp32_path = os.path.join(onnx_dir, "model.onnx")
torch.onnx.export(
    LogitsOnly(model), (example["input_ids"], example["attention_mask"]), fp32_path,
    input_names=["input_ids", "attention_mask"], output_names=["logits"],
    dynamic_axes={"input_ids": {0: "batch", 1: "sequence"}, "attention_mask": {0: "batch", 1: "sequence"},
                  "logits": {0: "batch"}},
    opset_version=17, dynamo=False,
)
print(f"ONNX fp32 {os.path.getsize(fp32_path) / 1024**2:.1f} MB")

# ---------- 2) Baseline -> JSON ----------
baseline = joblib.load(os.path.join(ckpt_root, "tfidf_lr_aggr_cw.joblib"))
vec, clf = baseline["vectorizer"], baseline["model"]
terms = [None] * len(vec.vocabulary_)
for term, idx in vec.vocabulary_.items():
    terms[idx] = term
KEEP_WORDS = {
    "not", "no", "nor", "never", "none", "nothing", "nobody", "nowhere", "neither",
    "cannot", "cant", "couldnt", "without",
    "very", "so", "too", "more", "most", "much", "less", "least", "enough",
    "but",
}
stop_words = sorted(set(ENGLISH_STOP_WORDS) - KEEP_WORDS)
r6 = lambda a: [float(f"{x:.6g}") for x in a]
baseline_json = {
    "run": "tfidf_lr_aggr_cw",
    "labels": [model.config.id2label[int(c)] for c in clf.classes_],
    "ngram_range": list(vec.ngram_range),
    "stop_words": stop_words,
    "terms": terms,
    "idf": r6(vec.idf_),
    "coef": [r6(row) for row in clf.coef_],
    "intercept": r6(clf.intercept_),
}
with open(os.path.join(out_dir, "baseline.json"), "w") as f:
    json.dump(baseline_json, f, separators=(",", ":"))
print(f"baseline.json {os.path.getsize(os.path.join(out_dir, 'baseline.json')) / 1024**2:.2f} MB, "
      f"{len(terms)} n-grams, {len(stop_words)} stopwords")

# ---------- 3) Check on the 2,000 test texts ----------
pred = pd.read_csv(os.path.join(here, "..", "results", "test_predictions.csv"))
texts = pred["text_min"].tolist()
label_names = [model.config.id2label[i] for i in range(len(model.config.id2label))]


def onnx_preds(path):
    sess = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
    out = []
    for i in range(0, len(texts), 64):
        enc = tokenizer(texts[i:i + 64], padding=True, truncation=True, max_length=128, return_tensors="np")
        logits = sess.run(None, {"input_ids": enc["input_ids"].astype(np.int64),
                                 "attention_mask": enc["attention_mask"].astype(np.int64)})[0]
        out += [label_names[k] for k in logits.argmax(axis=1)]
    return np.array(out)


ref_distil = pred["pred_distil_full_min"].to_numpy()
for name, path in [("fp32", fp32_path)]:
    p = onnx_preds(path)
    print(f"DistilBERT ONNX {name}: same class as the checkpoint on {(p == ref_distil).sum()} / {len(texts)} test texts, "
          f"accuracy {(p == pred['label_name'].to_numpy()).mean():.4f}")


def clean_aggr(text):
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(w for w in text.split() if w not in set(stop_words))


p_base = np.array([model.config.id2label[int(c)] for c in clf.predict(vec.transform([clean_aggr(t) for t in texts]))])
print(f"Baseline (sklearn, from text_min): same class as test_predictions.csv on "
      f"{(p_base == pred['pred_tfidf_lr_aggr_cw'].to_numpy()).sum()} / {len(texts)}")
