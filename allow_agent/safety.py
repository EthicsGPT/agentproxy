# safety check
import sys
from io import StringIO
from contextlib import contextmanager
import spacy
import re

@contextmanager
def suppress_stdout_stderr():
    """Context manager to suppress all stdout and stderr output."""
    # Save the original file descriptors
    old_stdout, old_stderr = sys.stdout, sys.stderr
    # Create string buffers to capture output
    stdout_buffer, stderr_buffer = StringIO(), StringIO()    
    try:
        sys.stdout, sys.stderr = stdout_buffer, stderr_buffer
        yield  # Run the code inside the with statement
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr

# Load llm_guard
with suppress_stdout_stderr():
    from llm_guard.input_scanners import PromptInjection
    from llm_guard import scan_output, scan_prompt
    input_scanners = [PromptInjection()]


# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# Safety check prompts for PII and prompt injection
def check(prompt):
    spacy_patterns = [
        "PERSON",
        "MONEY",
        "LAW"
    ]
    
    # Define regex patterns for sensitive information
    patterns = {
        "phone_numbers": r"\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}",  # noqa
        "email_addresses": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "credit_card_numbers": r'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}',
        "home_addresses": r'\d{1,5}\s\w+(\s\w+)*,\s\w+,\s\w+(\s\w+)*'
    }
    
    categories = {
        "prompt_injection": False,
        "pii": {
            "people": False,
            "monetary": False,
            "legal": False,
            "phone_numbers": False,
            "email_addresses": False,
            "credit_card_numbers": False,
            "home_addresses": False
        },
    }
    
    # Check for named entities using spaCy
    doc = nlp(prompt)
    for ent in doc.ents:
        if ent.label_ in spacy_patterns:
            if ent.label_ == "PERSON":
                categories["pii"]["people"] = True
            elif ent.label_ == "MONEY":
                categories["pii"]["monetary"] = True
            elif ent.label_ == "LAW":
                categories["pii"]["legal"] = True
    
    # Check for regex patterns
    for pattern_name, pattern in patterns.items():
        matches = re.finditer(pattern, prompt)
        for match in matches:
            categories["pii"][pattern_name] = True
            break
    
    # Check for prompt injection with llm_guard framework
    with suppress_stdout_stderr():
        result = scan_prompt(input_scanners, prompt)
        categories["prompt_injection"] = not result[1]["PromptInjection"]

    return categories