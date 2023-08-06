import unittest

from mdg.parse import parse
from mdg.validate import validate_package
from mdg.render import output_model


class TestSample_DrawIO_Django(unittest.TestCase):
    def setUp(self):
        # Env must be set before tests
        # self.recipie_path = './sample_recipie' + "/config-test.yaml"
        # os.environ.setdefault("PYMDG_SETTINGS_MODULE", self.recipie_path)

        self.model_package, self.test_cases = parse()

    def test_parse(self):
        self.assertEqual("SampleIndustry", self.model_package.name)

    def test_validate(self):
        # Deliberate error in test config
        errors = validate_package(self.model_package)
        self.assertEquals(len(errors), 1)

    def test_render_model(self):
        self.assertGreater(len(self.model_package.children), 0)
        # Test config has built in failure no child packages will be rendered
        self.assertRaises(ValueError, output_model, self.model_package)

        # Manually go to child package
        self.assertRaises(ValueError, output_model, self.model_package.children[0])
