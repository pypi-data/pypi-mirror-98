from tensorflow_modules import *
import tensorflow as tf
import unittest


class TestReversibleEncoderLayer(unittest.TestCase):
    d_model = 512
    num_heads = 8
    dff = 2048

    def test_dimension(self):
        model = ReversibleEncoderLayer(self.d_model, self.num_heads, self.dff)
        left = tf.random.uniform([64, 43, 512])
        right = tf.random.uniform([64, 43, 512])

        left_out, right_out = model(left, right, False, None)
        self.assertEqual([64, 43, 512], left_out.shape.as_list())
        self.assertEqual([64, 43, 512], right_out.shape.as_list())
