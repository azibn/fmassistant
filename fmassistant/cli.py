import sys
from fmassistant.assistant import MODELS
import argparse
from tqdm import tqdm
import time
import random
import threading
import os
import itertools
import readline 


def show_banner():
    print("""
    ────────────────────────────────────────────────────────────
    
     ███████╗███╗   ███╗    ████████╗ █████╗  ██████╗████████╗██╗ ██████╗███████╗
     ██╔════╝████╗ ████║    ╚══██╔══╝██╔══██╗██╔════╝╚══██╔══╝██║██╔════╝██╔════╝
     █████╗  ██╔████╔██║       ██║   ███████║██║        ██║   ██║██║     ███████╗
     ██╔══╝  ██║╚██╔╝██║       ██║   ██╔══██║██║        ██║   ██║██║     ╚════██║
     ██║     ██║ ╚═╝ ██║       ██║   ██║  ██║╚██████╗   ██║   ██║╚██████╗███████║
     ╚═╝     ╚═╝     ╚═╝       ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝╚══════╝
    
      Football Manager Tactical Assistant  
    
    ┌─────────────────────────────────────────────────────────────┐
    │  "19 goals in 40 games, do the maths that's a goal a game"  │
    │   - Eni Aluko                                               │  
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
    
    ⚪ Available Models: Claude | OpenAI | Ollama
    ⚪ Ask tactical questions for your FM setup
    ⚪ Commands: 'switch' | 'exit'
    
    ────────────────────────────────────────────────────────────

    """)



def setup_readline():
    """Setup readline with history"""

    history_file = os.path.expanduser("~/.fm_assistant_history")
    
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass 
    
    import atexit
    atexit.register(readline.write_history_file, history_file)
    
    readline.set_history_length(100)

def show_spinner(stop_event):
    """Show spinning animation"""
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while not stop_event.is_set():
        print(f"\r{next(spinner)} Thinking...", end='', flush=True)
        time.sleep(0.1)

def fm_assistant_ui(backend):
    setup_readline()
    show_banner()
    #print(f"=== FM Assistant ({backend.upper()}) ===")
    #print("Ask me anything about Football Manager tactics!")
    print("Type 'switch' to change AI model, 'exit' to quit.\n")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in {"exit", "quit"}:
                print("Good luck with your tactics!")
                break
            elif user_input.lower() == "switch":
                print("Available models:", ", ".join(MODELS.keys()))
                new_backend = input("Choose model: ").strip().lower()
                if new_backend in MODELS:
                    backend = new_backend
                    print(f"Switched to {backend.upper()}\n")
                else:
                    print("Invalid model. Staying with", backend.upper())
                continue
            
            if not user_input:
                continue
            
            # Add user message to history
            conversation_history.append({"role": "user", "content": user_input})
            
            # Start spinner
            stop_spinner = threading.Event()
            spinner_thread = threading.Thread(target=show_spinner, args=(stop_spinner,))
            spinner_thread.daemon = True
            spinner_thread.start()


            try:

                stop_spinner.set()
                spinner_thread.join(timeout=0.002)
                print("\r" + " " * 30, end='')  # Clear spinner line
                print("\r", end='', flush=True)

                response = MODELS[backend](conversation_history)
                print(f"\nFM Assistant: {response}\n")
              

                
                # Add assistant response to history
                conversation_history.append({"role": "assistant", "content": response})
                
            except Exception as model_error:

                stop_spinner.set()
                spinner_thread.join(timeout=0.5)
                print("\r" + " " * 30, end='')
                print("\r", end='', flush=True)
                print(f"Error with {backend}: {model_error}")
                print("Try switching to a different model.\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="claude", choices=MODELS.keys())
    args = parser.parse_args()
    fm_assistant_ui(backend=args.model)


if __name__ == "__main__":
    main()
    
