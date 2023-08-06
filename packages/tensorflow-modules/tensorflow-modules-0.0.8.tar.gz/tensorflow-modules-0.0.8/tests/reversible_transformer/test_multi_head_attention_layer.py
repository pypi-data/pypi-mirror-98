from tensorflow_modules import *
import tensorflow as tf
import unittest


class TestMultiHeadAttentionLayer(unittest.TestCase):
    d_model = 512
    num_heads = 8
    dff = 2048

    def test_dimension(self):
        model = MultiHeadAttentionLayer(self.d_model, self.num_heads)
        v = tf.random.uniform([64, 43, 512])
        q = tf.random.uniform([64, 43, 512])
        k = tf.random.uniform([64, 43, 512])

        attn, attn_weights_block = model(v, q, k, None, False)
        self.assertEqual([64, 43, 512], attn.shape)
        self.assertEqual([64, 8, 43, 43], attn_weights_block.shape)
