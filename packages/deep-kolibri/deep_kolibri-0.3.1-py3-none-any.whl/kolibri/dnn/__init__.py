import tensorflow as tf
from kolibri.dnn.tasks.audio import *
from kolibri.dnn.tasks.text import *

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
custom_objects = tf.keras.utils.get_custom_objects()


def custom_object_scope():
    return tf.keras.utils.custom_object_scope(custom_objects)


# from kolibri.dnn import layers
# from kolibri.dnn import embeddings
# from kolibri.dnn import indexers
# from kolibri.dnn import tasks
# from kolibri.dnn import utils
# from kolibri.dnn import callbacks
