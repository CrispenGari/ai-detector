import torch
from torch import nn

from api.models import device, stoi, labels_dict, PYTORCH_BILSTM_MODEL_PATH


class AIHumanBiLSTM(nn.Module):
    def __init__(
        self,
        vocab_size,
        embedding_size,
        hidden_size,
        output_size,
        num_layers,
        bidirectional,
        dropout,
        pad_index,
    ):
        super(AIHumanBiLSTM, self).__init__()
        self.embedding = nn.Sequential(
            nn.Embedding(vocab_size, embedding_size, padding_idx=pad_index)
        )

        self.lstm = nn.Sequential(
            nn.LSTM(
                embedding_size,
                hidden_size=hidden_size,
                bidirectional=bidirectional,
                num_layers=num_layers,
                dropout=dropout,
                batch_first=True,
            )
        )
        self.out = nn.Sequential(nn.Linear(hidden_size * 2, out_features=output_size))

    def forward(self, text, text_lengths):
        embedded = self.embedding(text)
        packed_embedded = nn.utils.rnn.pack_padded_sequence(
            embedded, text_lengths, batch_first=True, enforce_sorted=False
        )
        _, (hidden, _) = self.lstm(packed_embedded)
        if self.lstm[0].bidirectional:
            hidden = torch.cat([hidden[-1], hidden[-2]], dim=-1)
        else:
            hidden = hidden[-1]
        return self.out(hidden)


print(" ✅ LOADING PYTORCH bilstm MODEL!\n")

INPUT_DIM = len(stoi)
EMBEDDING_DIM = 300
HIDDEN_DIM = 256
OUTPUT_DIM = 1 if len(labels_dict) == 2 else len(labels_dict)
N_LAYERS = 2
BIDIRECTIONAL = True
DROPOUT = 0.5
PAD_IDX = stoi["[pad]"]

bilstm = AIHumanBiLSTM(
    INPUT_DIM,
    EMBEDDING_DIM,
    HIDDEN_DIM,
    OUTPUT_DIM,
    N_LAYERS,
    BIDIRECTIONAL,
    DROPOUT,
    PAD_IDX,
).to(device)


bilstm.load_state_dict(torch.load(PYTORCH_BILSTM_MODEL_PATH, map_location=device))

print(" ✅ LOADING PYTORCH bilstm MODEL DONE!\n")
