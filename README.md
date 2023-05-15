# NotKevin

This is my attempt at creating some fun interactive chatbots with memory based on gpt.
The assistant is meant to be a personal assistant that can be used to store information and retrieve it later.
Its a toy example.


### Build
```bash
pip install build
python -m build
```

### install
```bash
cd dist
conda create -n notkevin python=3.11
pip install notkevin-0.0.4-py3-none-any.whl
```

### Access
```base
conda activate notkevin
NK -n <name> 
```

### API KEY
The use of this requires an API KEY. This needs to be stored in the environment variable `OPENAI_API_KEY`.

### Flags
There are a few flags that can be provided to the program.
The standard `NK -h` will show the help menu.

`-c` or `--clear`  
Clears  the memory

`-n` or `--name`  
Name of the Agent. Defaults to `NotKevin`

`-r` or `--rubberduck` 
This is the no save option. The agent is fed your conversation history and contest from past conversations but does not save new content.

`--gpt4` 
This causes the model to use GPT-4 backend instead of GPT-3. Embeddings are still GPT-3.
