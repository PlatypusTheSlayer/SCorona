from transformers import XLNetForSequenceClassification, XLNetTokenizer
from keras.preprocessing.sequence import pad_sequences
import torch
import torch.nn.functional as F

MAX_LEN = 512
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = XLNetForSequenceClassification.from_pretrained('xlnet-base-cased', num_labels = 2)
model.load_state_dict(torch.load('xlnet_model.bin'))
tokenizer = XLNetTokenizer.from_pretrained('xlnet-base-cased')
model = model.to(device)
class_names = ['negative', 'positive']

def predict_sentiment(text):
    review_text = text

    encoded_review = tokenizer.encode_plus(
      review_text,
      max_length=MAX_LEN,
      add_special_tokens=True,
      return_token_type_ids=False,
      pad_to_max_length=False,
      return_attention_mask=True,
      return_tensors='pt',
      truncation=True
    )

    input_ids = pad_sequences(encoded_review['input_ids'], maxlen=MAX_LEN, dtype=torch.Tensor ,truncating="post",padding="post")
    input_ids = input_ids.astype(dtype = 'int64')
    input_ids = torch.tensor(input_ids) 

    attention_mask = pad_sequences(encoded_review['attention_mask'], maxlen=MAX_LEN, dtype=torch.Tensor ,truncating="post",padding="post")
    attention_mask = attention_mask.astype(dtype = 'int64')
    attention_mask = torch.tensor(attention_mask) 

    input_ids = input_ids.reshape(1,512).to(device)
    attention_mask = attention_mask.to(device)

    outputs = model(input_ids=input_ids, attention_mask=attention_mask)

    outputs = outputs[0][0].cpu().detach()

    probs = F.softmax(outputs, dim=-1).cpu().detach().numpy().tolist()
    _, prediction = torch.max(outputs, dim =-1)

    return class_names[prediction]

if __name__ == "__main__":
    predict_sentiment("pupka")