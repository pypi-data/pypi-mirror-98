# from easier import EasierSDK
# from classes.categories import Categories
# from minio import Minio

from easierSDK.easier import EasierSDK
from easierSDK.classes.categories import Categories  
import easierSDK.classes.constants as Constants 
from easierSDK.classes.training_metadata import TrainingMetadata
from easierSDK.classes.model_metadata import ModelMetadata

import os
from datetime import datetime

# Initializations
minio_access = os.getenv("minio_access", "adrian.arroyo")
minio_secret = os.getenv("minio_secret", "JlInP3p/VYffEQME")
easier = EasierSDK(easier_url="minio.easier-ai.eu", easier_user=minio_access, easier_password=minio_secret)

repositories = easier.get_repositories_metadata(category=None)

easier.datasets.download(repo_name="easier-public", category=Categories.MISC, dataset_name="kaggle-pokemon-data", path_to_download="./")
os.system("tar -xvf  ./datasets/misc/kaggle-pokemon-data/kaggle-pokemon-data.tar.gz -C  ./datasets/misc/kaggle-pokemon-data/")
pokemon_df = easier.datasets.load_csv(local_path="./datasets/misc/kaggle-pokemon-data/pokemon/Pokemon.csv", separator=',')
pokemon_df = pokemon_df.drop(columns=["#", "Name"])
pokemon_df = pokemon_df.dropna()
encoded_pokemon, one_hot_encoder = easier.datasets.one_hot_encode_data(pokemon_df, labels=["Legendary"])
labels, label_encoder = easier.datasets.encode_labels(encoded_pokemon, labels=["Legendary"])
scaled_pokemon, scaler = easier.datasets.scale_data(encoded_pokemon.drop(columns=["Legendary"]), ft_range=(0, 1))

x_train, y_train, x_test, y_test = easier.datasets.train_test_split_data(scaled_pokemon, labels)

import tensorflow as tf

my_tf_model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(x_train.shape[1],)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(len(label_encoder.classes_), activation='softmax')
  ])

# my_tf_model.compile(optimizer='adam',
#             loss=tf.keras.losses.categorical_crossentropy,
#             metrics=[tf.keras.metrics.mean_squared_error])
# my_tf_model.summary()


# # - Create ModelMetadata
mymodel_metadata = ModelMetadata()
mymodel_metadata.category = Categories.MISC
mymodel_metadata.name = 'my-simple-pokemon-classifier'
mymodel_metadata.last_modified = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
mymodel_metadata.description = 'My Simple Pokemon Clasifier'
mymodel_metadata.version = 0
mymodel_metadata.features = pokemon_df.columns.values.tolist()

# # - Create TrainingMetadata
mymodel_training_metadata = TrainingMetadata()
mymodel_training_metadata.inference_mode = Constants.CLASSIFIER
mymodel_training_metadata.optimizer = 'adam'
mymodel_training_metadata.loss = "categorical_crossentropy"
mymodel_training_metadata.epochs = 10
mymodel_training_metadata.batch_size = 10
mymodel_training_metadata.metrics = ['mse']

# Setup EasierModel
from easierSDK.classes.easier_model import EasierModel

my_easier_model = EasierModel()
my_easier_model.set_metadata(mymodel_metadata)
my_easier_model.set_training_metadata(mymodel_training_metadata)
my_easier_model.set_model(my_tf_model)

# Create training
easier.training.initialize(kube_config_path="/easier-sdk/easierSDK/k8s-adri-services-adri-conf")
easier.training.create_training(x_train, y_train, x_test, y_test, my_easier_model, mymodel_training_metadata)


# General info
# models_list, datasets_list = easier.show_available_repos()
# models_list, datasets_list = easier.show_available_repos(deep=True)
# print(models_list)
# print(datasets_list)

# models_list, datasets_list = easier.show_categories()
# models_list, datasets_list = easier.show_categories(deep=True)
# print(models_list)
# print(datasets_list)

# Models API
# easier.models.show_models(repo_name=None, category=None)
# print("-----")
# easier.models.show_models(repo_name="easier-private", category=None)
# print("-----")
# easier.models.show_models(repo_name=None, category=Categories.MISC)
# print("-----")
# easier.models.show_models(repo_name="easier-private", category=Categories.MISC)

# easier.models.show_model_info(repo_name="easier-private", category=Categories.MISC, model_name="resnet50_v2")
# easier.models.show_model_info(repo_name="easier-private", category=Categories.MISC, model_name="resnet50_v2", experimentID=1)

# easier.models.load_from_repository(repo_name="easier-private", category=Categories.MISC, model_name="resnet50_v2")
# easier.models.load_from_repository(repo_name="easier-private", category=Categories.MISC, model_name="resnet50_v2", experimentID=1)

# Datasets API
# easier.datasets.show_datasets(repo_name=None, category=None)
# print("-----")
# easier.datasets.show_datasets(repo_name="easier-private", category=None)
# print("-----")
# easier.datasets.show_datasets(repo_name=None, category=Categories.HEALTH)
# print("-----")
# easier.datasets.show_datasets(repo_name="easier-private", category=Categories.HEALTH)
