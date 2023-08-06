import os
import kubernetes
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import string
import random
import joblib
import tempfile
import json

from easierSDK.classes.categories import Categories
from easierSDK.classes import constants
from easierSDK.classes.easier_model import EasierModel
from easierSDK.classes.training_metadata import TrainingMetadata
from easierSDK.training import easier_training_config_map
from easierSDK.training import easier_training_deployment
from easierSDK.training import easier_training_service 
from easierSDK.training import easier_training_ingress 

class TrainingAPI():
    """Class to control the Training API of EasierSDK.
    """

    _easier_user = None
    _easier_password = None

    def __init__(self, easier_user, easier_password, minio_client, my_public_repo, my_private_repo):
        """Constructor for the TrainingAPI.

        Args:
            minio_client (Minio): Minio client object with user session initialized.
            my_public_repo (str): Name of the public bucket of the user.
            my_private_repo (str): Name of the private bucket of the user.
        """
        self._easier_user = easier_user
        self._easier_password = easier_password
        self.minio_client = minio_client
        self.my_public_repo = my_public_repo
        self.my_private_repo = my_private_repo
        
    def initialize(self, kube_config_path=None):
        if kube_config_path:
            kubernetes.config.load_kube_config(kube_config_path)
            with open(os.path.join(os.path.dirname(__file__), kube_config_path)) as f:
                kubeconfig = yaml.safe_load(f)
                self.namespace = kubeconfig['contexts'][0]['context']['namespace']
        else:
            kubernetes.config.load_kube_config()
            with open(os.path.join(os.path.dirname(__file__), os.environ.get('KUBECONFIG', '~/.kube/config'))) as f:
                kubeconfig = yaml.safe_load(f)
                self.namespace = kubeconfig['contexts'][0]['context']['namespace']

        print("Current context on namespace: " + str(self.namespace))
        
    def id_generator(self, size=16, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_training_data(self, repo_path=None):
        
        # Pickle x and y from minio
        x = None
        y = None
        x_test = None
        y_test = None
        with tempfile.TemporaryDirectory() as path:
            if repo_path is None: repo_path = os.getenv("model_path", '/train/data')

            object_list = self.minio_client.list_objects(self.my_private_repo, prefix=repo_path, recursive=True)
            has_items = False
            # 3. Download
            for obj in object_list:
                if not obj.is_dir:
                    has_items = True
                    self.minio_client.fget_object(self.my_private_repo, obj.object_name, path+'/'+obj.object_name)
            if not has_items:
                print('[ERROR] Could not find file. Please check parameters and try again.')
                return False
            try:
                x = joblib.load(path+'/'+repo_path+'/x.joblib')
            except Exception as e:
                print("[ERROR] Loading training data (x): " + str(e))
            try:
                y = joblib.load(path+'/'+repo_path+'/y.joblib')
            except Exception as e:
                print("[ERROR] Loading training data (y): " + str(e))
            try:
                x_test = joblib.load(path+'/'+repo_path+'/x_test.joblib')
            except Exception as e:
                print("[ERROR] Loading validation data (x_test): " + str(e))
            try:
                y_test = joblib.load(path+'/'+repo_path+'/y_test.joblib')
            except Exception as e:
                print("[ERROR] Loading validation data (y_test): " + str(e))

        return x, y, x_test, y_test

    def clear_training_data(self, repo_path, repo_name):
        # if public:
        #     repo_name = self.my_public_repo
        # else:    
        #     repo_name = self.my_private_repo
        # Remove a prefix recursively.
        for obj in self.minio_client.list_objects(repo_name, repo_path, recursive=True):
            try:
                self.minio_client.remove_object(repo_name, obj.object_name)
            except Exception as e:
                print("[ERROR] When deleting object: ", str(e))

    def create_training(self, x, y, x_test, y_test, easier_model:EasierModel, training_metadata:TrainingMetadata, public=False, namespace=None):
        # Test if model can be loaded
        if easier_model.get_model() is None:
            print("ERROR: There is no model to train")
            return None
        
        random_name = self.id_generator(size=8)
        minio_path = 'train/' + random_name

        # Pickle x and y and upload to minio
        with tempfile.TemporaryDirectory() as path:
            filename_x = os.path.join(path, 'x.joblib')
            filename_y = os.path.join(path, 'y.joblib')
            joblib.dump(x, filename_x, compress=True)
            joblib.dump(y, filename_y, compress=True)

            filename_x_test = os.path.join(path, 'x_test.joblib')
            filename_y_test = os.path.join(path, 'y_test.joblib')
            joblib.dump(x_test, filename_x_test, compress=True)
            joblib.dump(y_test, filename_y_test, compress=True)

            easier_model.set_training_metadata(training_metadata)
            
            # Upload model and set it to training state
            from easierSDK.easier import EasierSDK
            easier = EasierSDK(easier_user=self._easier_user, easier_password=self._easier_password)
            easier.models.upload(easier_model, public=public, training=True)
            
            if public:
                bucket = self.my_public_repo
            else:    
                bucket = self.my_private_repo
            
            # Create bucket if doesn't exist
            if not self.minio_client.bucket_exists(bucket): self.minio_client.make_bucket(bucket, location='es')

            # Upload training data
            for f in os.listdir(path):
                try:    
                    file_path = (minio_path + "/" + f)
                    a, b =self.minio_client.fput_object(bucket, file_path, path + '/' + f)
                except Exception as ex:
                    print('[ERROR] Unknown error uploading file {}: {}'.format(f, ex))
                    return None

        if namespace == None:
            namespace = self.namespace  
        
        # Enter a context with an instance of the API kubernetes.client
        with kubernetes.client.ApiClient() as api_client:
            # Create an instance of the API class
            api_instance = kubernetes.client.CoreV1Api(api_client)
            
            # api_instance.create_namespaced_persistent_volume_claim()

            num_pods = 1
            for i in range(num_pods):
                random_name += '-' + str(i)

                tf_config = json.dumps({
                    "cluster": {
                        "worker": ["host1:port", "host2:port", "host3:port"],
                        "ps": ["host4:port", "host5:port"]
                    },
                    "task": {"type": "worker", "index": i}
                })
                
                # config_map = None
                # with open(os.path.join(os.path.dirname(__file__), "easier-training-config_map.yaml")) as f:
                config_map = yaml.safe_load(easier_training_config_map.config_map)

                config_map['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
                config_map['data']['easier_user'] = self._easier_user
                config_map['data']['easier_password'] = self._easier_password
                config_map['data']['repo'] = bucket
                config_map['data']['category'] = easier_model.metadata.category.value
                config_map['data']['model_name'] = easier_model.metadata.name
                config_map['data']['experimentID'] = str(easier_model.metadata.version)
                config_map['data']['data_path'] = minio_path
                config_map['data']['TF_CONFIG'] = tf_config
                
                try:
                    api_response = api_instance.create_namespaced_config_map(namespace, config_map, pretty='true')
                    # print(api_response)
                except ApiException as e:
                    print("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)

                # deployment = None
                # with open(os.path.join(os.path.dirname(__file__), "easier-training-deployment.yaml")) as f:
                deployment = yaml.safe_load(easier_training_deployment.deployment)
            
                deployment['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
                deployment['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
                deployment['spec']['selector']['matchLabels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
                deployment['spec']['template']['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
                deployment['spec']['containers'][0]['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
                deployment['spec']['containers'][0]['envFrom'][0]['configMapRef']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
        
                try:
                    api_response = api_instance.create_namespaced_pod(namespace, deployment, pretty='true')
                    # print(api_response)
                except ApiException as e:
                    print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)

        return deployment['metadata']['name']

    def create_training_from_repo_model(self, x, y, repo_name:str, category:Categories, 
        model_name:str, experimentID:int, public=False, namespace=None, num_pods=4):
        
        if isinstance(category, str):
           category = Categories[category.upper()]
        
        # Test if model can be loaded
        from easierSDK.easier import EasierSDK
        easier = EasierSDK(easier_user=self._easier_user, easier_password=self._easier_password)
        easier_model = easier.models.get_model(repo_name=repo_name, category=category, model_name=model_name, experimentID=experimentID)    
        if easier_model.get_model() is None:
            print("ERROR: Could not load model " + str(model_name) +
                    " from repository " + repo_name + " and category " + category.value)
            return None
        
        # easier.models.upload(easier_model, public=public)

        random_name = self.id_generator(size=5)
        minio_path = 'train/' + random_name

        # Pickle x and y and upload to minio
        with tempfile.TemporaryDirectory() as path:
            filename_x = os.path.join(path, 'x.joblib')
            filename_y = os.path.join(path, 'y.joblib')
            joblib.dump(x, filename_x, compress=True)
            joblib.dump(y, filename_y, compress=True)


            # Upload all files in the path
            bucket = self.my_private_repo
            
            # Create bucket if doesn't exist
            if not self.minio_client.bucket_exists(bucket): self.minio_client.make_bucket(bucket, location='es')
            
            for f in os.listdir(path):
                try:    
                    file_path = (minio_path + "/" + f)
                    a, b =self.minio_client.fput_object(bucket, file_path, path + '/' + f)
                except Exception as ex:
                    print('[ERROR] Unknown error uploading file {}: {}'.format(f, ex))
                    return None

        if namespace == None:
            namespace = self.namespace  
        
        # Enter a context with an instance of the API kubernetes.client
        with kubernetes.client.ApiClient() as api_client:
            # Create an instance of the API class
            api_instance = kubernetes.client.CoreV1Api(api_client)
            
            api_instance.create_namespaced_persistent_volume_claim()


            for i in range(num_pods):
                random_name += '_' + str(i)

                tf_config = json.dumps({
                    "cluster": {
                        "worker": ["host1:port", "host2:port", "host3:port"],
                        "ps": ["host4:port", "host5:port"]
                    },
                    "task": {"type": "worker", "index": i}
                })
                
                # config_map = None
                # with open(os.path.join(os.path.dirname(__file__), "easier-training-config_map.yaml")) as f:
                config_map = yaml.safe_load(easier_training_config_map.config_map)

                config_map['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
                config_map['data']['easier_user'] = self._easier_user
                config_map['data']['easier_password'] = self._easier_password
                config_map['data']['repo'] = repo_name
                config_map['data']['category'] = category.value
                config_map['data']['model_name'] = model_name
                config_map['data']['experimentID'] = str(easier_model.metadata.version)
                config_map['data']['model_path'] = str(easier_model.metadata.version)
                config_map['data']['TF_CONFIG'] = tf_config
                
                try:
                    api_response = api_instance.create_namespaced_config_map(namespace, config_map, pretty='true')
                    # print(api_response)
                except ApiException as e:
                    print("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)

                # deployment = None
                # with open(os.path.join(os.path.dirname(__file__), "easier-training-deployment.yaml")) as f:
                deployment = yaml.safe_load(easier_training_deployment.deployment)
            
                deployment['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
                deployment['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
                deployment['spec']['selector']['matchLabels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
                deployment['spec']['template']['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
                deployment['spec']['containers'][0]['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
                deployment['spec']['containers'][0]['envFrom'][0]['configMapRef']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
        
                try:
                    api_response = api_instance.create_namespaced_pod(namespace, deployment, pretty='true')
                    # print(api_response)
                except ApiException as e:
                    print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)

                # service = None
                # with open(os.path.join(os.path.dirname(__file__), "easier-training-service.yaml")) as f:
                # service = yaml.safe_load(easier_training_service.service)
            
                # service['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
                # service['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
                # service['spec']['selector']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name

                # try:
                #     api_response = api_instance.create_namespaced_service(namespace, service, pretty='true')
                #     # print(api_response)
                # except ApiException as e:
                #     print("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)
            
                # networking_v1_beta1_api = kubernetes.client.NetworkingV1beta1Api()
                # hostname = None
                # # ingress = None
                # # with open(os.path.join(os.path.dirname(__file__), "easier-training-ingress.yaml")) as f:
                # ingress = yaml.safe_load(easier_training_ingress.ingress)
            
                # ingress['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
                # ingress['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
                # ingress['spec']['rules'][0]['host'] = model_name + '-' + 'easier-training' + '-' + self._easier_user.replace('.', '-') + '-' + random_name + '.easier-ai.eu'
                # ingress['spec']['rules'][0]['http']['paths'][0]['backend']['serviceName'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name

                # try:
                #     api_response = networking_v1_beta1_api.create_namespaced_ingress(namespace, ingress, pretty='true')
                #     # print(api_response)
                # except ApiException as e:
                #     print("Exception when calling CoreV1Api->create_namespaced_ingress: %s\n" % e)
                
                # hostname = ingress['spec']['rules'][0]['host']
                
                # if hostname:
                #     print("Your model will be served shortly in: " + str(hostname))
                # else:
                #     print("There was a problem training your model")

        return deployment['metadata']['name']

    def create_distributed_training(self, x, y, easier_model):
        raise NotImplementedError

    def delete_serving():
        raise NotImplementedError
    
    def deploy_visualization():
        raise NotImplementedError