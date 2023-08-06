import unittest
import logging
import sys
import io
from ibm_watson_machine_learning.tests.utils import get_wml_credentials, get_cos_credentials, get_space_id
from ibm_watson_machine_learning.tests.utils.cleanup import space_cleanup
from ibm_watson_machine_learning import APIClient
from models_preparation import create_tensorflow_model_data


class TestWMLClientWithTensorflow(unittest.TestCase):
    deployment_uid = None
    model_def_uid = None
    scoring_url = None
    cos_resource_instance_id = None
    scoring_data = None
    logger = logging.getLogger(__name__)
    space_name = 'tests_sdk_space'
    model_path = 'svt/artifacts/tf-model-with-metrics_2.1.zip'

    @classmethod
    def setUpClass(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """

        cls.wml_credentials = get_wml_credentials()

        cls.wml_client = APIClient(wml_credentials=cls.wml_credentials)

        if not cls.wml_client.ICP:
            cls.cos_credentials = get_cos_credentials()
            cls.cos_endpoint = cls.cos_credentials.get('endpoint_url')
            cls.cos_resource_instance_id = cls.cos_credentials.get('resource_instance_id')

        cls.wml_client = APIClient(wml_credentials=cls.wml_credentials)
        cls.project_id = cls.wml_credentials.get('project_id')

    def test_00a_space_cleanup(self):
        space_cleanup(self.wml_client,
                      get_space_id(self.wml_client, self.space_name,
                                   cos_resource_instance_id=self.cos_resource_instance_id),
                      days_old=7)
        TestWMLClientWithTensorflow.space_id = get_space_id(self.wml_client, self.space_name,
                                                 cos_resource_instance_id=self.cos_resource_instance_id)

        # if self.wml_client.ICP:
        #     self.wml_client.set.default_project(self.project_id)
        # else:
        self.wml_client.set.default_space(self.space_id)

    def test_00b_create_tensorflow_model_definition(self):
        meta_props = {
            self.wml_client.model_definitions.ConfigurationMetaNames.NAME: "TF 2.4 Model Definition NB",
            self.wml_client.model_definitions.ConfigurationMetaNames.DESCRIPTION: "SVT Model Def Tensorflow",
            self.wml_client.model_definitions.ConfigurationMetaNames.VERSION: "1.0",
            self.wml_client.model_definitions.ConfigurationMetaNames.PLATFORM: {"name": "python", "versions": ["3.7"]}
        }

        model_def_details = self.wml_client.model_definitions.store(self.model_path, meta_props)
        TestWMLClientWithTensorflow.model_def_uid = self.wml_client.model_definitions.get_uid(model_def_details)

    def test_02_create_and_run_training(self):
        asset_details = self.wml_client.data_assets.create('tf_mnist', './svt/datasets/MNIST_DATA')
        asset_id = self.wml_client.data_assets.get_id(asset_details)

        metadata = {
            self.wml_client.training.ConfigurationMetaNames.NAME: "Tensorflow Training from Notebook",
            self.wml_client.training.ConfigurationMetaNames.DESCRIPTION: "",
            self.wml_client.training.ConfigurationMetaNames.TAGS: [
                {
                    "value": "pyclienttraining",
                    "description": "python client training"
                }
            ],
            self.wml_client.training.ConfigurationMetaNames.TRAINING_DATA_REFERENCES: [{
                "name": "training_input_data",
                "type": "data_asset",
                "connection": {},
                "location": {
                    'id': asset_id
                }
            }],
            self.wml_client.training.ConfigurationMetaNames.TRAINING_RESULTS_REFERENCE: {"name": "tf_mnist_results",
                                                                                "connection": {},
                                                                                "location": {
                                                                                    "path": "/spaces/" + str(
                                                                                        self.space_id) + "/assets/trainings"
                                                                                },
                                                                                "type": "fs"
                                                                                },
            self.wml_client.training.ConfigurationMetaNames.MODEL_DEFINITION: {
                "id": self.model_def_uid,
                "command": "convolutional_network.py --trainImagesFile train-images-idx3-ubyte.gz --trainLabelsFile train-labels-idx1-ubyte.gz --testImagesFile t10k-images-idx3-ubyte.gz --testLabelsFile t10k-labels-idx1-ubyte.gz --learningRate 0.001 --trainingIters 6000",
                "software_spec": {
                    "name": "tensorflow_2.4-py3.7"
                },
                "hardware_spec": {
                    "name": "K80",
                    "num_nodes": 1
                },
                "parameters": {
                    "name": "TF 2.4 Training from Notebook",
                    "description": "TF 2.4 training from Python Client notebook"

                }
            }
        }

        training_details = self.wml_client.training.run(meta_props=metadata, asynchronous=False)
        import json
        print(json.dumps(training_details, indent=4))
        self.assertEqual(training_details['entity']['status']['state'], 'completed')

    def test_03_delete_model_definition(self):
        TestWMLClientWithTensorflow.logger.info("Delete model definition")
        self.wml_client.repository.delete(TestWMLClientWithTensorflow.model_def_uid)



    # def test_04_load_model(self):
    #     print(TestWMLClientWithTensorflow.model_uid)
    #     TestWMLClientWithTensorflow.logger.info("Load model from repository: {}".format(TestWMLClientWithTensorflow.model_uid))
    #     self.tf_model = self.wml_client.repository.load(TestWMLClientWithTensorflow.model_uid)
    #     TestWMLClientWithTensorflow.logger.debug("TF type: {}".format(type(self.tf_model)))
    #
    # def test_05_create_deployment(self):
    #     TestWMLClientWithTensorflow.logger.info("Create deployment")
    #     deployment_details = self.wml_client.deployments.create(artifact_uid=TestWMLClientWithTensorflow.model_uid,
    #                                                         meta_props={self.wml_client.deployments.ConfigurationMetaNames.NAME: "Test deployment",
    #                                                                     self.wml_client.deployments.ConfigurationMetaNames.ONLINE: {}})
    #
    #
    #     TestWMLClientWithTensorflow.deployment_uid = self.wml_client.deployments.get_uid(deployment_details)
    #     TestWMLClientWithTensorflow.scoring_url = self.wml_client.deployments.get_scoring_href(deployment_details)
    #     self.assertTrue('online' in str(deployment_details))
    #
    # def test_06_scoring(self):
    #     TestWMLClientWithTensorflow.logger.info("Score model")
    #
    #     scoring_payload = {
    #         'input_data': [
    #             {
    #                 'values': self.scoring_data.tolist()
    #             }
    #         ]
    #     }
    #     self.wml_client.deployments.ScoringMetaNames.show()
    #     scores = self.wml_client.deployments.score(TestWMLClientWithTensorflow.deployment_uid, meta_props=scoring_payload)
    #     self.assertIsNotNone(scores)
    #
    # def test_07_list_models(self):
    #     TestWMLClientWithTensorflow.logger.info("List models")
    #     stdout_ = sys.stdout
    #     stream = io.StringIO()
    #     sys.stdout = stream
    #     self.wml_client.repository.list()
    #     sys.stdout = stdout_
    #     TestWMLClientWithTensorflow.logger.info(stream.getvalue())
    #     self.assertTrue('GUID' in stream.getvalue())
    #
    # def test_08_list_deployments(self):
    #     TestWMLClientWithTensorflow.logger.info("List deployments")
    #     stdout_ = sys.stdout
    #     stream = io.StringIO()
    #     sys.stdout = stream
    #     self.wml_client.deployments.list()
    #     sys.stdout = stdout_
    #     TestWMLClientWithTensorflow.logger.info(stream.getvalue())
    #     self.assertTrue('GUID' in stream.getvalue())
    #
    # def test_09_delete_deployment(self):
    #     TestWMLClientWithTensorflow.logger.info("Delete deployment")
    #     self.wml_client.deployments.delete(TestWMLClientWithTensorflow.deployment_uid)
    #
    # def test_10_delete_model(self):
    #     TestWMLClientWithTensorflow.logger.info("Delete model")
    #     self.wml_client.repository.delete(TestWMLClientWithTensorflow.model_uid)


if __name__ == '__main__':
    unittest.main()
