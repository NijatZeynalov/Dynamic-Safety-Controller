
class Config:
    """
    Configuration settings for the Dynamic Safety Controller.
    """
    def __init__(self):
        self.model_name: str = "distilbert-base-uncased"
        self.safety_rules_path: str = "safety_rules.json"
        self.api_port: int = 8080
        self.max_tokens: int = 100
        self.temperature: float = 0.7
        self.top_p: float = 0.9
        self.top_k: int = 50
        self.safety_score_threshold: float = 0.5

        # Validation
        assert isinstance(self.api_port, int) and 0 < self.api_port < 65535, "API port must be a valid port number"
        assert 0.0 <= self.temperature <= 1.0, "Temperature must be between 0 and 1"
        assert 0.0 <= self.top_p <= 1.0, "Top-p must be between 0 and 1"
        assert self.max_tokens > 0, "Max tokens must be a positive integer"
