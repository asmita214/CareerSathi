from huggingface_hub import hf_hub_download
import shutil

path = hf_hub_download(
    repo_id="Pradeep016/career-guidance-qa-dataset",
    filename="Career QA Dataset.csv",
    repo_type="dataset"
)
shutil.copy(path, "data/career_qa.csv")
print("Saved to data/career_qa.csv")