from ..multi_head_attention.model import MultiHeadAttention
import tensorflow as tf


class MultiHeadAttentionLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, rate=0.1):
        super().__init__()

        self.mha = MultiHeadAttention(d_model, num_heads)
        self.dropout = tf.keras.layers.Dropout(rate)
        self.layernorm = tf.keras.layers.LayerNormalization(epsilon=1e-6)

    def call(self, v, k, q, mask, training):
        attn, attn_weights_block = self.mha(
            v, k, q, mask
        )
        attn = self.dropout(attn, training=training)
        attn = self.layernorm(attn, training=training)
        return attn, attn_weights_block
