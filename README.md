# NotKevin

This is my attempt at combing storage with a gpt.
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
pip install notkevin-0.0.0-py3-none-any.whl
```

### Access
```base
conda activate notkevin
NK
```

### API KEY
The use of this requires an API KEY. This needs to be stored in the environment variable `OPENAI_API_KEY`.

### Flags
There are a few flags that can be provided to the program.
The standard `NK -h` will show the help menu.

`-c` or `--clear`  
Clears  the memory

`-n` or `--nosave`  
Does not save the memory to the file

