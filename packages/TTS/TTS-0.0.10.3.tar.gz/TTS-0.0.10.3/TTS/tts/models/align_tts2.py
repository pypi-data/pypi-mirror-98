import math
import torch
import torch.nn as nn
import torch.nn.functional as F

from TTS.tts.layers.glow_tts.monotonic_align import maximum_path, generate_path
from TTS.tts.utils.generic_utils import sequence_mask
from TTS.tts.layers.losses import AlignTTSLoss


class FFTransformer(nn.Module):
    def __init__(self,
                 in_out_channels,
                 num_heads,
                 hidden_channels_ffn=2048,
                 kernel_size_fft=3,
                 dropout_p=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(in_out_channels,
                                               num_heads,
                                               dropout=dropout_p)

        padding = (kernel_size_fft - 1) // 2
        self.conv1 = nn.Conv1d(in_out_channels, hidden_channels_ffn,  kernel_size=kernel_size_fft, padding=padding)
        self.conv2 = nn.Conv1d(hidden_channels_ffn, in_out_channels,  kernel_size=kernel_size_fft, padding=padding)

        self.norm1 = nn.LayerNorm(in_out_channels)
        self.norm2 = nn.LayerNorm(in_out_channels)

        self.dropout = nn.Dropout(dropout_p)

    def forward(self, src, src_mask=None, src_key_padding_mask=None):
        """😦 ugly looking with all the transposing """
        src = src.permute(2, 0, 1)
        src2, enc_align = self.self_attn(src,
                                         src,
                                         src,
                                         attn_mask=src_mask,
                                         key_padding_mask=src_key_padding_mask)
        src = self.norm1(src + src2)
        # T x B x D -> B x D x T
        src = src.permute(1, 2, 0)
        src2 = self.conv2(F.relu(self.conv1(src)))
        src2 = self.dropout(src2)
        src = src + src2
        src = src.transpose(1, 2)
        src = self.norm2(src)
        src = src.transpose(1, 2)
        return src, enc_align


class FFTransformerBlock(nn.Module):
    def __init__(self, in_out_channels, num_heads, hidden_channels_ffn,
                 num_layers, dropout_p):
        super().__init__()
        self.fft_layers = nn.ModuleList([
            FFTransformer(in_out_channels=in_out_channels,
                          num_heads=num_heads,
                          hidden_channels_ffn=hidden_channels_ffn,
                          dropout_p=dropout_p) for _ in range(num_layers)
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
        for layer in self.fft_layers:
            x, align = layer(x, src_key_padding_mask=mask)
            alignments.append(align.unsqueeze(1))
        alignments = torch.cat(alignments, 1)
        return x


class FFTransformerDecoder(nn.Module):
    """Decoder with FeedForwardTransformer.

    Args:
        in_channels (int): number of input channels.
        out_channels (int): number of output channels.
        hidden_channels (int): number of hidden channels including Transformer layers.
        params (dict): dictionary for residual convolutional blocks.
    """
    def __init__(self, in_channels, out_channels, num_heads, hidden_channels_ffn, num_layers, dropout_p):

        super().__init__()
        self.transformer_block = FFTransformerBlock(in_channels, num_heads, hidden_channels_ffn, num_layers, dropout_p)
        self.postnet = nn.Conv1d(in_channels, out_channels, 1)

    def forward(self, x, x_mask=None, g=None):  # pylint: disable=unused-argument
        # TODO: handle multi-speaker
        o = self.transformer_block(x) * x_mask
        o = self.postnet(o)*  x_mask
        return o


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding for non-recurrent neural networks.
    Implementation based on "Attention Is All You Need"
    Args:
       channels (int): embedding size
       dropout (float): dropout parameter
    """
    def __init__(self, channels, dropout_p=0.0, max_len=5000):
        super().__init__()
        if channels % 2 != 0:
            raise ValueError(
                "Cannot use sin/cos positional encoding with "
                "odd channels (got channels={:d})".format(channels))
        pe = torch.zeros(max_len, channels)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.pow(10000,
                             torch.arange(0, channels, 2).float() / channels)
        pe[:, 0::2] = torch.sin(position.float() * div_term)
        pe[:, 1::2] = torch.cos(position.float() * div_term)
        pe = pe.unsqueeze(0).transpose(1, 2)
        self.register_buffer('pe', pe)
        if dropout_p > 0:
            self.dropout = nn.Dropout(p=dropout_p)
        self.channels = channels

    def forward(self, x, mask=None, first_idx=None, last_idx=None):
        """
        Shapes:
            x: [B, C, T]
            mask: [B, 1, T]
            first_idx: int
            last_idx: int
        """

        x = x * math.sqrt(self.channels)
        if first_idx is None:
            if self.pe.size(2) < x.size(2):
                raise RuntimeError(
                    f"Sequence is {x.size(2)} but PositionalEncoding is"
                    f" limited to {self.pe.size(2)}. See max_len argument.")
            if mask is not None:
                pos_enc = (self.pe[:, :, :x.size(2)] * mask)
            else:
                pos_enc = self.pe[:, :, :x.size(2)]
            x = x + pos_enc
        else:
            x = x + self.pe[:, :, first_idx:last_idx]
        if hasattr(self, 'dropout'):
            x = self.dropout(x)
        return x


class MDNBlock(nn.Module):
    """Mixture of Density Network implementation
    https://arxiv.org/pdf/2003.01950.pdf
    """
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.out_channels = out_channels
        self.conv1 = nn.Conv1d(in_channels, in_channels, 1)
        self.norm = nn.LayerNorm(in_channels)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.1)
        self.conv2 = nn.Conv1d(in_channels, out_channels, 1)

    def forward(self, x):
        o = self.conv1(x)
        o = o.transpose(1, 2)
        o = self.norm(o)
        o = o.transpose(1, 2)
        o = self.relu(o)
        o = self.dropout(o)
        mu_sigma = self.conv2(o)
        # TODO: check this sigmoid
        # mu = torch.sigmoid(mu_sigma[:, :self.out_channels//2, :])
        mu = mu_sigma[:, :self.out_channels//2, :]
        log_sigma = mu_sigma[:, self.out_channels//2:, :]
        return mu, log_sigma


class DurationPredictor(nn.Module):
    def __init__(self, num_chars, hidden_channels, hidden_channels_ffn, num_heads):
        super().__init__()
        self.embed = nn.Embedding(num_chars, hidden_channels)
        self.pos_enc = PositionalEncoding(hidden_channels, dropout_p=0.1)
        self.fft_block = FFTransformerBlock(hidden_channels, num_heads, hidden_channels_ffn, 2, 0.1)
        self.out_layer = nn.Conv1d(hidden_channels, 1, 1)

    def forward(self, text, text_lengths):
        # B, L -> B, L
        emb = self.embed(text)
        emb = self.pos_enc(emb.transpose(1, 2))
        x = self.fft_block(emb, text_lengths)
        x = self.out_layer(x).squeeze(-1)
        return x


class AlignTTS(nn.Module):
    """Speedy Speech model with Monotonic Alignment Search
    https://arxiv.org/abs/2008.03802
    https://arxiv.org/pdf/2005.11129.pdf

    Encoder -> DurationPredictor -> Decoder

    This model is able to achieve a reasonable performance with only
    ~3M model parameters and convolutional layers.

    This model requires precomputed phoneme durations to train a duration predictor. At inference
    it only uses the duration predictor to compute durations and expand encoder outputs respectively.

    Args:
        num_chars (int): number of unique input to characters
        out_channels (int): number of output tensor channels. It is equal to the expected spectrogram size.
        hidden_channels (int): number of channels in all the model layers.
        positional_encoding (bool, optional): enable/disable Positional encoding on encoder outputs. Defaults to True.
        length_scale (int, optional): coefficient to set the speech speed. <1 slower, >1 faster. Defaults to 1.
        encoder_type (str, optional): set the encoder type. Defaults to 'residual_conv_bn'.
        encoder_params (dict, optional): set encoder parameters depending on 'encoder_type'. Defaults to { "kernel_size": 4, "dilations": 4 * [1, 2, 4] + [1], "num_conv_blocks": 2, "num_res_blocks": 13 }.
        decoder_type (str, optional): decoder type. Defaults to 'residual_conv_bn'.
        decoder_params (dict, optional): set decoder parameters depending on 'decoder_type'. Defaults to { "kernel_size": 4, "dilations": 4 * [1, 2, 4, 8] + [1], "num_conv_blocks": 2, "num_res_blocks": 17 }.
        num_speakers (int, optional): number of speakers for multi-speaker training. Defaults to 0.
        external_c (bool, optional): enable external speaker embeddings. Defaults to False.
        c_in_channels (int, optional): number of channels in speaker embedding vectors. Defaults to 0.
    """
    # pylint: disable=dangerous-default-value

    def __init__(self,
                 num_chars,
                 out_channels,
                 hidden_channels=256,
                 hidden_channels_ffn=1024,
                 hidden_channels_dp=128,
                 num_heads=2,
                 num_transformer_layers=6,
                 dropout_p=0.1,
                 length_scale=1,
                 num_speakers=0,
                 external_c=False,
                 c_in_channels=0):

        super().__init__()
        self.length_scale = float(length_scale) if isinstance(
            length_scale, int) else length_scale
        self.emb = nn.Embedding(num_chars, hidden_channels)
        self.pos_encoder = PositionalEncoding(hidden_channels)
        self.encoder = FFTransformerBlock(hidden_channels, num_heads, hidden_channels_ffn, num_transformer_layers, dropout_p)
        self.decoder = FFTransformerDecoder(hidden_channels, out_channels, num_heads, hidden_channels_ffn, num_transformer_layers, dropout_p)
        self.duration_predictor = DurationPredictor(num_chars, hidden_channels_dp, hidden_channels_ffn=hidden_channels_ffn, num_heads=num_heads)

        self.mod_layer = nn.Conv1d(hidden_channels, hidden_channels, 1)
        self.mdn_block = MDNBlock(hidden_channels, 2*out_channels)

        if num_speakers > 1 and not external_c:
            # speaker embedding layer
            self.emb_g = nn.Embedding(num_speakers, c_in_channels)
            nn.init.uniform_(self.emb_g.weight, -0.1, 0.1)

        if c_in_channels > 0 and c_in_channels != hidden_channels:
            self.proj_g = nn.Conv1d(c_in_channels, hidden_channels, 1)

    def compute_log_probs(self, mu, log_sigma, y):
        '''Faster way to compute log probability'''
        scale = torch.exp(-2 * log_sigma)
        # [B, T_en, 1]
        logp1 = torch.sum(-0.5 * math.log(2 * math.pi) - log_sigma,
                            [1]).unsqueeze(-1)
        # [B, T_en, D] x [B, D, T_dec] = [B, T_en, T_dec]
        logp2 = torch.matmul(scale.transpose(1, 2), -0.5 * (y**2))
        # [B, T_en, D] x [B, D, T_dec] = [B, T_en, T_dec]
        logp3 = torch.matmul((mu * scale).transpose(1, 2), y)
        # [B, T_en, 1]
        logp4 = torch.sum(-0.5 * (mu**2) * scale,
                            [1]).unsqueeze(-1)
        # [B, T_en, T_dec]
        logp = logp1 + logp2 + logp3 + logp4
        return logp

    def compute_align_path(self, mu, log_sigma, y, x_mask, y_mask):
        # find the max alignment path
        attn_mask = torch.unsqueeze(x_mask, -1) * torch.unsqueeze(y_mask, 2)
        log_p = self.compute_log_probs(mu, log_sigma, y)
        # [B, T_en, T_dec]
        # align = self.viterbi(log_p, x_lengths, y_lengths)
        attn = maximum_path(log_p,
                            attn_mask.squeeze(1)).unsqueeze(1).detach()
        logp_max_path = None
        dr_mas = torch.sum(attn, -1)
        return dr_mas.squeeze(1), log_p

    def viterbi(self, log_prob_matrix, text_lengths, mel_lengths):
        B, L, T = log_prob_matrix.size()
        log_beta = log_prob_matrix.new_ones(B, L, T)*(-1e15)
        log_beta[:, 0, 0] = log_prob_matrix[:, 0, 0]

        for t in range(1, T):
            prev_step = torch.cat([log_beta[:, :, t-1:t], F.pad(log_beta[:, :, t-1:t], (0,0,1,-1), value=-1e15)], dim=-1).max(dim=-1)[0]
            log_beta[:, :, t] = prev_step+log_prob_matrix[:, :, t]

        curr_rows = text_lengths-1
        curr_cols = mel_lengths-1
        path = [curr_rows*1.0]
        for _ in range(T-1):
            is_go = log_beta[torch.arange(B), (curr_rows-1).to(torch.long), (curr_cols-1).to(torch.long)]\
                     > log_beta[torch.arange(B), (curr_rows).to(torch.long), (curr_cols-1).to(torch.long)]
            curr_rows = F.relu(curr_rows-1.0*is_go+1.0)-1.0
            curr_cols = F.relu(curr_cols-1+1.0)-1.0
            path.append(curr_rows*1.0)

        path.reverse()
        path = torch.stack(path, -1)

        indices = path.new_tensor(torch.arange(path.max()+1).view(1,1,-1)) # 1, 1, L
        align = 1.0*(path.new_tensor(indices==path.unsqueeze(-1))) # B, T, L

        for i in range(align.size(0)):
            pad= T-mel_lengths[i]
            align[i] = F.pad(align[i], (0,0,-pad,pad))

        return align.transpose(1,2)

    @staticmethod
    def convert_dr_to_align(dr, x_mask, y_mask):
        attn_mask = torch.unsqueeze(x_mask, -1) * torch.unsqueeze(y_mask, 2)
        attn = generate_path(dr, attn_mask.squeeze(1)).to(dr.dtype)
        return attn

    def expand_encoder_outputs(self, en, dr, x_mask, y_mask):
        """Generate attention alignment map from durations and
        expand encoder outputs

        Example:
            encoder output: [a,b,c,d]
            durations: [1, 3, 2, 1]

            expanded: [a, b, b, b, c, c, d]
            attention map: [[0, 0, 0, 0, 0, 0, 1],
                            [0, 0, 0, 0, 1, 1, 0],
                            [0, 1, 1, 1, 0, 0, 0],
                            [1, 0, 0, 0, 0, 0, 0]]
        """
        attn = self.convert_dr_to_align(dr, x_mask, y_mask)
        o_en_ex = torch.matmul(
            attn.squeeze(1).transpose(1, 2), en.transpose(1,
                                                          2)).transpose(1, 2)
        return o_en_ex, attn

    def format_durations(self, o_dr_log, x_mask):
        o_dr = (torch.exp(o_dr_log) - 1) * x_mask * self.length_scale
        o_dr[o_dr < 1] = 1.0
        o_dr = torch.round(o_dr)
        return o_dr

    @staticmethod
    def _concat_speaker_embedding(o_en, g):
        g_exp = g.expand(-1, -1, o_en.size(-1))  # [B, C, T_en]
        o_en = torch.cat([o_en, g_exp], 1)
        return o_en

    def _sum_speaker_embedding(self, x, g):
        # project g to decoder dim.
        if hasattr(self, 'proj_g'):
            g = self.proj_g(g)
        return x + g

    def _forward_encoder(self, x, x_lengths, g=None):
        if hasattr(self, 'emb_g'):
            g = nn.functional.normalize(self.emb_g(g))  # [B, C, 1]

        if g is not None:
            g = g.unsqueeze(-1)

        # [B, T, C]
        x_emb = self.emb(x)
        # [B, C, T]
        x_emb = torch.transpose(x_emb, 1, -1)

        # compute sequence masks
        x_mask = torch.unsqueeze(sequence_mask(x_lengths, x.shape[1]),
                                 1).to(x.dtype)

        # encoder pass
        o_en = self.encoder(x_emb, x_mask)

        # speaker conditioning for duration predictor
        if g is not None:
            o_en_dp = self._concat_speaker_embedding(o_en, g)
        else:
            o_en_dp = o_en
        return o_en, o_en_dp, x_mask, g

    def _forward_decoder(self, o_en, o_en_dp, dr, x_mask, y_lengths, g):
        y_mask = torch.unsqueeze(sequence_mask(y_lengths, None),
                                 1).to(o_en_dp.dtype)
        # expand o_en with durations
        o_en_ex, attn = self.expand_encoder_outputs(o_en, dr, x_mask, y_mask)
        # positional encoding
        if hasattr(self, 'pos_encoder'):
            o_en_ex = self.pos_encoder(o_en_ex, y_mask)
        # speaker embedding
        if g is not None:
            o_en_ex = self._sum_speaker_embedding(o_en_ex, g)
        # decoder pass
        o_de = self.decoder(o_en_ex, y_mask, g=g)
        return o_de, attn.transpose(1, 2)

    def _forward_mdn(self, o_en, y, y_lengths, x_mask):
        # MAS potentials and alignment
        mu, log_sigma = self.mdn_block(o_en)
        y_mask = torch.unsqueeze(sequence_mask(y_lengths, None), 1).to(o_en.dtype)
        dr_mas, logp = self.compute_align_path(mu, log_sigma, y, x_mask, y_mask)
        return dr_mas, mu, log_sigma, logp

    def forward(self, x, x_lengths, y, y_lengths, phase=None, g=None):  # pylint: disable=unused-argument
        """
        Shapes:
            x: [B, T_max]
            x_lengths: [B]
            y_lengths: [B]
            dr: [B, T_max]
            g: [B, C]
        """
        o_de, o_dr_log, dr_mas_log, attn, mu, log_sigma, logp = None, None, None, None, None, None, None
        if phase == 0:
            # train encoder and MDN
            o_en, o_en_dp, x_mask, g = self._forward_encoder(x, x_lengths, g)
            dr_mas, mu, log_sigma, logp = self._forward_mdn(o_en, y, y_lengths, x_mask)
            y_mask = torch.unsqueeze(sequence_mask(y_lengths, None),
                                 1).to(o_en_dp.dtype)
            attn = self.convert_dr_to_align(dr_mas, x_mask, y_mask)
        elif phase == 1:
            # train decoder
            o_en, o_en_dp, x_mask, g = self._forward_encoder(x, x_lengths, g)
            dr_mas, _, _, _ = self._forward_mdn(o_en, y, y_lengths, x_mask)
            o_de, attn = self._forward_decoder(o_en.detach(), o_en_dp.detach(), dr_mas.detach(), x_mask, y_lengths, g=g)
        elif phase == 2:
            # train the whole except duration predictor
            o_en, o_en_dp, x_mask, g = self._forward_encoder(x, x_lengths, g)
            dr_mas, mu, log_sigma, logp = self._forward_mdn(o_en, y, y_lengths, x_mask)
            o_de, attn = self._forward_decoder(o_en, o_en_dp, dr_mas, x_mask, y_lengths, g=g)
        elif phase == 3:
            # train duration predictor
            o_en, o_en_dp, x_mask, g = self._forward_encoder(x, x_lengths, g)
            o_dr_log = self.duration_predictor(x, x_mask)
            dr_mas, mu, log_sigma, logp = self._forward_mdn(o_en, y, y_lengths, x_mask)
            o_de, attn = self._forward_decoder(o_en, o_en_dp, dr_mas, x_mask, y_lengths, g=g)
            o_dr_log = o_dr_log.squeeze(1)
        else:
            o_en, o_en_dp, x_mask, g = self._forward_encoder(x, x_lengths, g)
            o_dr_log = self.duration_predictor(x, x_mask)
            dr_mas, mu, log_sigma, logp = self._forward_mdn(o_en, y, y_lengths, x_mask)
            o_de, attn = self._forward_decoder(o_en, o_en_dp, dr_mas, x_mask, y_lengths, g=g)
            o_dr_log = o_dr_log.squeeze(1)
        dr_mas_log = torch.log(1 + dr_mas).squeeze(1)
        return o_de, o_dr_log, dr_mas_log, attn, mu, log_sigma, logp

    def inference(self, x, x_lengths, g=None):  # pylint: disable=unused-argument
        """
        Shapes:
            x: [B, T_max]
            x_lengths: [B]
            g: [B, C]
        """
        # pad input to prevent dropping the last word
        x = torch.nn.functional.pad(x, pad=(0, 5), mode='constant', value=0)
        o_en, o_en_dp, x_mask, g = self._forward_encoder(x, x_lengths, g)
        o_dr_log = self.duration_predictor(x, x_mask)
        # duration predictor pass
        o_dr = self.format_durations(o_dr_log, x_mask).squeeze(1)
        y_lengths = o_dr.sum(1)
        o_de, attn = self._forward_decoder(o_en, o_en_dp, o_dr, x_mask, y_lengths, g=g)
        return o_de, attn

    def load_checkpoint(self, config, checkpoint_path, eval=False):  # pylint: disable=unused-argument, redefined-builtin
        state = torch.load(checkpoint_path, map_location=torch.device('cpu'))
        self.load_state_dict(state['model'])
        if eval:
            self.eval()
            assert not self.training