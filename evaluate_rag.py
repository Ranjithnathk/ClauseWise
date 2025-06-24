import json
import requests
from ragas import evaluate as ragas_evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset
import evaluate  # Hugging Face's evaluation library
import os
from statistics import mean

# --- Config ---
API_URL = "http://127.0.0.1:8000/chat"
EVAL_DATA_FILE = "evaluation_data.json"
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJxd2UiLCJleHAiOjE3NTA3MzczMTh9.L8lXbRk2sTEaL-bKlteGFWsfmU4RqXcMmhFdMHsW12Y"

# --- Load evaluation questions ---
with open(EVAL_DATA_FILE, "r") as f:
    data = json.load(f)

questions, answers, contexts, ground_truths = [], [], [], []
preds_for_hf, refs_for_hf = [], []

print("Starting evaluation...")

for item in data:
    pdf_name = item["pdf_name"]
    for qa in item["qa_pairs"]:
        question = qa["question"]
        expected_answer = qa["answer"]

        payload = {
            "model_name": "gpt-4o",
            "pdf_name": pdf_name,
            "messages": [question],
        }

        try:
            res = requests.post(
                API_URL,
                json=payload,
                headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
            )
            res.raise_for_status()
            answer = res.json().get("answer", "No answer returned.")
        except Exception as e:
            print(f"Failed for question: '{question}' - {e}")
            continue

        questions.append(question)
        answers.append(answer)
        contexts.append([f"Question: {question}\nAnswer: {answer}"])
        ground_truths.append([expected_answer])
        preds_for_hf.append(answer)
        refs_for_hf.append(expected_answer)

# --- RAGAS Evaluation ---
print("\n🔍 Running RAG Evaluation Metrics...")
ragas_dataset = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truths": ground_truths,
})
ragas_results = ragas_evaluate(ragas_dataset, metrics=[faithfulness, answer_relevancy])

# --- HF ROUGE and BERTScore ---
print("📐 Running ROUGE and BERTScore...")
rouge = evaluate.load("rouge")
bertscore = evaluate.load("bertscore")

rouge_results = rouge.compute(predictions=preds_for_hf, references=refs_for_hf)
bertscore_results = bertscore.compute(predictions=preds_for_hf, references=refs_for_hf, lang="en")

# --- Print All Results ---
print("\nEvaluation Results Summary:\n")

print(f"🔹 Faithfulness:       {mean(ragas_results['faithfulness']):.4f}")
print(f"🔹 Answer Relevancy:   {mean(ragas_results['answer_relevancy']):.4f}")
print(f"🔹 ROUGE-L:            {rouge_results['rougeL']:.4f}")
bert_f1 = sum(bertscore_results["f1"]) / len(bertscore_results["f1"])
print(f"🔹 BERTScore (F1):     {bert_f1:.4f}")
