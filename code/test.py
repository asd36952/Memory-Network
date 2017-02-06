from keras.layers import Input, merge
from keras.models import Model
import numpy as np

input_a = np.reshape([1, 2, 3], (1, 1, 3))
input_b = np.reshape([4, 5, 6], (1, 1, 3))

a = Input(shape=(1, 3))
b = Input(shape=(1, 3))

concat = merge([a, b], mode='concat', concat_axis=-1)
dot = merge([a, b], mode='dot', dot_axes=2)
cos = merge([a, b], mode='cos', dot_axes=2)

model_concat = Model(input=[a, b], output=concat)
model_dot = Model(input=[a, b], output=dot)
model_cos = Model(input=[a, b], output=cos)

print(input_a)
print(input_b)
print(model_concat.predict([input_a, input_b]))
print(model_dot.predict([input_a, input_b]))
print(model_cos.predict([input_a, input_b]))
