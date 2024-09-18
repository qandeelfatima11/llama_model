import time
import torch
import psutil
import logging
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login

# Configure logging
log_file_path = "/app/src/resources.log"
logging.basicConfig(filename=log_file_path, filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s')

def save_prompt_and_response(prompt, response):
    logging.info(f'Prompt: {prompt}')
    logging.info(f'Response: {response}')

def log_resource_usage(start_time, prompt, response):
    end_time = time.time()
    duration = end_time - start_time
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    
    logging.info(f"Time taken: {duration:.2f} seconds")
    logging.info(f"CPU Usage: {cpu_usage}%")
    logging.info(f"Memory Usage: {memory_usage}%")
    logging.info(f"Prompt: {prompt}")
    logging.info(f"Response: {response}")

def load_model():
    login(token="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")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
    
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        low_cpu_mem_usage=True,
        torch_dtype=torch.float32,
        device_map="auto"
    )
    
    return tokenizer, model

def pin_cpu_cores(cores):
    pid = os.getpid()
    os.sched_setaffinity(pid, cores)
    logging.info(f"Process {pid} pinned to CPU cores: {cores}")

def train_model(tokenizer, model, prompt="resources for diffusion models"):
    logging.info("\nTraining started...")
    start_time = time.time()
    
    # Pin the process to specific CPU cores (e.g., cores 0 and 1)
    cores = [0]
    pin_cpu_cores(cores)
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=64, truncation=True)  
    
    with torch.no_grad():
        for epoch in range(1):  # Reduced to 1 epoch
            outputs = model(**inputs)
            response = tokenizer.decode(outputs.logits.argmax(dim=-1).squeeze())
            save_prompt_and_response(prompt, response)
            time.sleep(1)  # Simulate a step taking 1 second

    log_resource_usage(start_time, prompt, response)
    logging.info("Training completed.\n")

if __name__ == "__main__":
    tokenizer, model = load_model()
    train_model(tokenizer, model)
