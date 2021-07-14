import tensorflow as tf

tensor_const = tf.constant([[10, 20], [30, 40]])
print(tensor_const)
var_init_2 = tf.Variable(name="var_init_2", dtype=tf.int32)
print(var_init_2.shape)
print(var_init_2)
