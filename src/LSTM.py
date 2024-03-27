import torch.nn as nn
import torch

from torchtext import data
from torchtext import vocab
from tqdm import tqdm


class Linear(nn.Module):
    def __init__(self, in_features, out_features):
        super(Linear, self).__init__()

        self.linear = nn.Linear(in_features=in_features,
                                out_features=out_features)
        self.init_params()

    def init_params(self):
        nn.init.kaiming_normal_(self.linear.weight)
        nn.init.constant_(self.linear.bias, 0)

    def forward(self, x):
        x = self.linear(x)
        return x


class LSTM(nn.Module):

    def __init__(self, input_size, hidden_size, num_layers, bidirectional, dropout):
        """
        Args:
            input_size: x 的特征维度
            hidden_size: 隐层的特征维度
            num_layers: LSTM 层数
        """
        super(LSTM, self).__init__()

        self.rnn = nn.LSTM(
            input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, bidirectional=bidirectional, dropout=dropout
        )

        self.init_params()

    def init_params(self):
        for i in range(self.rnn.num_layers):
            nn.init.orthogonal_(getattr(self.rnn, 'weight_hh_l{}'.format(i)))
            nn.init.kaiming_normal_(getattr(self.rnn, 'weight_ih_l{}'.format(i)))
            nn.init.constant_(getattr(self.rnn, 'bias_hh_l{}'.format(i)), val=0)
            nn.init.constant_(getattr(self.rnn, 'bias_ih_l{}'.format(i)), val=0)
            getattr(self.rnn, 'bias_hh_l{}'.format(i)).chunk(4)[1].fill_(1)

            if self.rnn.bidirectional:
                nn.init.orthogonal_(
                    getattr(self.rnn, 'weight_hh_l{}_reverse'.format(i)))
                nn.init.kaiming_normal_(
                    getattr(self.rnn, 'weight_ih_l{}_reverse'.format(i)))
                nn.init.constant_(
                    getattr(self.rnn, 'bias_hh_l{}_reverse'.format(i)), val=0)
                nn.init.constant_(
                    getattr(self.rnn, 'bias_ih_l{}_reverse'.format(i)), val=0)
                getattr(self.rnn, 'bias_hh_l{}_reverse'.format(i)).chunk(4)[1].fill_(1)

    def forward(self, x, lengths):
        # x: [seq_len, batch_size, input_size]
        # lengths: [batch_size]
        packed_x = nn.utils.rnn.pack_padded_sequence(x, lengths)

        # packed_x， packed_output: PackedSequence 对象
        # hidden: [num_layers * bidirectional, batch_size, hidden_size]
        # cell: [num_layers * bidirectional, batch_size, hidden_size]
        # Note: hidden 作为每个时间步的输出，cell 作为细胞状态。在相邻的时间步之间，cell 的值一般变化不大，但
        #              hidden 的差别一般会变化很大。
        packed_output, (hidden, cell) = self.rnn(packed_x)

        # output: [max_seq_len, batch_size, hidden_size * 2]
        # output_lengths: [batch_size]
        # 这里的 output 作为接下来全连接层的输入
        output, output_lengths = nn.utils.rnn.pad_packed_sequence(packed_output)

        return hidden, output


class TextRNN(nn.Module):

    def __init__(self, embedding_dim, output_dim, hidden_size, num_layers, bidirectional, dropout,
                 pretrained_embeddings):
        super(TextRNN, self).__init__()

        self.embedding = nn.Embedding.from_pretrained(
            pretrained_embeddings, freeze=False)
        self.rnn = LSTM(embedding_dim, hidden_size, num_layers, bidirectional, dropout)

        self.fc = Linear(hidden_size * 2, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        text, text_lengths = x
        # text: [sent len, batch size]
        embedded = self.dropout(self.embedding(text))
        # embedded: [sent len, batch size, emb dim]

        hidden, outputs = self.rnn(embedded, text_lengths)

        hidden = self.dropout(
            torch.cat((hidden[-2, :, :], hidden[-1, :, :]), dim=1))  # 连接最后一层的双向输出

        return self.fc(hidden)


if __name__ == '__main__':
    embedding_file = '/home/jason/Desktop/data/embeddings/glove/glove.840B.300d.txt'
    path = '/home/jason/Desktop/data/SST-2/'

    cache_dir = '.cache/'
    batch_size = 6
    vectors = vocab.Vectors(embedding_file, cache_dir)

    text_field = data.Field(tokenize='spacy',
                            lower=True,
                            include_lengths=True,
                            fix_length=5)
    label_field = data.LabelField(dtype=torch.long)

    train, dev, test = data.TabularDataset.splits(path=path,
                                                  train='train.tsv',
                                                  validation='dev.tsv',
                                                  test='test.tsv',
                                                  format='tsv',
                                                  skip_header=True,
                                                  fields=[('text', text_field), ('label', label_field)])

    text_field.build_vocab(train,
                           dev,
                           test,
                           max_size=25000,
                           vectors=vectors,
                           unk_init=torch.Tensor.normal_)
    label_field.build_vocab(train, dev, test)

    pretrained_embeddings = text_field.vocab.vectors
    labels = label_field.vocab.vectors

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    train_iter, dev_iter, test_iter = data.BucketIterator.splits((train, dev, test),
                                                                 batch_sizes=(batch_size, len(dev), len(test)),
                                                                 sort_key=lambda x: len(x.text),
                                                                 sort_within_batch=True,
                                                                 repeat=False,
                                                                 shuffle=True,
                                                                 device=device
                                                                )

    model = TextRNN(300, 2, 200, 2, True, 0.4, pretrained_embeddings)

    for step, batch in enumerate(tqdm(train_iter, desc="Iteration")):
        logits = model(batch.text)
        break
