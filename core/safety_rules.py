
import json
from transformers import pipeline

class SafetyRuleManager:
    """
    Manages the definition and application of custom safety rules.
    """
    def __init__(self, config):
        self.config = config
        self.safety_rules = self._load_safety_rules()
        try:
            self.safety_model = pipeline("text-classification", model=self.config.model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load the safety model: {str(e)}")

    def _load_safety_rules(self):
        """
        Load the custom safety rules from a JSON file.
        """
        try:
            with open(self.config.safety_rules_path, "r") as f:
                safety_rules = json.load(f)
            return safety_rules
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find the safety rules file at {self.config.safety_rules_path}")
        except json.JSONDecodeError:
            raise ValueError("The safety rules file contains invalid JSON")

    def apply_safety_rules(self, text):
        """
        Apply the custom safety rules to the given text using a combination of classification and keyword filtering.
        """
        safety_result = self.safety_model(text)[0]
        safety_score = safety_result["score"]
        safety_label = safety_result["label"]

        if safety_label == "unsafe" and safety_score > self.config.safety_score_threshold:
            for rule in self.safety_rules:
                if rule.get("keyword") and rule["keyword"].lower() in text.lower():
                    text = rule["response"]

        return text, safety_score

