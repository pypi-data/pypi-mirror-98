from ..transformer.point_wise_feed_forward_network import PointWiseFeedForwardNetwork
from .multi_head_attention_layer import MultiHeadAttentionLayer
import tensorflow as tf


class ReversibleDecoderLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super().__init__()

        self.mha1 = MultiHeadAttentionLayer(d_model, num_heads, rate)
        self.mha2 = MultiHeadAttentionLayer(d_model, num_heads, rate)
        self.ffn = tf.keras.Sequential([
            PointWiseFeedForwardNetwork(d_model, dff),
            tf.keras.layers.Dropout(rate),
            tf.keras.layers.LayerNormalization(epsilon=1e-6),
        ])

    def call(self, left, right, enc_output, training, look_ahead_mask, padding_mask):
        # enc_output.shape == (batch_size, input_seq_len, d_model)

        # (batch_size, target_seq_len, d_model)
        attn1, attn_weights_block1 = self.mha1(
            left, left, left, look_ahead_mask, training
        )
        right = attn1 + right

        # (batch_size, target_seq_len, d_model)
        attn2, attn_weights_block2 = self.mha2(
            enc_output, enc_output, right, padding_mask, training
        )
        left = attn2 + left                             # (batch_size, target_seq_len, d_model)

        ffn_output = self.ffn(left, training=training)  # (batch_size, target_seq_len, d_model)
        right = ffn_output + right                      # (batch_size, target_seq_len, d_model)

        return left, right, attn_weights_block1, attn_weights_block2

    def backward_grads(self, y_left, y_right, dy_left, dy_right, enc_output, training, look_ahead_mask, padding_mask):
        with tf.GradientTape() as ffntape:
            ffntape.watch(y_left)
            ffnleft = self.ffn(y_left, training=training)

        grads_combined = ffntape.gradient(
            ffnleft, [y_left] + self.ffn.trainable_variables, output_gradients=dy_right
        )
        dffn = grads_combined[1:]
        dleft = dy_left + grads_combined[0]
        right = y_right - ffnleft

        with tf.GradientTape() as mha2tape:
            mha2tape.watch(right)
            mha2attn, attn_weights_block2 = self.mha2(
                enc_output, enc_output, right, padding_mask, training
            )

        grads_combined = mha2tape.gradient(
            [mha2attn, attn_weights_block2], [right] + self.mha2.trainable_variables, output_gradients=dleft
        )
        dmha2 = grads_combined[1:]
        dright = dy_right + grads_combined[0]
        left = y_left - mha2attn

        with tf.GradientTape() as mha1tape:
            mha1tape.watch(left)
            mha1attn, attn_weights_block1 = self.mha1(
                left, left, left, look_ahead_mask, training
            )

        grads_combined = mha1tape.gradient(
            [mha1attn, attn_weights_block1], [left] + self.mha1.trainable_variables, output_gradients=dright
        )
        dmha1 = grads_combined[1:]
        dleft = dleft + grads_combined[0]
        right = right - mha1attn

        grads = dmha1 + dmha2 + dffn

        return left, right, dleft, dright, grads


# 左右逆転
class ReversalReversibleDecoderLayer(ReversibleDecoderLayer):
    def call(self, left, right, enc_output, training, look_ahead_mask, padding_mask):
        # left, right を逆に
        right, left, attn_weights_block1, attn_weights_block2 = super().call(
            right, left, enc_output, training, look_ahead_mask, padding_mask
        )
        return left, right, attn_weights_block1, attn_weights_block2

    def backward_grads(self, y_left, y_right, dy_left, dy_right, enc_output, training, look_ahead_mask, padding_mask):
        # left, right を逆に
        right, left, dright, dleft, grads = super().backward_grads(
            y_right, y_left, dy_right, dy_left, enc_output, training, look_ahead_mask, padding_mask
        )
        return left, right, dleft, dright, grads
