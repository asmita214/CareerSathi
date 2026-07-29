import pandas as pd

def load_data(path="data/career_qa.csv"):
    df = pd.read_csv(path)
    df = df.dropna(subset=["role", "question", "answer"])
    return df

def build_chunks(df):
    chunks = []
    for _, row in df.iterrows():
        text = f"Role: {row['role']}\nQuestion: {row['question']}\nAnswer: {row['answer']}"
        chunks.append({
            "text": text,
            "role": row["role"]
        })
    return chunks

if __name__ == "__main__":
    df = load_data()
    chunks = build_chunks(df)
    print(f"Total chunks: {len(chunks)}")
    print(chunks[0])
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

def build_index(chunks):
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    texts = [c["text"] for c in chunks]

    print("Generating embeddings... this may take a few minutes for 1620 chunks.")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype("float32"))

    return index, embeddings

def save_index(index, chunks, index_path="data/faiss_index.bin", chunks_path="data/chunks.pkl"):
    faiss.write_index(index, index_path)
    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Saved index to {index_path} and chunks to {chunks_path}")
if __name__ == "__main__":
    df = load_data()
    chunks = build_chunks(df)
    print(f"Total chunks: {len(chunks)}")

    index, embeddings = build_index(chunks)
    save_index(index, chunks)