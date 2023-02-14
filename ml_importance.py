from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import numpy as np
import pickle

model = tf.keras.models.load_model("ml\single_token_vendor_model")

with open("ml\single_token_vendor_tokenizer.pickle","rb") as file:
    tkn = pickle.load(file)

def return_importance_vector(input_string):
    importance = []
    words = input_string.lower().replace("_"," ").replace("-"," ").split(" ")
    
    for word in words:
        tokenised_sequence = tkn.texts_to_sequences([word])
        test_sequence = np.array(pad_sequences(tokenised_sequence,maxlen = 24,padding = "pre"))

        importance.append(model.predict(test_sequence,verbose = False)[0][0])


    return importance