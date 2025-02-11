import os
import anthropic
from dotenv import load_dotenv
from src.utils import create_midi_from_text
from traceback import format_exc
import copy

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


def get_anthropic_results(messages, system_prompt=[], model="claude-3-5-sonnet-20241022", max_tokens=4096, temperature=0, api_key=None):
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=messages,
        system=system_prompt
    )
    return message.content


def generate_midi_text(prompt, system_prompt, context=[], api_key=None):
    messages = []
    for prev_output in context:
        messages.append({"role": "assistant", "content": prev_output})
    messages.append({"role": "user", "content": prompt})
    return get_anthropic_results(messages, system_prompt, api_key=api_key)

def create_ai_midi(prompt, system_prompt, export_path, filename, tempo=120,
                time_signature=(4, 4), context=[], api_key=None, curr_chunk_id=None, full_num_chunks=None):
    """Generate MIDI text using Claude API and create a MIDI file."""

    if curr_chunk_id is not None:
        prompt = f"{prompt}\n\n This works will have {full_num_chunks} parts. This is part {curr_chunk_id} of {full_num_chunks} of the loop. Write the current loop with the exact requested bar length and make sure it fits the larger narrative of the piece."

    if context:
        prompt = f"{prompt}\n\n To help you generate a better high quality output, we provide the previous pieces of the loop as context:"
        for prev_output in context:
            prompt += f"\n\n{prev_output}"
            prompt += "\n\n"


    # print("!!!! prompt: ", prompt)
    # print("!!!! system prompt: ", system_prompt)
        
    LLM_out = generate_midi_text(prompt, system_prompt, context, api_key=api_key)
    midi_text = LLM_out[0].text
    
    # The generated text should already be clean, but let's ensure it
    midi_lines = [line for line in midi_text.split('\n') if line.strip()]
    cleaned_midi_text = '\n'.join(midi_lines)


    text_export_path = os.path.join(export_path, f"{filename}.txt")
    #export text to file
    with open(text_export_path, 'w') as file:
        file.write(cleaned_midi_text)

    midi_export_path = os.path.join(export_path, f"{filename}.mid")
    

    print("!!!! cleaned midi text: ", cleaned_midi_text)
    print("!!!! Tempo: ", tempo)
    print("!!!! Time signature: ", time_signature)
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

        # from src.prompts.melody_prompt_v01 import prompt, system_prompt, tempo, time_signature, per_file_length
        # from src.prompts.drums_prompt_v01 import prompt, system_prompt, tempo, time_signature
        # from src.prompts.chord_prompt_v01 import prompt, system_prompt, tempo, time_signature
        # from src.prompts.bassline_prompt_v01 import prompt, system_prompt, tempo, time_signature, per_file_length
        from src.prompts.twin_peaks_sunset.drums_prompt_v01 import prompt, system_prompt, tempo, time_signature, per_file_length
        EXPORT_PATH = os.path.join('.', 'MIDI_files_v02', 'twin_peaks_sunset')
        os.makedirs(EXPORT_PATH, exist_ok=True)

        
        n = 1  # Expected number of MIDI output files
        k = 0  # Batch size for context
        piece_name = find_name_from_prompt_with_ai(prompt)
        current_path = os.path.join(EXPORT_PATH, piece_name)
        os.makedirs(current_path, exist_ok=True)
        
        context = []
        for i in range(n):
            current_prompt = copy.deepcopy(prompt)

            # adage = f"""The full piece will consists of {n} parts each with {per_file_length} bars in length. This is part {i+1}. 
            # At each iteration, we are providing you with the previous {k} parts of the piece as context below. Use this information to create a coherent and evolving loop which 
            # Can sum into a full, cohesive piece.
            # """

            adage = "The loop will consists of 1 part with 8 bars in length. You are working on the single part."

            current_prompt = f"{adage}\n\n{current_prompt}"
            filename_prefix = f"{i+1}"
            export_name = f"{filename_prefix}"
            # if file already exists, read text from file and add to context
            if os.path.exists(os.path.join(current_path, f"{export_name}.mid")):
                with open(os.path.join(current_path, f"{export_name}.txt"), 'r') as file:
                    context.append(file.read())
                    print(f"File {export_name} already exists. Adding to context and skipping generation.")
            else:
                midi_text = create_ai_midi(current_prompt, system_prompt, current_path, export_name, tempo, time_signature, context=context[-k:])
                context.append(midi_text)
            
    except anthropic.APIError as e:
        print(f"An error occurred while calling the Anthropic API: {e}")
        # print out the full traceback
        print(f"Full traceback: {format_exc()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 
        print(f"Full traceback: {format_exc()}")
