import time as time_lib
import argparse
import os, sys
import joblib
import json
import tensorflow as tf
import pandas
import numpy
import joblib
import tempfile

from easierSDK.easier import EasierSDK
from easierSDK.classes.categories import Categories
from easierSDK.classes.model_metadata import ModelMetadata
from easierSDK.classes.easier_model import EasierModel
import easierSDK.classes.constants as constants
from easierSDK import datasetsAPI

# Variable definition
easier = None
easier_model = None

# https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/distribute/multi_worker_with_keras.ipynb#scrollTo=iUZna-JKAOrX

# Environment variables loading
# tf_config = json.loads(os.environ['TF_CONFIG'])
# num_workers = len(tf_config['cluster']['worker'])

checkpoint_dir = os.getenv('CHECKPOINT_DIR', '/train/checkpoint')
data_dir = os.getenv('DATA_DIR', '/train/data')
model_dir = os.getenv('MODEL_DIR', '/train/model')
model_name = os.getenv('MODEL_NAME', 'model')

per_worker_batch_size = os.getenv('WORKER_BATCH_SIZE', 64)
# global_batch_size = per_worker_batch_size * num_workers
# save_freq = os.getenv('SAVE_FREQ', 10)

def dataset_fn(input_context):
    pass
    batch_size = input_context.get_per_replica_batch_size(global_batch_size)
    dataset = tf.data.Dataset()
    dataset = dataset.shard(
        input_context.num_input_pipelines, input_context.input_pipeline_id)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(2) # This prefetches 2 batches per device.
    return dataset


def build_compile_model(model_dir:str, model_name:str):
    pass
    model = tf.keras.models.model_from_json(json.loads(model_dir + '/' + model_name + '.json'), 
                custom_objects=None)
    model.compile(
        optimizer='rmsprop', 
        loss=tf.keras.losses.categorical_crossentropy,
        metrics=[tf.keras.metrics.mean_squared_error]
    )
    return model

def compile_model(easier_model:EasierModel):
    # TF Compile should be done within distributed strategy
    easier_model.model.compile(
        optimizer=easier_model.training_metadata.optimizer, 
        loss=easier_model.training_metadata.loss,
        metrics=easier_model.training_metadata.metrics
    )
    easier_model.model.summary()
    return easier_model

if __name__ == "__main__":
    
    # Initializations
    easier_user = os.getenv("easier_user")
    easier_password = os.getenv("easier_password")
    easier = EasierSDK(easier_user=easier_user, easier_password=easier_password)

    repo = os.getenv("repo")
    category = os.getenv("category")
    model_name = os.getenv("model_name")
    experimentID = os.getenv("experimentID")
    data_path = os.getenv("data_path")

    easier_model = easier.models.get_model(repo_name=repo, category=category, model_name=model_name, experimentID=experimentID, load_level=constants.FULL, training=True)

    x, y, x_test, y_test = easier.training.get_training_data(repo_path=data_path)

    easier_model = compile_model(easier_model)

    history = easier_model.model.fit(x, y, validation_data=(x_test, y_test), epochs=easier_model.training_metadata.epochs, batch_size=easier_model.training_metadata.batch_size, verbose=2)

    easier.training.clear_training_data(repo_path=data_path, repo_name=repo)

    easier.models._finish_model_training(easier_model, repo_name=repo, category=category, experimentID=experimentID)

    # Successfull exit
    sys.exit()

def distributed_training():
    # Worker 0 is the chief worker
    if tf_config['task']['index'] == 0:
               
        # Define the distributed strategy. ClusterResolver tells how the workers are distributed
        
        # cluster_resolver = tf.distribute.cluster_resolver.KubernetesClusterResolver(
        #     {"worker": ["job-name=worker-cluster-a", "job-name=worker-cluster-b"]})
        # cluster_resolver.task_type = "worker"
        # cluster_resolver.task_id = 0

        cluster_resolver = tf.distribute.cluster_resolver.TFConfigClusterResolver()
        strategy = tf.distribute.MultiWorkerMirroredStrategy(cluster_resolver=cluster_resolver)

        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
        
        # Read data from /train/data
        dataset = tf.data.Dataset.from_tensor_slices()
        multi_worker_dataset = strategy.experimental_distribute_dataset(dataset, options)

        with strategy.scope():
            # Model building/compiling need to be within `strategy.scope()`.
            multi_worker_model = build_compile_model(model_dir)


        callbacks = [
                # This callback saves a SavedModel every epoch
                # We include the current epoch in the folder name.
                tensorflow.keras.callbacks.ModelCheckpoint(
                    filepath=checkpoint_dir + "/ckpt-{epoch}", save_freq=save_freq
                )
            ]
        multi_worker_model.fit(multi_worker_dataset, epochs=3, steps_per_epoch=70)

        multi_worker_model.save(checkpoint_dir + "final_model.h5")

    else:
        cluster_resolver = tf.distribute.cluster_resolver.TFConfigClusterResolver()
        strategy = tf.distribute.MultiWorkerMirroredStrategy(cluster_resolver=cluster_resolver)

        # with strategy.scope():
        #     # Model building/compiling need to be within `strategy.scope()`.
        #     multi_worker_model = build_compile_model(model_dir)

        callbacks = [
                # This callback saves a SavedModel every epoch
                # We include the current epoch in the folder name.
                tensorflow.keras.callbacks.ModelCheckpoint(
                    filepath=checkpoint_dir + "/ckpt-{epoch}", save_freq=save_freq
                )
            ]
        multi_worker_model.fit(multi_worker_dataset, epochs=3, steps_per_epoch=70)