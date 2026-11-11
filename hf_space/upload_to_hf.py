"""Upload the selected checkpoints to a Hugging Face model repo and publish the static demo Space.

Usage (after `hf auth login` with a Write token):
    python hf_space/export_web.py <ckpt folder> <web folder>     # once, writes ONNX + baseline.json
    python hf_space/upload_to_hf.py <ckpt folder> <web folder>

<ckpt folder> = the unzipped checkpoints_final.zip from the group's Drive folder (DL/A2/):
distil_full_min/ and tfidf_lr_aggr_cw.joblib. Free accounts can only host static Spaces, so the demo runs in
the browser: DistilBERT as ONNX with transformers.js, the baseline from baseline.json in plain JavaScript.
"""
import os
import shutil
import sys
import tempfile

from huggingface_hub import HfApi

MODEL_NAME = "goat-a2-emotion"        # model repo:  <user>/goat-a2-emotion
SPACE_NAME = "goat-a2-emotion-demo"   # Space:       <user>/goat-a2-emotion-demo

ckpt_root, web_dir = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
assert os.path.isfile(os.path.join(ckpt_root, "distil_full_min", "model.safetensors"))
assert os.path.isfile(os.path.join(ckpt_root, "tfidf_lr_aggr_cw.joblib"))
assert os.path.isfile(os.path.join(web_dir, "model", "onnx", "model.onnx"))

api = HfApi()
user = api.whoami()["name"]
model_repo = f"{user}/{MODEL_NAME}"
space_repo = f"{user}/{SPACE_NAME}"
model_url = f"https://huggingface.co/{model_repo}"
space_url = f"https://huggingface.co/spaces/{space_repo}"


def filled(name):
    # Read a template from hf_space/ and put the real repo names in
    with open(os.path.join(here, name), encoding="utf-8") as f:
        text = f.read()
    return text.replace("REPO_ID", model_repo).replace("SPACE_URL", space_url).replace("MODEL_URL", model_url)


# 1) Model repo: the two original checkpoints + model card
api.create_repo(model_repo, repo_type="model", exist_ok=True)
api.upload_folder(repo_id=model_repo, folder_path=os.path.join(ckpt_root, "distil_full_min"),
                  path_in_repo="distil_full_min", commit_message="Add DistilBERT checkpoint (distil_full_min)")
api.upload_file(repo_id=model_repo, path_or_fileobj=os.path.join(ckpt_root, "tfidf_lr_aggr_cw.joblib"),
                path_in_repo="tfidf_lr_aggr_cw.joblib", commit_message="Add baseline checkpoint (tfidf_lr_aggr_cw)")
api.upload_file(repo_id=model_repo, path_or_fileobj=filled("MODEL_CARD.md").encode(), path_in_repo="README.md",
                commit_message="Update model card")

# 2) Static Space: page + script + exported models, gathered in one folder and uploaded in one commit
with tempfile.TemporaryDirectory() as stage:
    for name in ["index.html", "goat.js"]:
        shutil.copy(os.path.join(here, "static", name), stage)
    shutil.copy(os.path.join(web_dir, "baseline.json"), stage)
    shutil.copytree(os.path.join(web_dir, "model"), os.path.join(stage, "model"))
    with open(os.path.join(stage, "README.md"), "w", encoding="utf-8") as f:
        f.write(filled("SPACE_README.md"))
    api.create_repo(space_repo, repo_type="space", space_sdk="static", exist_ok=True)
    api.upload_folder(repo_id=space_repo, repo_type="space", folder_path=stage,
                      commit_message="Static demo: DistilBERT (ONNX) + TF-IDF baseline in the browser")

print("Model repo :", model_url)
print("Space      :", space_url)
print("Embed URL  :", api.space_info(space_repo).host)   # the *.hf.space address used in the site iframe
