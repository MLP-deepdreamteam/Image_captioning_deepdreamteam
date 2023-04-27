# feature extract 추가 
# Xcetpion 


# import our_model

# test_model = our_model.define_our_model()
# our_model.load_model(test_model)



from PIL import Image
import numpy as np
import pickle 
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.applications.xception import Xception
import os
import tensorflow as tf

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'false'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Now you can continue with your code





def load_tokenizer(pkl_path):
    with open(pkl_path, "rb") as f:
        tokenizer_pickle = pickle.load(f)

    tokenizer = tokenizer_pickle['tokenizer']
    return tokenizer

def extract_features(filename, model, model_e = 'xception'):
        try:
            image = Image.open(filename)

        except:
            print("ERROR: Couldn't open image! Make sure the image path and extension is correct")
        
        if model_e[:-2] == "vgg":
            image = image.resize((224,224))
            print("resizing")
        elif(model_e[:-2] == "mobilenet"):
            image = image.resize((224,224))
            print("resizing")          

        else:
            image = image.resize((299,299))


        image = np.array(image)
        
        # for images that has 4 channels, we convert them into 3 channels
        if image.shape[2] == 4: 
            image = image[..., :3]
        image = np.expand_dims(image, axis=0)
        image = image/127.5
        image = image - 1.0
        feature = model.predict(image)
        return feature

def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = '<start>'

    units = model.layers[-5].decoder_units
    attention_layer  = model.layers[-4]
    attention_weights_list = []


    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        # pred = model.predict([photo, sequence], verbose=0)

        initial_state = model.layers[2](model.layers[1](photo))
        # print("initial_state",initial_state.shape)
        decoder_embedding = model.layers[3](sequence)

        # Sum the decoder_embedding tensor along the one-hot encoding axis
        # print("decoder_embedding",decoder_embedding.shape)

        decoder_outputs, state_h, state_c = model.layers[-5](decoder_embedding, initial_state=[initial_state, initial_state])

        # print("decoder_outputs",decoder_outputs.shape,"state_h", state_h.shape, "state_c",state_c.shape)
        # print(model.layers[1](photo).shape)
        # dense_output = tf.expand_dims(model.layers[1](photo), 1)  # Add a new dimension
        c_v, at_wt = attention_layer(decoder_outputs, state_h)
        # print("c_v",c_v.shape)
        # print("at_wt",at_wt.shape)
        attention_weights_list.append(at_wt)
        pred = model.predict([photo, sequence], verbose=0)
        pred = np.argmax(pred, axis=-1)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word

        if word == 'end' or word == '<end>':
            in_text = in_text[:-3] + "<" + in_text[-3:] + ">"
            break
    attention_weights_array = np.squeeze(np.array(attention_weights_list))
    return in_text, attention_weights_array


def define_CNN_Encoder():
    CNN_model = Xception(include_top=False, pooling="avg")
    # CNN_model.summary()
    return CNN_model
    

def extract_caption(image_filepath,model,CNN_model):
    photo = extract_features(image_filepath, CNN_model)
    # print(photo.shape)
    tokenizer = load_tokenizer("my_tokenizer_230422.pkl")
    caption, _ =  generate_desc(model, tokenizer,photo, max_length=26)
    print(caption) # 
    return caption

# print(extract_caption("static\images\Lena.jpg",test_model))
