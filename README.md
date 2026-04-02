# BUSHIDAI TRUTH SIMULATOR v0.7.0
**TRUTH == TRUTH** 🌌📊💫🦊🥋

A small, fully local Python script that can improve itself.

**This is not ChatGPT.**  
**This is not Ollama.**  
This is not a smart chatbot.

It is a neuro-symbolic experiment:

- Converts ordinary sentences into real Hyperon/MeTTa symbols  
- Checks with a small neural network if it is correct  
- Reasons with PLN + ECAN  
- Rewrites its own rules if the truth value is too low  

Everything runs locally. No server. No subscription. No black box.

### Installation
```bash
python3 -m pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install numpy sympy
How to try it
Bash# Run with the 3 default goals
python3 bushidai_truth_v0.7.0.py

# Or run with your own goals
python3 bushidai_truth_v0.7.0.py --goals "I am hungry and want truth" "What is the real governance" "Break the semantics"
Command-line options
You can control Bushidai with these options:
OptionDescriptionDefault valueExample--goalsList of sentences/goals you want to test3 built-in test goals--goals "I am hungry and want truth" "What is the real governance" "Break the semantics"--depthHow deep the reasoning goes (PLN + Hyperon)7--depth 12--budgetAttention budget for ECAN0.85--budget 0.9--verboseShow detailed output (STI/LTI, rules, etc.)True--verbose=false--statePath to the memory filebushidai_state.json--state my_memory.json
You can always see all options with:
Bashpython3 bushidai_truth_v0.7.0.py --help
Open the code. Read it. Modify it. Play with it.
Why this exists
Because it proves that things can be done differently: small, open, transparent, and self-adaptable.
Created by Thijs Smits (TS87)
Fork it. Break it. Improve it.