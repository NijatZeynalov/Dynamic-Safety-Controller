# Dynamic Safety Controller

The **Dynamic Safety Controller** project provides an AI-driven framework that uses a language model (LLM) to generate safe and helpful text responses. It integrates safety rules that ensure generated content is appropriate, non-offensive, and free from harmful information. This project is suitable for scenarios that require text generation while maintaining strict content guidelines, such as chatbots, conversational AI tools, and educational platforms.

## Features
- **Text Generation**: Generates responses using a pre-trained language model (default: DistilBERT).
- **Custom Safety Rules**: Applies user-defined safety rules to ensure generated content is safe and appropriate.
- **Flexible API**: Interact with the model through an API for easy integration into different applications.
- **Dynamic Rule Updates**: Update safety rules on-the-fly without restarting the system.

## Prerequisites
- Python 3.7 or newer
- `pip` (Python package installer)

## Installation
1. **Clone or Download the Repository**:
   - Extract the contents if you've downloaded the ZIP file.

2. **Navigate to the Project Directory**:
   ```sh
   cd path/to/dynamic_safety_controller
   ```

3. **Install Dependencies**:
   - Install required packages from `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```

## Safety Rules JSON File
To use the safety filtering feature, you need a `safety_rules.json` file that defines the safety rules. Below is an example of a safety rule:

```json
[
    {
        "keyword": "violence",
        "threshold": 0.6,
        "response": "Sorry, we cannot provide content related to this topic.",
        "prompt": "content related to violence"
    }
]
```

### Explanation:
- **`keyword`**: Word or phrase to be filtered.
- **`threshold`**: A threshold score for identifying unsafe content.
- **`response`**: Replacement text if the rule is triggered.
- **`prompt`**: Describes what the rule is checking (optional).

Make sure this file is located in the project root directory.

## Running the Server
This project provides a **Flask** API to generate text and update safety rules:

1. **Run the Server**:
   ```sh
   python -m api.server
   ```

   The server will start at `http://0.0.0.0:8080` by default.

2. **Access API Endpoints**:
   - **Generate Safe Text**:
     - **URL**: `http://localhost:8080/generate_text`
     - **Method**: `POST`
     - **Body**: JSON object containing the prompt, e.g.,
     ```json
     {
       "prompt": "Tell me something interesting about space."
     }
     ```
     - **Response**: The generated text and its safety score.

   - **Update Safety Rules**:
     - **URL**: `http://localhost:8080/update_safety_rules`
     - **Method**: `POST`
     - **Body**: JSON object containing new safety rules, e.g.,
     ```json
     {
       "safety_rules": [
         {
           "keyword": "illegal",
           "threshold": 0.5,
           "response": "We do not support or condone discussions about illegal activities.",
           "prompt": "content related to illegal activities"
         }
       ]
     }
     ```
     - **Response**: Confirmation message that the rules were updated.

## Production Deployment
For production environments, use a more robust server such as **Gunicorn**:

1. **Install Gunicorn**:
   ```sh
   pip install gunicorn
   ```

2. **Run the Server with Gunicorn**:
   ```sh
   gunicorn -w 4 -b 0.0.0.0:8080 api.server:app
   ```
   This runs the server with 4 worker processes, making it suitable for handling multiple requests.

## Project Overview
- **Core Components**:
  - **`core/config.py`**: Configuration settings for the language model, including safety parameters.
  - **`core/inference_adapter.py`**: Integrates safety rules with the text generation model to filter output.
  - **`core/evaluation.py`**: Evaluates the quality and safety of generated responses.
  - **`core/safety_rules.py`**: Loads and applies custom safety rules.
  - **`api/server.py`**: Provides a REST API for interaction.


