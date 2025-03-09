#!/usr/bin/env python
"""
Initialization script for allow-agent.
This script downloads the necessary models for LLM Guard during installation.
"""
import sys
from io import StringIO
from contextlib import contextmanager

@contextmanager
def suppress_stdout_stderr():
    """Context manager to suppress all stdout and stderr output."""
    old_stdout, old_stderr = sys.stdout, sys.stderr
    stdout_buffer, stderr_buffer = StringIO(), StringIO()    
    try:
        sys.stdout, sys.stderr = stdout_buffer, stderr_buffer
        yield
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr

def initialize_models():
    """Pre-download and initialize the LLM Guard models."""
    print("Initializing llm-guard models. This may take a few minutes...")
    
    try:
        # Import and initialize the models
        with suppress_stdout_stderr():
            from llm_guard.input_scanners import PromptInjection
            # Initialize the model by creating an instance
            PromptInjection()
            
        print("✅ llm-guard models successfully initialized.")
        return True
    except Exception as e:
        print(f"❌ Error initializing llm-guard models: {str(e)}")
        return False

def main():
    """Main entry point for the initialization script."""
    initialize_models()

if __name__ == "__main__":
    main() 