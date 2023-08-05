import torch
import torch.nn as nn
import torch.nn.functional as F


class TransformerEncoderLayer(nn.Module):
    def __init__(self,
                 in_out_channels,
                 num_heads,
                 hidden_channels_ffn=2048,
                 dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(in_out_channels, num_heads, dropout=dropout)

        self.linear1 = nn.Linear(in_out_channels, hidden_channels_ffn)
        self.linear2 = nn.Linear(hidden_channels_ffn, in_out_channels)

        self.norm1 = nn.LayerNorm(in_out_channels)
        self.norm2 = nn.LayerNorm(in_out_channels)

        self.dropout = nn.Dropout(dropout)

    def forward(self, src, src_mask=None, src_key_padding_mask=None):
        src2, enc_align = self.self_attn(src,
                                         src,
                                         src,
                                         attn_mask=src_mask,
                                         key_padding_mask=src_key_padding_mask)
        src = src + self.dropout(src2)
        src = self.norm1(src)

        src2 = self.linear2(self.dropout(F.relu(self.linear1(src))))
        src = src + self.dropout(src2)
        src = self.norm2(src)

        return src, enc_align


class TransformerDecoderLayer(nn.Module):
    def __init__(self,
                 in_out_channels,
                 num_heads,
                 hidden_channels_ffn=2048,
                 dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(in_out_channels, num_heads, dropout=dropout)
        self.multihead_attn = nn.MultiheadAttention(in_out_channels, num_heads, dropout=dropout)

        self.linear1 = nn.Linear(in_out_channels, hidden_channels_ffn)
        self.linear2 = nn.Linear(hidden_channels_ffn, in_out_channels)

        self.norm1 = nn.LayerNorm(in_out_channels)
        self.norm2 = nn.LayerNorm(in_out_channels)
        self.norm3 = nn.LayerNorm(in_out_channels)

        self.dropout = nn.Dropout(dropout)

    def forward(self,
                tgt,
                memory,
                tgt_mask=None,
                memory_mask=None,
                tgt_key_padding_mask=None,
                memory_key_padding_mask=None):
        tgt2, dec_align = self.self_attn(tgt,
                                         tgt,
                                         tgt,
                                         attn_mask=tgt_mask,
                                         key_padding_mask=tgt_key_padding_mask)
        tgt = tgt + self.dropout(tgt2)
        tgt = self.norm1(tgt)

        tgt2, enc_dec_align = self.multihead_attn(tgt,
                                                  memory,
                                                  memory,
                                                  attn_mask=memory_mask,
                                                  key_padding_mask=memory_key_padding_mask)
        tgt = tgt + self.dropout(tgt2)
        tgt = self.norm2(tgt)

        tgt2 = self.linear2(self.dropout(F.relu(self.linear1(tgt))))
        tgt = tgt + self.dropout(tgt2)
        tgt = self.norm3(tgt)

        return tgt, dec_align, enc_dec_align


class FFTransformersBlock(nn.Module):
    def __init__(self, in_out_channels, num_heads, hidden_channels_ffn,
                 num_layers):
        super().__init__()
        self.fft_layers = nn.ModuleList([
            TransformerEncoderLayer(in_out_channels=in_out_channels,
                                    num_heads=num_heads,
                                    hidden_channels_ffn=hidden_channels_ffn)
            for _ in range(num_layers)
        ])

    def forward(self, x, mask=None):
        # B, L, D -> B, L, D
        mask = 1 if mask is None else mask
        alignments = []
        x = x.transpose(0, 1)
        for layer in self.fft_layers:
            x, align = layer(x, src_key_padding_mask=mask)
            alignments.append(align.unsqueeze(1))
        alignments = torch.cat(alignments, 1)
        return x.transpose(0, 1), alignments


class PositionalEncoding(nn.Module):
    def __init__(self, channels, max_len=5000):
        super().__init__()
        self.register_buffer('pe', self._get_pe_matrix(channels, max_len))

    def forward(self, x):
        return x + self.pe[:x.size(0)].unsqueeze(1)

    def _get_pe_matrix(self, channels, max_len):
        pe = torch.zeros(max_len, channels)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.pow(10000, torch.arange(0, channels, 2).float() / channels)

        pe[:, 0::2] = torch.sin(position / div_term)
        pe[:, 1::2] = torch.cos(position / div_term)

        return pe


class EmbeddingWithPositionalEncoding(nn.Module):
    def __init__(self, num_chars, hidden_channels), dropout=0.1:
        super().__init__()
        # B, L -> B, L, D
        self.embed = nn.Embedding(num_chars, hidden_channels)
        self.pos_enc = PositionalEncoding(hidden_channels)
        self.dropout = nn.Dropout(dropout)

    def forward(self, text):
        B, L = text.size(0), text.size(1)
        x = self.embed(text).transpose(0,1)
        x += self.pos_enc.pe[:L].unsqueeze(1)
        x = self.dropout(x).transpose(0,1)
        return x