import time
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login

# Load tokenizer and model
login(token="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")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")

# Simulate some training code
def train_model():
    print("Training started...")
    for epoch in range(5):  # Simulate 5 epochs of training
        inputs = tokenizer("Sample input text", return_tensors="pt")
        outputs = model(**inputs)
        time.sleep(1)  # Simulate a step taking 1 second
    print("Training completed.")

if __name__ == "__main__":
    train_model()
