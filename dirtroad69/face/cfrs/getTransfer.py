
# coding: utf-8

# In[2]:

import tensorflow as tf


# In[11]:

import time
from datetime import timedelta
import os
import numpy as np


# In[7]:

data_dir = 'C:\\Users\\Reg2017\\PycharmProjects\\JeffDropsIT\\DirtRoad69\\face\\inception' # directory for inception model
path_graph_def = "classify_image_graph_def.pb" # inception model downloaded graph
label = np.array([ [1.,  0.,  0.]])  # label with one-hot encode


# In[33]:

graph = tf.Graph()

# Set the new graph as the default.
with graph.as_default():

# TensorFlow graphs are saved to disk as so-called Protocol Buffers
# aka. proto-bufs which is a file-format that works on multiple
# platforms. In this case it is saved as a binary file.

# Open the graph-def file for binary reading.
        path = os.path.join(data_dir, path_graph_def)
        with tf.gfile.FastGFile(path, 'rb') as file:
             # The graph-def is a saved copy of a TensorFlow graph.
             # First we need to create an empty graph-def.
            graph_def = tf.GraphDef()

            # Then we load the proto-buf file into the graph-def.
            graph_def.ParseFromString(file.read())

                # Finally we import the graph-def to the default TensorFlow graph.
            tf.import_graph_def(graph_def, name='')
session = tf.Session(graph=graph)
print("graph created successfully")
#return graph, session

def _create_feed_dict(image_path=None, image=None):
    """
    Create and return a feed-dict with an image.

    :param image_path:
         The input image is a jpeg-file with this file-path.

    :param image:
            The input image is a 3-dim array which is already decoded.
            The pixels MUST be values between 0 and 255 (float or int).

     :return:
            Dict for feeding to the Inception graph in TensorFlow.
        """

    if image is not None:
            # Image is passed in as a 3-dim array that is already decoded.
           feed_dict = {"DecodeJpeg:0": image}


    elif image_path is not None:
            # Read the jpeg-image as an array of bytes.
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()

            # Image is passed in as a jpeg-encoded image.
        feed_dict = {"DecodeJpeg/contents:0": image_data}

    else:
        raise ValueError("Either image or image_path must be set.")

    return feed_dict

def transfer_values(image_path=None, image=None):
    """
    Calculate the transfer-values for the given image.

    """
    start_time = time.time()
    import numpy as np

    # Create a feed-dict for the TensorFlow graph with the input image.
    feed_dict = _create_feed_dict(image_path=image_path, image=image)

    transfer_values = session.run(transfer_layer, feed_dict=feed_dict)

    # Reduce to a 1-dim array.
    transfer_values = np.squeeze(transfer_values)
    end_time = time.time()
    time_dif = end_time - start_time

    print("time: " + str(time_dif) + ' sec')
    return transfer_values.reshape(1, 2048)

def restore():
    # restore model and it variables
    sess = tf.Session()
    saver = tf.train.import_meta_graph('C:/cfrs-model/inception.cpkl.meta')
    saver.restore(sess, tf.train.latest_checkpoint('C:/cfrs-model/'))

    label = np.array([[1., 0., 0.]])
    x = sess.graph.get_tensor_by_name('x:0')
    y_true = sess.graph.get_tensor_by_name('y_true:0')
    y_pred_cls = sess.graph.get_tensor_by_name('ArgMax_1:0')

    return x, y_true, y_pred_cls, sess


def getClass(array):

    cls = int(str(array).lstrip('[').rstrip(']'))
    return cls

#---------------------------------------------------------------------------------------------------------------------


#graph, session = graphing()
#session = tf.Session(graph=graph)
# In[14]:
transfer_layer = graph.get_tensor_by_name('pool_3:0')
transfer_values_im = transfer_values(image_path='C:\\test1\\2015\\cow2015-3-0030.jpg')



x, y_true, y_pred_cls, sess = restore()


# In[65]:

feed_dict = {x: transfer_values_im, y_true: label}


# In[66]:

cls_pred = sess.run(y_pred_cls, feed_dict=feed_dict)


# In[67]:

print(getClass(cls_pred))

