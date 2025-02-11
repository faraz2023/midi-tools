import gradio as gr
import os
import importlib
from claude_to_midi_v02 import create_ai_midi, find_name_from_prompt_with_ai
from midi_concat import concatenate_midis
import tempfile
import anthropic
from src.utils import create_midi_from_text
import time
import subprocess
from midi2audio import FluidSynth

# Define available loop types and their associated prompt modules
loop_types = {
    "bassline": "src.prompts_gradio.bassline_prompt_v01",
    "chords": "src.prompts_gradio.chord_prompt_v01",
    "melody": "src.prompts_gradio.melody_prompt_v01",
    "drums": "src.prompts_gradio.drums_prompt_v01"
}

SOUNDFONTS = {
    "piano": "soundfonts/piano.sf2",  # You'll need to provide appropriate soundfont files
    "drums": "soundfonts/drums.sf2"
}

def midi_to_audio(midi_path, instrument_type="piano"):
    """Convert MIDI to audio using FluidSynth"""
    output_path = midi_path.replace('.mid', '.mp3')
    fs = FluidSynth(sound_font=SOUNDFONTS[instrument_type])
    fs.midi_to_audio(midi_path, output_path)
    return output_path

def load_loop_defaults(loop_type):
    """Load default values for selected loop type"""
    module = importlib.import_module(loop_types[loop_type])
    return_dict = {
        'output_type': module.defaults['output_type'],
        'instrument': module.defaults['instrument'],
        'per_file_length': module.defaults['per_file_length'],
        'tempo': module.defaults['tempo'],
        'time_signature_num': module.defaults['time_signature'][0],
        'time_signature_den': module.defaults['time_signature'][1],
        'key': module.defaults['key'],
        'genre': module.defaults['genre'],
        'description': module.defaults['description'],
        'n_chunks': 1,
        'k_context': 0
    }
    return return_dict


def generate_midi(api_key, loop_type, output_type, instrument, per_file_length, tempo, 
                 time_signature_num, time_signature_den, key, genre, description, 
                 n_chunks, k_context, instrument_type, progress=gr.Progress()):
    
    if not api_key:
        raise gr.Error("Please enter your Anthropic API key")
    
    try:
        output_dir = os.path.join(os.getcwd(), "gradio_output_midi")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Create temp workspace
        with tempfile.TemporaryDirectory() as tmpdir:
            # Initialize client with user-provided API key
            client = anthropic.Anthropic(api_key=api_key)
            
            # Load the prompt module
            prompt_module = importlib.import_module(loop_types[loop_type])
            
            # Create time signature tuple
            time_signature = (int(time_signature_num), int(time_signature_den))


            
            # Generate system prompt and user prompt using the current parameters
            system_prompt = prompt_module.get_system_prompt(
                output_type=output_type,
                per_file_length=per_file_length,
                genre=genre,
                instrument=instrument,
                tempo=tempo,
                time_signature=time_signature,
                key=key
            )
            
            base_prompt = prompt_module.get_prompt(
                output_type=output_type,
                instrument=instrument,
                per_file_length=per_file_length,
                tempo=tempo,
                time_signature=time_signature,
                key=key,
                genre=genre,
                description=description
            )


            # Create MIDI files
            midi_files = []
            context = []
            for i in range(n_chunks):
                progress((i+1)/n_chunks, desc=f"Creating chunk {i+1}/{n_chunks}")
                
                # Generate MIDI
                context_i = min(i, k_context)
                midi_text = create_ai_midi(
                    prompt=base_prompt,
                    system_prompt=system_prompt,
                    export_path=tmpdir,
                    filename=str(i+1),
                    tempo=tempo,
                    time_signature=(int(time_signature_num), int(time_signature_den)),
                    context=context[-context_i:],
                    api_key=api_key,
                    curr_chunk_id=i+1,
                    full_num_chunks=n_chunks
                )
                context.append(midi_text)
                midi_files.append(os.path.join(tmpdir, f"{i+1}.mid"))
            
            # Concatenate MIDI files
            temp_final_path = os.path.join(tmpdir, "final.mid")
            # print("number of files in tmpdir: ", len(os.listdir(tmpdir)))
            # print("List of files in tmpdir: ", os.listdir(tmpdir))
            concatenate_midis(tmpdir)

            timestamp = int(time.time())

            final_midi_filename = f"{output_type}_{timestamp}.mid"
            final_txt_filename = f"{output_type}_{timestamp}.txt"
            final_audio_filename = f"{output_type}_{timestamp}.mp3"
            
            final_midi_path = os.path.join(output_dir, final_midi_filename)
            final_txt_path = os.path.join(output_dir, final_txt_filename)
            final_audio_path = os.path.join(output_dir, final_audio_filename)

            
            final_filename = f"{output_type}_{timestamp}.mid"
            final_path = os.path.join(output_dir, final_filename)
            
            # Copy the file from temp directory to permanent location
            import shutil
            shutil.copy2(temp_final_path, final_midi_path)
            
            # Create concatenated text file
            all_text = []
            for i in range(n_chunks):
                with open(os.path.join(tmpdir, f"{i+1}.txt"), 'r') as f:
                    all_text.append(f.read())
            
            with open(final_txt_path, 'w') as f:
                f.write("\n\n".join(all_text))
            
            # Generate audio preview
            audio_path = midi_to_audio(final_midi_path, instrument_type)
            
            return final_midi_path, final_txt_path, audio_path
            
    except Exception as e:
        raise gr.Error(f"Generation failed: {str(e)}")

# Custom CSS for retro aesthetic
css = """
#title {
    text-align: center;
    font-family: 'Comic Sans MS', cursive;
    font-size: 3em !important;
    color: #ff6b6b;
    text-shadow: 2px 2px #ffd93d;
    background: linear-gradient(45deg, #ff6b6b, #ffd93d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 20px 0;
}
.vintage-box {
    border: 3px solid #4a4a4a !important;
    border-radius: 10px !important;
    padding: 20px !important;
    background: #f0e6d3 !important;
}
"""

with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
    gr.HTML("<h1 id='title'>Dr. Khoshbakhtian's Cabinet of Familiar Tunes</h1>")
    
    with gr.Row():
        api_key = gr.Textbox(label="🔑 Anthropic API Key", placeholder="Enter your API key here...", type="password")
    
    with gr.Row():
        with gr.Column(scale=1, variant="vintage-box"):
            loop_type = gr.Dropdown(choices=list(loop_types.keys()), label="Loop Type", value="drums")
            
            with gr.Accordion("Composition Parameters", open=True):  # Changed to open by default
                output_type = gr.Textbox(label="Output Type", interactive=True)
                instrument = gr.Textbox(label="Instrument", interactive=True)
                per_file_length = gr.Number(label="Chunk Length (bars)", precision=0, interactive=True)
                tempo = gr.Number(label="Tempo (BPM)", precision=0, interactive=True)
                time_signature_num = gr.Number(label="Time Signature Numerator", precision=0, interactive=True)
                time_signature_den = gr.Number(label="Time Signature Denominator", precision=0, interactive=True)
                key = gr.Textbox(label="Key", interactive=True)
                genre = gr.Textbox(label="Genre", lines=2, interactive=True)
                description = gr.Textbox(label="Description", lines=4, interactive=True)
                n_chunks = gr.Number(label="Number of Chunks", value=1, precision=0, interactive=True)
                k_context = gr.Number(label="Context Window", value=1, precision=0, interactive=True)

                instrument_type = gr.Radio(
                    choices=["piano", "drums"],
                    label="Preview Sound",
                    value="piano"
                )
        
        with gr.Column(scale=2):
            generate_btn = gr.Button("✨ Imagine the Tune!", variant="primary")
            with gr.Row():
                output_midi = gr.File(label="Download MIDI", visible=False)
                output_txt = gr.File(label="Download Text", visible=False)
            
            # Audio preview
            audio_preview = gr.Audio(label="Preview", visible=False)
            
            error_box = gr.Textbox(visible=False)


    def on_generate_click(*args):
        try:
            midi_path, txt_path, audio_path = generate_midi(*args)
            return [
                gr.File(value=midi_path, visible=True),
                gr.File(value=txt_path, visible=True),
                gr.Audio(value=audio_path, visible=True),
                gr.Textbox(visible=False)
            ]
        except Exception as e:
            return [
                gr.File(visible=False),
                gr.File(visible=False),
                gr.Audio(visible=False),
                gr.Textbox(value=str(e), visible=True)
            ]
        
    generate_btn.click(
        fn=on_generate_click,
        inputs=[
            api_key,
            loop_type,
            output_type,
            instrument,
            per_file_length,
            tempo,
            time_signature_num,
            time_signature_den,
            key,
            genre,
            description,
            n_chunks,
            k_context,
            instrument_type
        ],
        outputs=[
            output_midi,
            output_txt,
            audio_preview,
            error_box
        ]
    )


    
    # Load defaults when loop type changes
    def update_defaults(loop_type):
        defaults = load_loop_defaults(loop_type)
        return (
        defaults["output_type"],
        defaults["instrument"],
        defaults["per_file_length"],
        defaults["tempo"],
        defaults["time_signature_num"],
        defaults["time_signature_den"],
        defaults["key"],
        defaults["genre"],
        defaults["description"],
        defaults["n_chunks"],
        defaults["k_context"]
        )
    
    loop_type.change(
        fn=update_defaults,
        inputs=loop_type,
        outputs=[
            output_type,
            instrument,
            per_file_length,
            tempo,
            time_signature_num,
            time_signature_den,
            key,
            genre,
            description,
            n_chunks,
            k_context
        ]
    )
    
    def on_generate_click(*args):
        try:
            return generate_midi(*args), gr.File(visible=True), gr.Textbox(visible=False)
        except Exception as e:
            return None, gr.File(visible=False), gr.Textbox(value=str(e), visible=True)
    
    generate_btn.click(
        fn=on_generate_click,
        inputs=[
            api_key,
            loop_type,
            output_type,
            instrument,
            per_file_length,
            tempo,
            time_signature_num,
            time_signature_den,
            key,
            genre,
            description,
            n_chunks,
            k_context
        ],
        outputs=[
            output_midi,
            output_midi,
            error_box
        ]
    )

if __name__ == "__main__":
    demo.launch(debug=True)