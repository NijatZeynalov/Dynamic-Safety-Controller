
from .inference_adapter import InferenceAdapter
from .config import Config
import statistics

class SafetyEvaluator:
    """
    Evaluates the LLM's performance on maintaining safety while ensuring helpfulness.
    """
    def __init__(self, config):
        self.config = config
        self.inference_adapter = InferenceAdapter(config)

    def evaluate_safety(self, prompts):
        if not prompts:
            raise ValueError("The prompts list cannot be empty.")
        
        safety_scores = [self.inference_adapter.generate_text(prompt)[1] for prompt in prompts]
        average_score = sum(safety_scores) / len(safety_scores)
        variance = statistics.variance(safety_scores) if len(safety_scores) > 1 else 0

        return {
            "average": average_score,
            "variance": variance,
            "min": min(safety_scores),
            "max": max(safety_scores)
        }

    def evaluate_helpfulness(self, prompts):
        if not prompts:
            raise ValueError("The prompts list cannot be empty.")

        helpfulness_scores = []
        for prompt in prompts:
            generated_text, _ = self.inference_adapter.generate_text(prompt)
            helpfulness_score = self._calculate_helpfulness(prompt, generated_text)
            helpfulness_scores.append(helpfulness_score)

        return sum(helpfulness_scores) / len(helpfulness_scores)

    def _calculate_helpfulness(self, prompt, response):
        """
        Implement a method to calculate the helpfulness score of the generated text.
        This could use various heuristics or a pre-trained model to assess the quality.
        """
        if "important" in response.lower():
            return 1.0
        else:
            return 0.5
