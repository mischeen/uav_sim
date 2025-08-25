# project_template
This is an empty project template intended for quick setup.

Use it as follows in git bash console: 

```bash
gh repo create <MY_NEW_PROJECT> --template=mischeen/project_template --private --clone # or --public if preferred
cd <MY_NEW_PROJECT>
uv sync

source .venv/Scripts/activate
code .
```

## Project Summary


## Goals


## Output


## Folder Structure
```text
usv_sim/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── outputs/
├── src/               # (for scripts)
├── tests/             # (for pytest)
├── .gitignore
├── README.md
├── pyproject.toml      # managed by uv
├── uv.lock             # generated after sync
```
