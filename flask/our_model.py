
import tensorflow as tf
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding, Dropout, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2


total_words = 9000

max_length = 26

def define_our_model(total_words = 9000, max_length = 26):
    class BahdanauAttention(tf.keras.layers.Layer):
        def __init__(self, units):
            super(BahdanauAttention, self).__init__()
            self.W1 = Dense(units)
            self.W2 = Dense(units)
            self.V = Dense(1)

        def call(self, features, hidden):
            hidden_with_time_axis = tf.expand_dims(hidden, 1)
            score = self.V(tf.nn.tanh(self.W1(features) + self.W2(hidden_with_time_axis)))
            attention_weights = tf.nn.softmax(score, axis=1)
            context_vector = attention_weights * features
            context_vector = tf.reduce_sum(context_vector, axis=1)
            return context_vector, attention_weights
            
        def get_config(self):
            config = super(BahdanauAttention, self).get_config()
            config.update({
                'W1': self.W1,
                'W2': self.W2,
                'V': self.V,
            })
            return config

    embedding_dim = 256
    units = 256
    vocab_size = total_words + 1  # Add 1 for zero padding

    # 윤성(230417/230419)
    # encoder_input = Input(shape=(576,))
    # encoder_input = Input(shape=(512,))
    encoder_input = Input(shape=(2048,)) # xception

    l2_lambda = 0.001
    fe1 = Dense(embedding_dim, activation='relu', kernel_regularizer=l2(l2_lambda))(encoder_input)        
    # fe1 = Dense(embedding_dim, activation='relu')(encoder_input)

    fe2 = Dropout(0.5)(fe1)

    decoder_input = Input(shape=(max_length,))
    decoder_embedding = Embedding(vocab_size, embedding_dim, mask_zero=True)(decoder_input)
    decoder_lstm = LSTM(units, return_sequences=True, return_state=True, dropout=0.5, recurrent_dropout=0.2, name='decoder_lstm')
    decoder_outputs, state_h, state_c = decoder_lstm(decoder_embedding, initial_state=[fe2, fe2])

    # Add custom attribute 'decoder_units' to the decoder_lstm layer
    decoder_lstm.decoder_units = units

    attention_layer = BahdanauAttention(units)
    context_vector, attention_weights = attention_layer(fe1, state_h)
    decoder_concat = Concatenate(axis=-1)([context_vector, state_h])

    dense_layer = Dense(units, activation='relu')
    dense_output = dense_layer(decoder_concat)
    output = Dense(vocab_size, activation='softmax')(dense_output)

    # att_model = Model([encoder_input, decoder_input], output)
    # att_model2 = Model([encoder_input, decoder_input], output)
    test_model = Model([encoder_input, decoder_input], output)


    test_model.compile(optimizer=tf.keras.optimizers.Adam(), loss='categorical_crossentropy',)
    print("Compile success")
    return test_model


# load_weights

def load_model(test_model):
    test_model.load_weights("_content_drive_MyDrive_3조_Models_xception_t_1682372355+FN+4_caption_model.h5")

    print("load model success")
    print(test_model.summary())

