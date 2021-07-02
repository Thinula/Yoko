import tensorflow as tf
import os
import pandas as pd

# taken from tensorflow documentation
def pack_features_vector(features, labels):
  """Pack the features into a single array."""
  features = tf.stack(list(features.values()), axis=1)
  return features, labels

class policyNet:

    def __init__(self, weights_file=None):
        if weights_file:
            pass
        else:
            self.model = tf.keras.Sequential()
            self.model.add(tf.keras.Input(shape=(64, )))
            self.model.add(tf.keras.layers.Dense(106, activation="relu"))
            self.model.add(tf.keras.layers.Dropout(0.4, input_shape=(106,)))
            # output probability for playing each possible index
            self.model.add(tf.keras.layers.Dense(64, activation="sigmoid"))

            lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(initial_learning_rate=0.01, decay_rate=0.9, decay_steps=10000)
            opt = tf.keras.optimizers.SGD(learning_rate=lr_schedule, momentum=0.9)
            self.model.compile(optimizer=opt, loss="binary_crossentropy") #, metrics=[tf.keras.metrics.CategoricalCrossentropy()])#"accuracy"])
            
            #for layer in self.model.layers:
            #    weights = layer.get_weights()[0]
            #    print(weights)
            #    print(len(weights))

    def train_weights(self, dataset_path, batch_size=32):
        column_names = ["Posn #"] + ["Feature " + str(i+1) for i in range(64)] + ["Label"]

        train_dataset = tf.data.experimental.make_csv_dataset(
            dataset_path,
            batch_size,
            column_names=column_names,
            select_columns=column_names[1:],
            label_name=column_names[-1],
            num_epochs=250)
        train_dataset = train_dataset.map(pack_features_vector)
        features, labels = next(iter(train_dataset))

        labels = tf.keras.utils.to_categorical(labels, num_classes=64, dtype="int")
        self.model.fit(features, labels, batch_size=batch_size, epochs=250, verbose=1, validation_split=0.2)     

    def test_accuracy(self, dataset_path, batch_size=32):
        df = pd.read_csv(dataset_path)
        features = df[["Feature " + str(i+1) for i in range(64)]]
        targets = df[["Label " + str(i+1) for i in range(64)]]

        dataset = tf.data.Dataset.from_tensor_slices((features.values, targets.values))
        test_dataset = dataset.shuffle(len(dataset)).batch(batch_size)

        features, labels = next(iter(test_dataset))
        print(features[:5])
        print(labels[:5])

        self.model.evaluate(features, labels, batch_size=batch_size, verbose=1)

    def save_weights(self, file_name):
        self.model.save_weights(filepath=file_name)

    def load_weights(self, file_name):
        self.model.load_weights(filepath=file_name)

batch_size = 128
policy = policyNet()
#policy.train_weights(dataset_path="Policy Dataset/training_data.csv", batch_size=batch_size)
policy.load_weights(file_name="Policy Dataset/weights.h5")
policy.test_accuracy(dataset_path="Policy Dataset/testing_data.csv", batch_size=batch_size)
policy.save_weights(file_name="Policy Dataset/weights.h5")
