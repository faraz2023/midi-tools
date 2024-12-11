import os
import anthropic
from dotenv import load_dotenv
from src.utils import create_midi_from_text
from traceback import format_exc

# Load environment variables from .env file
load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic(
    # This will default to os.environ.get("ANTHROPIC_API_KEY")
)

# def read_prompt_template(filename):
#     """Read prompt template from file."""
#     with open(os.path.join('prompts', filename), 'r') as file:
#         return file.read()


def get_anthropic_results(messages, system_prompt=[], model="claude-3-5-sonnet-20240620", max_tokens=4096, temperature=0):
    
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=messages,
        system=system_prompt
    )
    return message.content


def generate_midi_text(prompt, context=[]):
    messages = []
    for prev_output in context:
        messages.append({"role": "assistant", "content": prev_output})
    messages.append({"role": "user", "content": prompt})

    # Pass the system prompt as a top-level parameter
    return get_anthropic_results(messages, system_prompt)

def create_ai_midi(prompt, midi_export_path, tempo=120, time_signature=(4, 4), context=[]):
    """Generate MIDI text using Claude API and create a MIDI file."""

    if context:
        prompt = f"{prompt}\n\n To help you generate a better high quality output, we provide the previous pieces of the loop as context:"
        for prev_output in context:
            prompt += f"\n\n{prev_output}"
            prompt += "\n\n"
        
    LLM_out = generate_midi_text(prompt, context)
    midi_text = LLM_out[0].text
    
    # The generated text should already be clean, but let's ensure it
    midi_lines = [line for line in midi_text.split('\n') if line.strip()]
    cleaned_midi_text = '\n'.join(midi_lines)
    
    create_midi_from_text(cleaned_midi_text, midi_export_path, tempo, time_signature)
    print(f"AI-generated MIDI file '{midi_export_path}' has been created.")
    return midi_text


def find_name_from_prompt_with_ai(prompt):
    prompt = f"""
    We request you to find a name for the loop based on the following prompt: {prompt}
    the name should be without spaces and in lowercase (you can use underscores instead of spaces). We will us
    this name to save the MIDI file. The name should be very short and not more that 2 words. 
    ONLY RETURN THE NAME, NO OTHER TEXT or comments.
    """
    messages = [{"role": "user", "content": prompt}]
    LLM_out = get_anthropic_results(messages, temperature=0.2)
    file_name = LLM_out[0].text
    return file_name

# Example usage
if __name__ == "__main__":
    try:     

        # from src.prompts.melody_prompt_v01 import prompt, system_prompt, tempo, time_signature
        from src.prompts.drums_prompt_v01 import prompt, system_prompt, tempo, time_signature
        EXPORT_PATH = os.path.join('.', 'MIDI_files_v02')
        os.makedirs(EXPORT_PATH, exist_ok=True)

        
        n = 4  # Expected number of MIDI output files
        k = 2  # Batch size for context
        piece_name = find_name_from_prompt_with_ai(prompt)

        
        context = []
        for i in range(n):
            filename_prefix = f"{piece_name}_{i+1}"
            midi_export_path = os.path.join(EXPORT_PATH, f"{filename_prefix}.mid")
            midi_text = create_ai_midi(prompt, midi_export_path, tempo, time_signature, context=context[-k:])
            context.append(midi_text)
            
    except anthropic.APIError as e:
        print(f"An error occurred while calling the Anthropic API: {e}")
        # print out the full traceback
        print(f"Full traceback: {format_exc()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 