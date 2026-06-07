# fastapi-project-skeleton
template for fastapi project onborading

##project setup
# Create the Virtual Environment
> uv venv

# To actiate virtual env - cmd
> .venv\Scripts\activate.bat

# To actiate virtual env - bash
> source .venv/bin/activate

# To deactiate virtual env
> deactivate

# If you have cloned a repository or have an existing pyproject.toml, use the below command to install the required packages into your local environment
> uv sync

# If your project manages dependencies via a traditional requirements.txt file instead of a pyproject.toml configuration, use the low-level pip compatibility interfac

> uv pip install -r requirements.txt

# run the project to generate scaffolder
> uv run main.py
