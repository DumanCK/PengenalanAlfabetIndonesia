#from tensorflow.python.util import deprecation
#deprecation._PRINT_DEPRECATION_WARNINGS = False

import tensorflow as tf
#tf.get_logger().warning('test')
# WARNING:tensorflow:test
tf.get_logger().setLevel('ERROR')
#tf.get_logger().warning('test')

#import warnings

#warnings.filterwarnings('ignore', category=DeprecationWarning)
#warnings.filterwarnings('ignore', category=FutureWarning)

from preprocess import *
import keras
#from keras.models import Sequential
#from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
#from keras.utils import to_categorical
from keras.models import load_model


feature_dim_1 = 20
feature_dim_2 = 11
channel = 1

# Predicts one sample
def predict(filepath, model):
    sample = wav2mfcc(filepath)
    sample_reshaped = sample.reshape(1, feature_dim_1, feature_dim_2, channel)
    return get_labels()[0][
            np.argmax(model.predict(sample_reshaped))
    ]

# load model
model = load_model('model.h5')
print(predict('./KUNCI/Z.wav', model=model))
