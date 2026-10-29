import torch
import torch.nn as nn
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 1. Load the dataset
with open('chat_data.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 2. Extract unique characters & mappings
chars = sorted(list(set(text)))
vocab_size = len(chars)

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

encode = lambda s: [stoi.get(c, 0) for c in s]
decode = lambda l: ''.join([itos[i] for i in l])

data = torch.tensor(encode(text), dtype=torch.long)

# 3. Model Hyperparameters
n_embd = 32
hidden_size = 64
batch_size = 16
block_size = 16
max_iters = 1200

# RNN Model Definition
class TinyAngryBot(nn.Module):
    def __init__(self, vocab_size, n_embd, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, n_embd)
        self.rnn = nn.RNN(n_embd, hidden_size, batch_first=True)
        self.linear = nn.Linear(hidden_size, vocab_size)

    def forward(self, idx, hidden=None):
        emb = self.embedding(idx)
        out, hidden = self.rnn(emb, hidden)
        logits = self.linear(out)
        return logits, hidden

    def generate(self, idx, max_new_tokens):
        hidden = None
        if idx.shape[1] > 1:
            _, hidden = self(idx[:, :-1])
            logits, hidden = self(idx[:, -1:], hidden)
        else:
            logits, hidden = self(idx)

        for _ in range(max_new_tokens):
            logits = logits[:, -1, :]
            probs = nn.functional.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)
            logits, hidden = self(idx_next, hidden)
            
        return idx

# Initialize & Train Model on Startup
model = TinyAngryBot(vocab_size, n_embd, hidden_size)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-2)

print("Training the angry English bot...")
for iter in range(max_iters):
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])

    logits, _ = model(x)
    B, T, C = logits.shape
    logits = logits.view(B * T, C)
    targets = y.view(B * T)

    loss = criterion(logits, targets)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

print("Training complete! Starting Web Server...")

# --- Web Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    if not user_msg:
        return jsonify({'reply': 'Say something, you dumbass!'})

    input_ids = encode(user_msg.lower())
    if not input_ids:
        input_ids = [0]

    input_tensor = torch.tensor(input_ids, dtype=torch.long).unsqueeze(0)
    input_len = input_tensor.shape[1]

    generated_ids = model.generate(input_tensor, max_new_tokens=70)[0].tolist()
    new_token_ids = generated_ids[input_len:]
    bot_reply = decode(new_token_ids)

    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True, port=5000)