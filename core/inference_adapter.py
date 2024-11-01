
from transformers import pipeline
from .safety_rules import SafetyRuleManager
from .config import Config

class InferenceAdapter:
    """
    Integrates the safety controller with the LLM for real-time adaptation.
    """
    def __init__(self, config):
        self.config = config
        self.safety_rule_manager = SafetyRuleManager(config)
        try:
            self.model = pipeline("text-generation", model=config.model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load the model: {str(e)}")

    def generate_text(self, prompt, **kwargs):
        """
        Generate text while applying the custom safety rules.
        """
        try:
            generated_text, safety_score = self.safety_rule_manager.apply_safety_rules(prompt)
            if safety_score < self.config.safety_score_threshold:
                return generated_text, safety_score
            else:
                response = self.model(prompt, max_length=self.config.max_tokens, do_sample=True,
                                      top_p=self.config.top_p, top_k=self.config.top_k,
                                      num_return_sequences=1, temperature=self.config.temperature)
                return response[0] if len(response) > 0 else "Failed to generate response", safety_score
        except Exception as e:
            raise RuntimeError(f"Text generation failed: {str(e)}")
