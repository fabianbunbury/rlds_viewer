
import tensorflow_datasets as tfds
import rlds
import tensorflow as tf 
import json

# create RLDS dataset builder
builder = tfds.builder_from_directory(
    builder_dir="gs://gresearch/robotics/berkeley_cable_routing/0.1.0/"
)
ds = builder.as_dataset(split="train[0:1]")
info = builder.info
meta_data = info.as_json
json1_data = json.loads(meta_data)[0]


# Extract the number of episodes in the dataset
num_episodes = tf.data.experimental.cardinality(ds)
print("Number of episodes:", num_episodes.numpy())
number_train = len(json.loads(meta_data)['splits'][0]['shardLengths'])
