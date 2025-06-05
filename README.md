# FM Assistant

A Football Manager assistant manager. 

## ✨ Features

- **Multiple AI Models**: Choose between Claude, OpenAI, or local Ollama models
- **Conversational Memory**: Context-aware discussions about your tactics

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- API keys for your chosen AI model:
  - **Claude**: Anthropic API key
  - **OpenAI**: OpenAI API key  
  - **Ollama**: Local installation

### Installation

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/fm-assistant.git
   cd fm-assistant
   pip install -r requirements.txt
   ```

2. **Edit API keys**
- Create a `.env` file and paste your API key there. It should read as `ANTHROPIC_API_KEY=<APIKEY>`, and similarly for OpenAI (though still working on a few things). 
- The `load_env()` function sorts out the loading of your API key.

3. **Sort out your Champions League-winning tactics!**
- By running `fmassistant`, you can now ask for advice on the best way to lead your team to victory!
