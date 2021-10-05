import codecs
import logging
import os
import pickle

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

import model.Constants as Constants
from dataset.dataset import MonoLingualData, collate_fn
from dataset.loader import load_vocab

logger = logging.getLogger()


class LanguageModel(nn.Module):
    def __init__(self, params, emb_size, hidden_size, ouput_size, dropout=0.1):
        super(LanguageModel, self).__init__()
        self.emb_size = emb_size
        self.hidden_size = hidden_size
        self.output_size = ouput_size
        self.dropout = dropout

        self.embedding = nn.Embedding(ouput_size, hidden_size)

        if params.us_pretrain_embedding:
            self.init_embedding(params)

        self.rnn = nn.LSTM(self.emb_size, self.hidden_size, num_layers=2, dropout=self.dropout, batch_first=True)
        self.dropout = nn.Dropout(self.dropout)

        self.proj = nn.Linear(hidden_size, self.output_size)

    def forward(self, input_seq, tgt_seq):
        input_seq = self.dropout(self.embedding(input_seq))
        out, hidden = self.rnn(input_seq, None)

        out = self.proj(self.dropout(out))
        loss_func = nn.CrossEntropyLoss(ignore_index=Constants.PAD)

        out = out.view(-1, out.size(-1))
        tgt_seq = tgt_seq.view(-1)

        loss = loss_func(out, tgt_seq)

        return loss

    def get_ppl_reward(self, input_seq):
        with torch.no_grad():
            input_seq = input_seq.to("cpu")
            tgt_seq = input_seq[:, 1:].contiguous()
            input_seq = input_seq[:, :-1].contiguous()

            mask = tgt_seq != Constants.PAD

            input_seq = self.embedding(input_seq)
            out, hidden = self.rnn(input_seq, None)

            out = self.proj(out)
            log_prob = F.log_softmax(out, dim=-1)

            index = tgt_seq.unsqueeze(-1)
            select_log_prob = torch.gather(log_prob, -1, index).squeeze(-1) * mask.float()
            ppl_reward = torch.exp(select_log_prob.sum(dim=-1) / select_log_prob.size(-1))

        return ppl_reward.cpu().numpy()

    def init_embedding(self, args):
        logger.info("init LM embeddings with pretrained vector")
        pre_train_path = args.embedding_path
        weight_file = codecs.open(pre_train_path, mode='rb')
        emb_weight = pickle.load(weight_file)

        self.embedding = nn.Embedding.from_pretrained(emb_weight, freeze=False)


def load_mono_data(params, vocab):
    path = params.data_path
    assert os.path.isfile(path), path
    with codecs.open(path) as f:
        read_file = f.readlines()
        raw_data = [sent.strip() for sent in read_file]

        lm_loader = DataLoader(
            dataset=MonoLingualData(
                params=params,
                mono_data=raw_data,
                word2index=vocab,
                max_len=params.len_max_seq,
                frequent_word_list=None,
                ppdb_rules=None,
                data_mode=None,
                train_mode='otf'
            ),
            batch_size=params.batch_size,
            shuffle=True,
            collate_fn=collate_fn,
        )
        logger.info("Loaded mono data:", lm_loader)
        return lm_loader


def get_iterator(data_loader):
    data_iter = data_loader.__iter__()
    return data_iter


def get_batch(iterator):
    try:
        batch = iterator.next()
    except StopIteration:
        iterator = get_iterator(load_mono_data(params, word2index))
        batch = iterator.next()
    return batch


def lm_step(lm, lm_optimizer, iterator):
    lm.train()
    batch = get_batch(iterator)
    # print(batch)
    input_seq, input_pos = map(lambda x: x.to(Constants.device), batch)
    tgt_seq = input_seq[:, 1:].contiguous()
    input_seq = input_seq[:, :-1].contiguous()

    loss = lm(input_seq, tgt_seq)
    # print(loss)
    lm_optimizer.zero_grad()
    loss.backward()
    lm_optimizer.step()
    return loss


class params:
    us_pretrain_embedding = True
    data_path = "data/nonpara/comp_dev.txt"
    embedding_path = "resource/embedding.pkl"
    stoplist_path = "resource/stop.list"
    batch_size = 5
    len_max_seq = 120
    vocab_path = "data/vocab.list"
    steps = 2005
    lr = 0.0001
    hidden_size = 2

    class args:
        embedding_path = "resource/embedding.pkl"


if __name__ == '__main__':
    lm = LanguageModel(params, emb_size=512, hidden_size=params.hidden_size, ouput_size=30995)
    lm_optimizer = torch.optim.Adam(lm.parameters(), lr=params.lr, betas=(0.5, 0.999))
    word2index, index2word = load_vocab(params)
    # print(word2index)
    iterator = get_iterator(load_mono_data(params, word2index))
    for i in range(params.steps):
        loss_step = lm_step(lm=lm, lm_optimizer=lm_optimizer, iterator=iterator)
        if i % 100 == 0:
            logger.info(loss_step.item())
    torch.save(lm, open("LM.pkl", "wb"))
