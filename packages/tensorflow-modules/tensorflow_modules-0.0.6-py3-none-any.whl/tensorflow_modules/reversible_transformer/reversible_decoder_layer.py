from ..transformer.point_wise_feed_forward_network import PointWiseFeedForwardNetwork
from ..multi_head_attention.model import MultiHeadAttention
import tensorflow as tf


class ReversibleDecoderLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super().__init__()

        self.mha1 = MultiHeadAttention(d_model, num_heads)
        self.mha2 = MultiHeadAttention(d_model, num_heads)

        self.ffn = PointWiseFeedForwardNetwork(d_model, dff)

        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm3 = tf.keras.layers.LayerNormalization(epsilon=1e-6)

        self.dropout1 = tf.keras.layers.Dropout(rate)
        self.dropout2 = tf.keras.layers.Dropout(rate)
        self.dropout3 = tf.keras.layers.Dropout(rate)

    def call(self, left, right, enc_output, training, look_ahead_mask, padding_mask):
        # enc_output.shape == (batch_size, input_seq_len, d_model)

        # (batch_size, target_seq_len, d_model)
        attn1, attn_weights_block1 = self.mha1(
            left, left, left, look_ahead_mask
        )
        attn1 = self.dropout1(attn1, training=training)
        right = self.layernorm1(attn1 + right)

        # (batch_size, target_seq_len, d_model)
        attn2, attn_weights_block2 = self.mha2(
            enc_output, enc_output, right, padding_mask
        )
        attn2 = self.dropout2(attn2, training=training)
        left = self.layernorm2(attn2 + left)            # (batch_size, target_seq_len, d_model)

        ffn_output = self.ffn(left)                     # (batch_size, target_seq_len, d_model)
        ffn_output = self.dropout3(ffn_output, training=training)
        right = self.layernorm3(ffn_output + right)     # (batch_size, target_seq_len, d_model)

        return left, right, attn_weights_block1, attn_weights_block2


# 左右逆転
class ReversalReversibleDecoderLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super().__init__()

        self.mha1 = MultiHeadAttention(d_model, num_heads)
        self.mha2 = MultiHeadAttention(d_model, num_heads)

        self.ffn = PointWiseFeedForwardNetwork(d_model, dff)

        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm3 = tf.keras.layers.LayerNormalization(epsilon=1e-6)

        self.dropout1 = tf.keras.layers.Dropout(rate)
        self.dropout2 = tf.keras.layers.Dropout(rate)
        self.dropout3 = tf.keras.layers.Dropout(rate)

    def call(self, left, right, enc_output, training, look_ahead_mask, padding_mask):
        # enc_output.shape == (batch_size, input_seq_len, d_model)

        # (batch_size, target_seq_len, d_model)
        attn1, attn_weights_block1 = self.mha1(
            right, right, right, look_ahead_mask
        )
        attn1 = self.dropout1(attn1, training=training)
        left = self.layernorm1(attn1 + left)

        # (batch_size, target_seq_len, d_model)
        attn2, attn_weights_block2 = self.mha2(
            enc_output, enc_output, left, padding_mask
        )
        attn2 = self.dropout2(attn2, training=training)
        right = self.layernorm2(attn2 + right)      # (batch_size, target_seq_len, d_model)

        ffn_output = self.ffn(right)                # (batch_size, target_seq_len, d_model)
        ffn_output = self.dropout3(ffn_output, training=training)
        left = self.layernorm3(ffn_output + left)   # (batch_size, target_seq_len, d_model)

        return left, right, attn_weights_block1, attn_weights_block2
