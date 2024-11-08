import torch
import os
import json
import re
import spacy
from nltk.corpus import stopwords

# torch device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Model name
MODEL_NAME = "lstm.pt"

this =  os.path.dirname(__file__)

# Model paths
PYTORCH_BILSTM_MODEL_PATH = os.path.join(this, f"static/{MODEL_NAME}")


eng_stopwords = stopwords.words("english")

# Tokenizer
print(" ✅ LOADING TOKENIZER FROM SPACY(en_core_web_sm)!\n")
spacy_en = spacy.load('en_core_web_sm')
print(" ✅ LOADING TOKENIZERS DONE!\n")

def tokenize_en(sent: str) -> list:
    return [tok.text for tok in spacy_en.tokenizer(sent)]


UNKNOWN_TOKEN = "[unk]"

with open(
    os.path.join(this, "static/labels_dict.json"), "r"
) as reader:
    labels_dict = json.loads(reader.read())

with open(os.path.join(this, "static/vocab.json"), "r") as reader:
    stoi = json.loads(reader.read())


def clean_sentence(sent: str, lower: bool = True) -> str:
    sent = sent.lower() if lower else sent
    sent = re.sub(r"(@|#)([A-Za-z0-9]+)", " ", sent)
    sent = re.sub(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", " ", sent
    )
    sent = re.sub(r"https?\S+", " ", sent, flags=re.MULTILINE)  # removing url's
    sent = re.sub(r"\d", " ", sent)  # removing none word characters
    sent = re.sub(r"[^\w\s\']", " ", sent)
    sent = re.sub(r"\s+", " ", sent).strip()  # remove more than one space
    return sent


def stopwords_remover(words: list[str]) -> list[str]:
    return [word for word in words if word not in eng_stopwords]


def text_pipeline(x: str):
    values = list()
    x = clean_sentence(x)
    tokens = tokenize_en(x)
    tokens = stopwords_remover(tokens)
    for token in tokens:
        try:
            v = stoi[token]
        except KeyError:
            v = stoi[UNKNOWN_TOKEN]
        values.append(v)
    return values


def inference_preprocess_text(text, max_len=300, padding="pre"):
    assert (
        padding == "pre" or padding == "post"
    ), "the padding can be either pre or post"
    text_holder = torch.zeros(
        max_len, dtype=torch.int32
    )  # fixed size tensor of max_len with  = 0
    processed_text = torch.tensor(text_pipeline(text), dtype=torch.int32)
    pos = min(max_len, len(processed_text))
    if padding == "pre":
        text_holder[:pos] = processed_text[:pos]
    else:
        text_holder[-pos:] = processed_text[-pos:]
    text_list = text_holder.unsqueeze(dim=0)
    return text_list


classes = list(labels_dict.keys())


def predict_ai(model, sentence, device):
    model.eval()
    with torch.no_grad():
        tensor = inference_preprocess_text(sentence).to(device)
        length = torch.tensor([len(t) for t in tensor])
        prob = torch.sigmoid(model(tensor, length).squeeze(0)).cpu().item()
        prediction = 1 if prob >= 0.5 else 0
        class_name = classes[prediction]
        confidence = prob if prediction == 1 else 1 - prob
        pred_data = [
            ["class_id", prediction],
            ["class_name", class_name],
            ["probability", round(float(confidence), 3)],
        ]
        return dict(pred_data)
