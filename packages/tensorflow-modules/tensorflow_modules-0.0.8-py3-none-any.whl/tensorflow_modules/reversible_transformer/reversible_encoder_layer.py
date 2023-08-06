from ..transformer.point_wise_feed_forward_network import PointWiseFeedForwardNetwork
from .multi_head_attention_layer import MultiHeadAttentionLayer
import tensorflow as tf


class ReversibleEncoderLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super().__init__()

        self.mha = MultiHeadAttentionLayer(d_model, num_heads, rate)
        self.ffn = tf.keras.Sequential([
            PointWiseFeedForwardNetwork(d_model, dff),
            tf.keras.layers.Dropout(rate),
            tf.keras.layers.LayerNormalization(epsilon=1e-6),
        ])

    def call(self, left, right, training, mask):
        attn_output, attn_weights_block = self.mha(left, left, left, mask, training)
        right = attn_output + right     # (batch_size, input_seq_len, d_model)
        left = self.ffn(right, training=training) + left   # (batch_size, input_seq_len, d_model)

        return left, right, attn_weights_block

    def backward_grads(self, y_left, y_right, dy_left, dy_right, training, mask):
        with tf.GradientTape() as ffntape:
            ffntape.watch(y_right)
            ffnright = self.ffn(y_right, training=training)

        grads_combined = ffntape.gradient(
            ffnright, [y_right] + self.ffn.trainable_variables, output_gradients=dy_left
        )
        dffn = grads_combined[1:]
        dright = dy_right + grads_combined[0]
        left = y_left - ffnright

        with tf.GradientTape() as mhatape:
            mhatape.watch(left)
            mhaattn, attn_weights_block = self.mha(
                left, left, left, mask, training
            )

        grads_combined = mhatape.gradient(
            [mhaattn, attn_weights_block], [left] + self.mha.trainable_variables, output_gradients=dright
        )
        dmha = grads_combined[1:]
        dleft = dy_left + grads_combined[0]
        right = y_right - mhaattn

        grads = dmha + dffn

        return left, right, dleft, dright, grads
