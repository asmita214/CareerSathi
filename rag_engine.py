import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def load_index(index_path="data/faiss_index.bin", chunks_path="data/chunks.pkl"):
    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def retrieve(query, index, chunks, top_k=4):
    query_vec = model.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_vec, top_k)
    results = [chunks[i] for i in indices[0]]
    return results

def generate_answer(query, retrieved_chunks):
    context = "\n\n".join([c["text"] for c in retrieved_chunks])

    prompt = f"""You are CareerSaathi, a helpful career guidance assistant.
Use the context below to answer the user's question as helpfully as possible.
The context may not use the exact same words as the question — use your judgment to connect related information (for example, "qualifications" and "skills" are related; "how to start a career" often includes the skills needed).
Only say you don't have the information if the context is truly unrelated to the question.
Respond in the SAME language the user asked in (English or Hindi).

Context:
{context}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    index, chunks = load_index()

    test_query = "डेटा साइंटिस्ट बनने के लिए मुझे कौन से स्किल्स चाहिए?"
    retrieved = retrieve(test_query, index, chunks)
    print("--- Retrieved Chunks ---")
    for i, r in enumerate(retrieved):
        print(f"{i+1}. {r['text'][:150]}...")
    print("------------------------\n")
    answer = generate_answer(test_query, retrieved)

    print("Query:", test_query)
    print("\nAnswer:", answer)