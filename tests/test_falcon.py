import unittest
from src.utils.singleton import Singleton
from src.models.falcon import FalconModel

class TestFalconModel(unittest.TestCase):

    def test_singleton(self):
        instance1 = Singleton.get_instance()
        instance2 = Singleton.get_instance()
        self.assertIs(instance1, instance2, "Singleton instances are not the same!")

    def test_falcon_model_response(self):
        model = FalconModel()
        response = model.generate_response("What is the capital of France?")
        self.assertIsInstance(response, str, "Response should be a string.")
        self.assertEqual(response, "Paris", "Response should be 'Paris'.")

if __name__ == '__main__':
    unittest.main()