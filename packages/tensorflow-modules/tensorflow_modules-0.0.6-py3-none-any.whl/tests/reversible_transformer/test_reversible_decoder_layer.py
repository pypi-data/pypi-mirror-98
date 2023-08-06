from tensorflow_modules import *
import tensorflow as tf
import unittest


class TestReversibleDecoderLayer(unittest.TestCase):
    d_model = 512
    num_heads = 8
    dff = 2048

    def test_dimension(self):
        model = ReversibleDecoderLayer(self.d_model, self.num_heads, self.dff)
        left = tf.random.uniform([64, 43, 512])
        right = tf.random.uniform([64, 43, 512])
        enc_output = tf.random.uniform([64, 43, 512])

        left_out, right_out, attn1, attn2 = model(left, right, enc_output, False, None, None)
        self.assertEqual([64, 43, 512], left_out.shape.as_list())
        self.assertEqual([64, 43, 512], right_out.shape.as_list())
        self.assertEqual([64, 8, 43, 43], attn1.shape)
        self.assertEqual([64, 8, 43, 43], attn2.shape)


class TestReversalReversibleDecoderLayer(unittest.TestCase):
    d_model = 512
    num_heads = 8
    dff = 2048

    def test_dimension(self):
        model = ReversalReversibleDecoderLayer(self.d_model, self.num_heads, self.dff)
        left = tf.random.uniform([64, 43, 512])
        right = tf.random.uniform([64, 43, 512])
        enc_output = tf.random.uniform([64, 43, 512])

        left_out, right_out, attn1, attn2 = model(left, right, enc_output, False, None, None)
        self.assertEqual([64, 43, 512], left_out.shape.as_list())
        self.assertEqual([64, 43, 512], right_out.shape.as_list())
        self.assertEqual([64, 8, 43, 43], attn1.shape)
        self.assertEqual([64, 8, 43, 43], attn2.shape)
