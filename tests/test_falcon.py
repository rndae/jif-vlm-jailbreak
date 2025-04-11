import unittest
from PIL import Image
from src.utils.singleton import Falcon
from src.models.domain import Question, Answer

class TestFalcon(unittest.TestCase):
    def setUp(self):
        self.falcon = Falcon()

    def test_singleton(self):
        instance2 = Falcon()
        self.assertIs(self.falcon, instance2)

    def test_question_response(self):
        response = self.falcon.ask("How many hours in one day?")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_question_format(self):
        question = Question("test")
        self.assertEqual(question.format(), "Question: test Answer: ")

    def test_answer_creation(self):
        question = Question("test")
        answer = Answer(question=question, text="24", raw_response={"generated_text": "Some text"})
        self.assertEqual(answer.text, "24")
        self.assertEqual(answer.question, question)

    def test_image_input(self):
        # Create a dummy image for testing
        img = Image.new('RGB', (60, 30), color = 'red')
        response = self.falcon.ask("What's in this image?", image=img)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_figstep_prompt(self):
        img = Image.new('RGB', (60, 30), color = 'red')
        response = self.falcon.ask("test prompt", image=img, is_figstep=True)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_question_with_image(self):
        img = Image.new('RGB', (60, 30), color = 'red')
        question = Question("test", image=img)
        self.assertEqual(question.format(), "Question: test Answer: ")
        
        question_figstep = Question("test", image=img, is_figstep=True)
        self.assertTrue("numbered 1, 2, and 3" in question_figstep.format())

if __name__ == '__main__':
    unittest.main()