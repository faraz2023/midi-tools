# midi-tools
Personal library for generative midi generation 

## Local Installation

To install dependencies locally:

```bash
pip install midi2audio

# On macOS
brew install fluid-synth

# On Ubuntu/Debian
sudo apt-get install fluidsynth
```

## Git LFS Setup

This repository uses Git Large File Storage (LFS) for managing soundfont files. To work with the repository:

1. Install Git LFS:
   ```bash
   # On macOS
   brew install git-lfs

   # On Ubuntu/Debian
   sudo apt-get install git-lfs
   ```

2. Enable Git LFS in your repository:
   ```bash
   git lfs install
   ```

3. When cloning the repository, the soundfonts will be automatically downloaded:
   ```bash
   git clone https://your-repository-url.git
   ```

## Docker Installation

The application can be run using Docker, which handles all dependencies automatically:

1. Make sure you have Docker and Docker Compose installed
3. Build and run the container:
   ```bash
   docker-compose up --build
   ```
4. Access the application at http://localhost:7860

The MIDI files will be saved in the `gradio_output_midi` directory, which is mounted as a volume.