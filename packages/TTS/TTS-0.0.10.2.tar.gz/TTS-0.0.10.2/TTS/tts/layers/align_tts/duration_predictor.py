from torch import nn
from .transforms import FFTransformersBlock


class DurationPredictor(nn.Module):
    def __init__(self, in_channels, hidden_channels_ffn, num_heads):
        super().__init__()
        self.Prenet = Prenet(hp)
        self.FFT = FFTransformersBlock(in_channels, num_heads, hidden_channels_ffn, 2)
        self.linear = nn.Linear(in_channels, 1)

    def forward(self, text, text_lengths):
        # B, L -> B, L
        encoder_input = self.Prenet(text)
        x = self.FFT(encoder_input, text_lengths)[0]
        x = self.linear(x).squeeze(-1)
        return x
