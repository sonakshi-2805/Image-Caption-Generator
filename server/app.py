from flask import Flask, request, jsonify
import cv2
import numpy as np

from keras.applications import ResNet50
from keras.layers import (
    Dense, Input, LSTM, TimeDistributed,
    Embedding, Activation, RepeatVector, Concatenate
)
from keras.models import Model
from keras_preprocessing.sequence import pad_sequences

from tqdm import tqdm
from flask_cors import CORS


# =========================
# RESNET MODEL
# =========================

resnet = ResNet50(
    include_top=False,
    weights='imagenet',
    input_shape=(224,224,3),
    pooling='avg'
)

print("="*50)
print("resnet loaded")


# =========================
# VOCAB
# =========================

vocab = np.load('vocab.npy', allow_pickle=True)
vocab = vocab.item()

inv_vocab = {v:k for k,v in vocab.items()}


# =========================
# PARAMETERS
# =========================

embedding_size = 128
max_len = 40
vocab_size = len(vocab)


# =========================
# IMAGE FEATURE MODEL
# =========================

image_input = Input(shape=(2048,), name="dense_input")

image_features = Dense(
    embedding_size,
    activation='relu'
)(image_input)

image_features = RepeatVector(max_len)(image_features)


# =========================
# LANGUAGE MODEL
# =========================

language_input = Input(
    shape=(max_len,),
    name="embedding_input"
)

language_features = Embedding(
    input_dim=vocab_size,
    output_dim=embedding_size
)(language_input)

language_features = LSTM(
    256,
    return_sequences=True
)(language_features)

language_features = TimeDistributed(
    Dense(embedding_size)
)(language_features)


# =========================
# COMBINE BOTH MODELS
# =========================

merged = Concatenate()(
    [image_features, language_features]
)

x = LSTM(
    128,
    return_sequences=True
)(merged)

x = LSTM(
    512,
    return_sequences=False
)(x)

x = Dense(vocab_size)(x)

output = Activation('softmax')(x)


model = Model(
    inputs=[image_input, language_input],
    outputs=output
)


model.compile(
    loss='categorical_crossentropy',
    optimizer='RMSprop',
    metrics=['accuracy']
)


# =========================
# LOAD TRAINED WEIGHTS
# =========================

model.load_weights('mine_model_weights.h5')


print("="*50)
print("model loaded")


# =========================
# FLASK APP
# =========================

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

CORS(
    app,
    resources={
        r"/*": {
            "origins":"*"
        }
    }
)



@app.route('/after', methods=['POST'])
def after():

    global model, vocab, inv_vocab


    file = request.files['file']


    file.save('static/file.jpg')


    img = cv2.imread(
        'static/file.jpg'
    )


    img = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )


    img = cv2.resize(
        img,
        (224,224)
    )


    img = np.reshape(
        img,
        (1,224,224,3)
    )


    # Extract image features

    features = resnet.predict(img).reshape(
        1,2048
    )


    print("="*50)
    print("Predict Features")


    text_in = ['startofseq']

    final = ''


    print("="*50)
    print("GETTING CAPTION")


    count = 0


    while count < 20:

        count += 1


        encoded = []

        for word in text_in:
            encoded.append(
                vocab[word]
            )


        padded = pad_sequences(
            [encoded],
            maxlen=max_len,
            padding='post',
            truncating='post'
        )


        prediction = model.predict(
            [features, padded],
            verbose=0
        )


        sampled_index = np.argmax(
            prediction
        )


        sampled_word = inv_vocab[
            sampled_index
        ]


        if sampled_word != 'endofseq':

            final += " " + sampled_word


        text_in.append(
            sampled_word
        )


    return jsonify(
        {
            "caption": final
        }
    )



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
