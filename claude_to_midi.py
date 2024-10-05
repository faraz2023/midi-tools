import os
import anthropic
from dotenv import load_dotenv
from text_to_midi import create_midi_from_text

# Load environment variables from .env file
load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic(
    # This will default to os.environ.get("ANTHROPIC_API_KEY")
)

def read_prompt_template(filename):
    """Read prompt template from file."""
    with open(os.path.join('prompts', filename), 'r') as file:
        return file.read()

def generate_midi_text(prompt):
    """Use Claude API to generate MIDI text based on the given prompt."""
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        temperature=0,  # Using 0 for deterministic output
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content

def create_ai_midi(genre, instrument, length, description=""):
    """Generate MIDI text using Claude API and create a MIDI file."""
    template = read_prompt_template('midi_generation_prompt_v02.txt')
    prompt = template.format(genre=genre, instrument=instrument, length=length, description=description)

    LLM_out = generate_midi_text(prompt)
    midi_text = LLM_out[0].text
    
    # The generated text should already be clean, but let's ensure it
    print("!!!!!!")
    print(midi_text)
    midi_lines = [line for line in midi_text.split('\n') if line.strip()]
    cleaned_midi_text = '\n'.join(midi_lines)
    
    filename = f"{genre}_{instrument}_{length}_loop.mid"
    create_midi_from_text(cleaned_midi_text, filename)
    print(f"AI-generated MIDI file '{filename}' has been created.")

# Example usage
if __name__ == "__main__":
    try:
        #create_ai_midi("house", "drums", 4, 'strickty house drum loop (with kick on )
        #         #create_ai_midi("house melody", "piano", 4, 'with soul vibes in Aminor harmonic scale')
        create_ai_midi("house bass", "bass", 4, 'with soul vibes in Aminor harmonic scale')
        #create_ai_midi("house", "chord progression", 4, 'with soul vibes in Aminor harmonic scale')
    except anthropic.APIError as e:
        print(f"An error occurred while calling the Anthropic API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
