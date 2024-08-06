from tensorflow import keras
from keras import layers
from keras.datasets import mnist
from keras.utils import to_categorical

def create_network():
  network = keras.Sequential([
  layers.Flatten(input_shape=(28, 28)),
  layers.Dense(512, activation='relu', input_shape=(28 * 28,)),
  layers.Dense(10, activation='softmax')
  ])
  network.compile(
    optimizer='rmsprop',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
  return network

def fit_network(network, train_images, train_labels):
    return network.fit(train_images, train_labels, epochs=1, batch_size=128, verbose=1)

def trainModel(weights):
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    train_images = train_images.astype('float32') / 255
    test_images = test_images.astype('float32') / 255
    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)
    nr_of_samples = train_images.shape[0]

    network = create_network()
    if weights is not None:
      network.set_weights(weights)
      print(f"Using consumed weights on {nr_of_samples} samples")
    else:
       print(f"Training network from scratch on {nr_of_samples} samples")

    fit_network(network, train_images, train_labels)
    return network.weights, nr_of_samples