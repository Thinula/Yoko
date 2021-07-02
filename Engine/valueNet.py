import tensorflow as tf

class valueNet:

    def __init__(self, weights_file=None):
        if weights_file:
            pass
        else:
            self.model = tf.keras.Sequential()
            self.model.add(tf.keras.Input(shape=(64,)))
            self.model.add(tf.keras.layers.Dense(42,activation="relu"))
            # output probability for winning this game (+1 for B, -1 for W win)
            self.model.add(tf.keras.layers.Dense(1, activation="tanh"))
            
            #for layer in self.model.layers:
            #    weights = layer.get_weights()[0]
            #    print(weights)
            #    print(len(weights))

    def train_weights(self, dataset):
        
        pass

    def save_weights(self, file_name):
        pass
