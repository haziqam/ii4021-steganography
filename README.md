# II4021-Steganography

## Setting up
1. Make sure Python 3.12 or later is installed
2. [Optional] create Python virtual environment (venv)
3. Install the dependencies at [requirements.txt](./requirements.txt)

## Usage
1. Run `python3 main.py [-h] [--seed [SEED]] [--out OUT] file {embed,extract} {image,audio,video} {lsb,bpcs}`
2. Input the message in the CLI, or you can pipe the message from another source (e.g. text file) into the program (see redirect or pipe)
