import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Dense, LayerNormalization, GlobalAveragePooling1D, Input
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt


class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-3)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-3)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)


class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions


maxlen = 20  # Only consider the first 200 words of each text
x_data, y_data = np.load("x_data.npy"), np.load("y_data.npy")
print(len(x_data), "Training sequences")
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=777)
print(len(x_train), "Validation sequences")
print(len(x_test), "Validation sequences")
print(x_train[:10], y_train[:10])
# x_train = keras.preprocessing.sequence.pad_sequences(x_train, maxlen=maxlen)
# x_test = keras.preprocessing.sequence.pad_sequences(x_test, maxlen=maxlen)
print(x_train[:10], y_train[:10])

vocab_size = len(x_data)
print(vocab_size)
embed_dim = 32  # Embedding size for each token
num_heads = 2  # Number of attention heads
ff_dim = 32  # Hidden layer size in feed forward network inside transformer

batch_size = 32
epochs = 5
transformer_block = TransformerBlock(embed_dim, num_heads, ff_dim)
optimizer = Adam(learning_rate=0.01)

# inputs = layers.Input(shape=(maxlen,))
model = Sequential()

model.add(Input(shape=(maxlen,)))
model.add(TokenAndPositionEmbedding(maxlen, vocab_size, embed_dim))

model.add(transformer_block)


model.add(GlobalAveragePooling1D())
model.add(Dropout(0.1))

model.add(Dense(20))
model.add(Dropout(0.1))

model.add(Dense(7, activation='softmax'))
# embedding_layer = TokenAndPositionEmbedding(maxlen, vocab_size, embed_dim)
# x = embedding_layer(inputs)
# transformer_block = TransformerBlock(embed_dim, num_heads, ff_dim)
# x = transformer_block(x)
# x = transformer_block(x)
# x = transformer_block(x)
# x = layers.GlobalAveragePooling1D()(x)
# x = layers.Dropout(0.1)(x)
# x = layers.Dense(20, activation="relu")(x)
# x = layers.Dropout(0.1)(x)
# outputs = layers.Dense(7, activation="softmax")(x)
# print(outputs)
# model = keras.Model(inputs=inputs, outputs=outputs)
model_checkpoint = ModelCheckpoint(filepath="./TextClassificationModel/", save_best_only=True)
model.summary()

model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"])
history = model.fit(
    x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2, callbacks=[model_checkpoint]
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss=history.history['loss']
val_loss=history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()