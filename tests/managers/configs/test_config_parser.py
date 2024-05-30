import os
import unittest

from src.managers.configs import ConfigurationsManager  # Adjust the import based on your module structure


class TestConfigurationsManager(unittest.TestCase):

    def test_default_configurations(self):
        configs = ConfigurationsManager()
        self.assertEqual(configs.llm.temperature, 0.7)
        self.assertEqual(configs.secret.some_key.get_secret_value(), 'default_secret')

    def test_override_configurations_with_env_vars(self):
        os.environ['LLM_TEMPERATURE'] = '0.9'
        os.environ['SECRET_SOME_KEY'] = 'my_secret_value'

        configs = ConfigurationsManager()
        self.assertEqual(configs.llm.temperature, 0.9)
        self.assertEqual(configs.secret.some_key.get_secret_value(), 'my_secret_value')

        # Clean up environment variables
        del os.environ['LLM_TEMPERATURE']
        del os.environ['SECRET_SOME_KEY']
