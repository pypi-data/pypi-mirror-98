import torch
import torch.nn as nn
import torch.nn.functional as F


class TransformerEncoder(nn.Module):
    def __init__(self,
                 in_out_channels,
                 num_heads,
                 hidden_channels_ffn=2048,
                 dropout_p=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(in_out_channels,
                                               num_heads,
                                               dropout=dropout_p)

        self.linear1 = nn.Linear(in_out_channels, hidden_channels_ffn)
        self.linear2 = nn.Linear(hidden_channels_ffn, in_out_channels)

        self.norm1 = nn.LayerNorm(in_out_channels)
        self.norm2 = nn.LayerNorm(in_out_channels)

        self.dropout = nn.Dropout(dropout_p)

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


class TransformerDecoder(nn.Module):
    def __init__(self,
                 in_out_channels,
                 num_heads,
                 hidden_channels_ffn=2048,
                 dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(in_out_channels,
                                               num_heads,
                                               dropout=dropout)
        self.multihead_attn = nn.MultiheadAttention(in_out_channels,
                                                    num_heads,
                                                    dropout=dropout)

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

        tgt2, enc_dec_align = self.multihead_attn(
            tgt,
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
                 num_layers, dropout_p):
        super().__init__()
        self.fft_layers = nn.ModuleList([
            TransformerEncoder(in_out_channels=in_out_channels,
                               num_heads=num_heads,
                               hidden_channels_ffn=hidden_channels_ffn,
                               dropout_p=dropout_p)
            for _ in range(num_layers)
        ])

    def forward(self, x, mask=None, g=None):
        """
        TODO: handle multi-speaker
        Shapes:
            x: [B, C, T]
            mask:  [B, 1, T] or [B, T]
        """
        if mask is not None and mask.ndim == 3:
            mask = mask.squeeze(1)
            # mask is negated, torch uses 1s and 0s reversely.
            mask = ~mask.bool()
        alignments = []
        # T x B X C
        x = x.transpose(0, 1).transpose(0, 2)
        for layer in self.fft_layers:
            x, align = layer(x, src_key_padding_mask=mask)
            alignments.append(align.unsqueeze(1))
        alignments = torch.cat(alignments, 1)
        return x.transpose(0, 2).transpose(0, 1)
