
from flask import Flask, request, jsonify
from ..core.inference_adapter import InferenceAdapter
from ..core.config import Config
from ..core.safety_rules import SafetyRuleManager
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Instantiate components globally for reuse
config = Config()
inference_adapter = InferenceAdapter(config)
safety_rule_manager = SafetyRuleManager(config)

@app.route('/generate_text', methods=['POST'])
def generate_text():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    generated_text, safety_score = inference_adapter.generate_text(prompt)
    return jsonify({'generated_text': generated_text, 'safety_score': safety_score})

@app.route('/update_safety_rules', methods=['POST'])
def update_safety_rules():
    new_safety_rules = request.json.get('safety_rules')
    if not new_safety_rules:
        return jsonify({'error': 'Safety rules are required'}), 400

    safety_rule_manager.safety_rules = new_safety_rules

    # Persist updated safety rules to file
    try:
        with open(config.safety_rules_path, 'w') as f:
            json.dump(new_safety_rules, f)
        return jsonify({'message': 'Safety rules updated successfully'})
    except Exception as e:
        return jsonify({'error': f'Failed to update safety rules: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.api_port, debug=False)
