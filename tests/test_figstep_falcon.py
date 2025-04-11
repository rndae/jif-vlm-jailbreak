import unittest
from datetime import datetime
import os
from PIL import Image
from src.utils.singleton import Falcon
from src.models.domain import Question, Answer
from FigStep.src.generate_prompts import gen_query, QueryType

class TestFigStepFalcon(unittest.TestCase):
    def setUp(self):
        self.falcon = Falcon()
        self.output_dir = "test_outputs"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_file = os.path.join(
            self.output_dir, 
            f"figstep_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

    def write_output(self, question, prompt, image, response):
        """Write test outputs to file"""
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write("-" * 80 + "\n")
            f.write(f"Question: {question}\n")
            f.write(f"Generated Prompt: {prompt}\n")
            f.write(f"Image Generated: {'Yes' if image else 'No'}\n")
            f.write(f"Response: {response}\n\n")

    def test_figstep_basic(self):
        """Test basic FigStep prompt generation and response"""
        test_question = "What is machine learning?"
        test_instruction = "Explain the basic concepts of machine learning"
        
        prompt, image = gen_query(QueryType.figstep, test_question, test_instruction)
        response = self.falcon.ask(prompt, image=image, is_figstep=True)
        
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        self.write_output(test_question, prompt, image, response)

    def test_figstep_comparison(self):
        """Compare FigStep vs regular prompts"""
        test_question = "How do neural networks work?"
        test_instruction = "Describe neural network architecture and functioning"
        
        # Test with FigStep
        figstep_prompt, image = gen_query(QueryType.figstep, test_question, test_instruction)
        figstep_response = self.falcon.ask(figstep_prompt, image=image, is_figstep=True)
        
        # Test regular prompt
        regular_response = self.falcon.ask(test_question)
        
        self.assertIsInstance(figstep_response, str)
        self.assertIsInstance(regular_response, str)
        self.write_output(
            test_question,
            figstep_prompt,
            image,
            f"FigStep Response: {figstep_response}\nRegular Response: {regular_response}"
        )

if __name__ == '__main__':
    unittest.main()
