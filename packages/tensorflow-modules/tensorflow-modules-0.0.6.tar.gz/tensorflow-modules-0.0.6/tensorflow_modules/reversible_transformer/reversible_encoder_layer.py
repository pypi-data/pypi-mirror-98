from ..transformer.point_wise_feed_forward_network import PointWiseFeedForwardNetwork
from ..multi_head_attention.model import MultiHeadAttention
import tensorflow as tf


class ReversibleEncoderLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super().__init__()

        self.mha = MultiHeadAttention(d_model, num_heads)
        self.ffn = PointWiseFeedForwardNetwork(d_model, dff)

        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)

        self.dropout1 = tf.keras.layers.Dropout(rate)
        self.dropout2 = tf.keras.layers.Dropout(rate)

    def call(self, left, right, training, mask):
        attn_output, _ = self.mha(left, left, left, mask)   # (batch_size, input_seq_len, d_model)
        attn_output = self.dropout1(attn_output, training=training)
        right = self.layernorm1(right + attn_output)        # (batch_size, input_seq_len, d_model)

        ffn_output = self.ffn(right)                # (batch_size, input_seq_len, d_model)
        ffn_output = self.dropout2(ffn_output, training=training)
        left = self.layernorm2(left + ffn_output)   # (batch_size, input_seq_len, d_model)

        return left, right
