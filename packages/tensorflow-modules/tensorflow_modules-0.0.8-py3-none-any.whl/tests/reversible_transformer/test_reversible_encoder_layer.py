from tensorflow_modules import *
import tensorflow as tf
import unittest


class TestReversibleDecoderLayer(unittest.TestCase):
    d_model = 512
    num_heads = 8
    dff = 2048
    model = ReversibleEncoderLayer(d_model, num_heads, dff)

    def test_dimension(self):
        left = tf.random.uniform([64, 43, 512])
        right = tf.random.uniform([64, 43, 512])

        left_out, right_out, attn = self.model(left, right, False, None)
        self.assertEqual([64, 43, 512], left_out.shape.as_list())
        self.assertEqual([64, 43, 512], right_out.shape.as_list())
        self.assertEqual([64, 8, 43, 43], attn.shape)

    def test_backward_grads(self):
        shape = [1, 1, 512]
        left = tf.random.normal(shape)
        right = tf.random.normal(shape)
        dleft = tf.random.normal(shape)
        dright = tf.random.normal(shape)

        with tf.GradientTape() as tape:
            tape.watch(left)
            tape.watch(right)
            left_out, right_out, attn_weights_block = self.model(
                left, right, False, None
            )

        # Compute true grads
        dleft_true, dright_true = tape.gradient([left_out, right_out], [left, right], output_gradients=[dleft, dright])

        # Compute grads from reconstruction
        left_back, right_back, dleft_back, dright_back, grads = self.model.backward_grads(
            left_out, right_out, dleft, dright, False, None
        )

        thres = 1e-6

        self.assertTrue(all(tf.reshape(abs(dleft_true - dleft_back), [-1]) < thres))
        self.assertTrue(all(tf.reshape(abs(dright_true - dright_back), [-1]) < thres))
        self.assertTrue(all(tf.reshape(abs(left - left_back), [-1]) < thres))
        self.assertTrue(all(tf.reshape(abs(right - right_back), [-1]) < thres))

        optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
        optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
