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