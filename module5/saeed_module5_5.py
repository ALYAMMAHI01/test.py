import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load pre-trained model and tokenizer
model_name = "bert-base-uncased"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Set the maximum context window to 4096 tokens (you can adjust this value as needed)
max_context_window = 4096

# Define a function to generate text with increased context
def generate_text(context, max_context):
    inputs = tokenizer(context, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=max_context, no_repeat_ngram_size=3, do_sample=True, temperature=1.2)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage
context = "The quick brown fox jumps over the lazy dog."
max_context = 512
print(generate_text(context, max_context))

# To change the temperature of the LLM, you need to adjust the `temperature` parameter when calling the `model.generate()` method. The `temperature` control is not directly available as a model attribute; it's
# primarily controlled through the Hugging Face API.
#
# However, we can modify our function to accept an additional argument for temperature and then adjust the output accordingly:
#
def generate_text(context, max_context, temperature):
    inputs = tokenizer(context, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=max_context, no_repeat_ngram_size=3, do_sample=True, temperature=temperature)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage
context = "The quick brown fox jumps over the lazy dog."
max_context = 512
print(generate_text(context, max_context, 1.2))
