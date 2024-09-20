

from transformers import AutoModel, AutoTokenizer
model_dir = './local_model_directory'  # Path to your local directory
model = AutoModel.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
inputs = tokenizer("I am feeling bad nowadays", return_tensors="pt")
outputs = model(**inputs)
if __name__=='__main__':
    print(outputs.last_hidden_state)
