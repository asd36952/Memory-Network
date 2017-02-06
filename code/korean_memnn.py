from keras.models import Model
from keras.layers.embeddings import Embedding
from keras.layers import Activation, Dense, merge, Permute, Dropout, Input, Lambda, RepeatVector, Reshape
from keras.layers import LSTM
from keras import backend as K


import numpy as np

import util

MAXIMUM_MEMORY_SIZE=10000
story_maxlen=0
query_maxlen=0
MEMORY=K.placeholder(shape=(MAXIMUM_MEMORY_SIZE,64))

stories=[["Seongwoo","was","born","in","Busan","."],["Seongwoo","goes","to","Ulsan","."],["Seongwoo","likes","cat","."]] #["Seongwoo","likes","cat","."]

queries=[["Where","is","the","birthplace","of","Seongwoo","?"],["Where","is","Seongwoo","?"]]
answers=[["Busan"],["Ulsan"]]

vocabulary=set()
story_maxnum=0
for story in stories:
    story_maxnum+=1
    story_maxlen=max(len(story),story_maxlen)
    for word in story:
        vocabulary.add(word)
for query in queries:
    query_maxlen=max(len(query),query_maxlen)
    for word in query:
        vocabulary.add(word)

vocabulary=list(vocabulary)
vocabulary.append("Unknown")
vocab_size=len(vocabulary)

#vectorized_stories=[]
#for elem in util.vectorize_sentence(stories,vocabulary,story_maxlen):
#    vectorized_stories+=elem
vectorized_stories=util.vectorize_sentence(stories,vocabulary,story_maxlen)
vectorized_queries=util.vectorize_sentence(queries,vocabulary,query_maxlen)
vectorized_answers=util.vectorize_sentence(answers,vocabulary,None)

#vectorized_stories=np.array([vectorized_stories])
vectorized_stories=np.array(vectorized_stories)
vectorized_queries=np.array(vectorized_queries)
vectorized_answers=np.array(vectorized_answers)

#story_input = Input(shape=(story_maxlen*story_maxnum,))
story_input = Input(batch_shape=(story_maxnum,story_maxlen,))
story_embedding_layer=Embedding(input_dim=vocab_size+1,output_dim=64)(story_input)
#story_embedding_layer=Reshape((story_maxnum,story_maxlen,64))(story_embedding_layer)
story_forward_LSTM_layer=LSTM(64)(story_embedding_layer)
story_backward_LSTM_layer=LSTM(64,go_backwards=True)(story_embedding_layer)
story_merged_LSTM_layer=merge([story_forward_LSTM_layer,story_backward_LSTM_layer],mode='concat')
story_bid_LSTM_layer=Dense(64)(story_merged_LSTM_layer)
#story_bid_LSTM_layer=Reshape(1,64)
#repeated_story_bid_LSTM_layer=RepeatVector(len(vectorized_queries))(story_bid_LSTM_layer)
#input_encoder_m.add(Dropout(0.3))

#model1=Model(input=story_input,output=repeated_story_bid_LSTM_layer)
model1=Model(input=story_input,output=story_bid_LSTM_layer)

model1.compile('rmsprop', 'mse')
memory1=model1.predict(np.array(vectorized_stories))
print(memory1)
def make_memory(final):
    model1=Model(input=story_input,output=final)
    model1.compile('rmsprop', 'mse')
    return K.variable(value=model1.predict(np.array(vectorized_stories)))
a=Lambda(make_memory)(story_bid_LSTM_layer)
a=RepeatVector(4)(a)

model2=Model(input=story_input,output=a)
model2.compile('rmsprop', 'mse') 
print(model2.predict(np.array(vectorized_stories)))
print(model1.output_shape)
print(model2.output_shape)
exit()

#memory_input=Input(batch_shape=(len(memory1),64))
query_input = Input(shape=(query_maxlen,))
query_embedding_layer=Embedding(input_dim=vocab_size+1,output_dim=64,mask_zero=True)(query_input)
query_forward_LSTM_layer=LSTM(64)(query_embedding_layer)
query_backward_LSTM_layer=LSTM(64,go_backwards=True)(query_embedding_layer)
query_merged_LSTM_layer=merge([query_forward_LSTM_layer,query_backward_LSTM_layer],mode='concat')
query_bid_LSTM_layer=Dense(64)(query_merged_LSTM_layer)
#question_encoder.add(Dropout(0.3))
#attention=merge([memory1,query_bid_LSTM_layer],mode='dot',dot_axes=[1,1])
#attention=merge([query_bid_LSTM_layer,story_bid_LSTM_layer.output],mode='dot',dot_axes=[1,2])
print(model1.output_shape)
#attention=merge([query_bid_LSTM_layer,model1.output],mode='dot',dot_axes=[1,2])
#attention=Activation("linear")(attention)
#attention=K.tensor_dot(story_bid_LSTM_layer,query_bid_LSTM_layer,axes=[1,2])
attention=K.batch_dot(query_bid_LSTM_layer,model1.output,axes=[1,1])
attention=Activation("linear")(attention)
#model=Model(input=[memory_input,query_input],output=attention)
model=Model(input=[story_input,query_input],output=attention)
model.compile('rmsprop', 'mse')
print(memory1)
#print(model.predict([memory1,np.array(vectorized_queries)]))
print(model.predict([np.array(vectorized_stories),np.array(vectorized_queries)]))
exit()


match = Sequential()
match.add(Merge([input_encoder_m, question_encoder],
                mode='dot',
                dot_axes=[2, 2]))
match.add(Activation('softmax'))
# output: (samples, story_maxlen, query_maxlen)
# embed the input into a single vector with size = story_maxlen:
input_encoder_c = Sequential()
input_encoder_c.add(Embedding(input_dim=vocab_size,
                              output_dim=query_maxlen,
                              input_length=story_maxlen))
input_encoder_c.add(Dropout(0.3))
# output: (samples, story_maxlen, query_maxlen)
# sum the match vector with the input vector:
response = Sequential()
response.add(Merge([match, input_encoder_c], mode='sum'))
# output: (samples, story_maxlen, query_maxlen)
response.add(Permute((2, 1)))  # output: (samples, query_maxlen, story_maxlen)

# concatenate the match vector with the question vector,
# and do logistic regression on top
answer = Sequential()
answer.add(Merge([response, question_encoder], mode='concat', concat_axis=-1))
# the original paper uses a matrix multiplication for this reduction step.
# we choose to use a RNN instead.
answer.add(LSTM(32))
# one regularization layer -- more would probably be needed.
answer.add(Dropout(0.3))
answer.add(Dense(vocab_size))
# we output a probability distribution over the vocabulary
answer.add(Activation('softmax'))

answer.compile(optimizer='rmsprop', loss='categorical_crossentropy',
               metrics=['accuracy'])
# Note: you could use a Graph model to avoid repeat the input twice
answer.fit([inputs_train, queries_train, inputs_train], answers_train,
           batch_size=32,
           nb_epoch=120,
           validation_data=([inputs_test, queries_test, inputs_test], answers_test))
