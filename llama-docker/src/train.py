import time
import torch
import psutil
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login

# Configure logging
log_file_path = "/app/src/resources.log"
logging.basicConfig(filename=log_file_path, filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to save the prompt and model response to the log file
def save_prompt_and_response(prompt, response):
    logging.info(f'Prompt: {prompt}')
    logging.info(f'Response: {response}')

# Function to log system resource usage
def log_resource_usage(start_time, prompt, response):
    end_time = time.time()
    duration = end_time - start_time
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    
    # Logging the resource usage and prompt
    logging.info(f"Time taken: {duration:.2f} seconds")
    logging.info(f"CPU Usage: {cpu_usage}%")
    logging.info(f"Memory Usage: {memory_usage}%")
    logging.info(f"Prompt: {prompt}")
    logging.info(f"Response: {response}")

# Load tokenizer and model
# def load_model():
#     login(token="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")
#     tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
#     model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct", low_cpu_mem_usage=True, torch_dtype=torch.float16)
#     return tokenizer, model

def load_model():
    login(token="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")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
    
    # Load the model with memory optimizations
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # Enable gradient checkpointing to save memory
    model.gradient_checkpointing_enable()
    
    return tokenizer, model


# Simulate some training code
def train_model(tokenizer, model, prompt="scope of datascience"):
    logging.info("Training started...")
    start_time = time.time()
    
    # Tokenize and generate response
    inputs = tokenizer(prompt, return_tensors="pt", max_length=128)  # Adjust max_length if needed
    
    # Disable gradient calculation to save memory during inference
    with torch.no_grad():
        for epoch in range(5):  # Simulate 5 epochs of training
            outputs = model(**inputs)
            response = tokenizer.decode(outputs.logits.argmax(dim=-1).squeeze())  # Extract response from outputs
            save_prompt_and_response(prompt, response)
            time.sleep(1)  # Simulate a step taking 1 second

    # Log resource usage after training
    log_resource_usage(start_time, prompt, response)
    logging.info("Training completed.")

if __name__ == "__main__":
    tokenizer, model = load_model()
    train_model(tokenizer, model)
