import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

# -------------------------------------------------------------
# 1. Map Child Settings (Question options, choices, metadata)
# -------------------------------------------------------------
class CopierQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid") # Block completely malformed question sub-keys
    
    type: Optional[str] = None
    help: Optional[str] = None
    default: Optional[Any] = None
    choices: Optional[Union[List[Any], Dict[str, Any]]] = None
    secret: Optional[bool] = None
    multiselect: Optional[bool] = None
    min: Optional[Union[int, float]] = None
    max: Optional[Union[int, float]] = None
    validator: Optional[str] = None
    when: Optional[Union[bool, str]] = None

# -------------------------------------------------------------
# 2. Map Main Schema (Copier Internal Configurations)
# -------------------------------------------------------------
class CopierConfig(BaseModel):
    # Forbid unknown internal keys, but allow custom user fields via pattern or post-parse
    model_config = ConfigDict(extra="allow") 

    # Common Copier Internal Variables
    min_copier_version: Optional[str] = Field(None, alias="_min_copier_version")
    answers_file: Optional[str] = Field(None, alias="_answers_file")
    subdirectory: Optional[str] = Field(None, alias="_subdirectory")
    exclude: Optional[List[str]] = Field(None, alias="_exclude")
    skip_if_exists: Optional[List[str]] = Field(None, alias="_skip_if_exists")
    tasks: Optional[List[str]] = Field(None, alias="_tasks")
    migrations: Optional[List[Dict[str, str]]] = Field(None, alias="_migrations")
    jinja_extensions: Optional[List[str]] = Field(None, alias="_jinja_extensions")
    secret_questions: Optional[List[str]] = Field(None, alias="_secret_questions")
    templates_suffix: Optional[str] = Field(None, alias="_templates_suffix")
    lifecycle_hooks: Optional[Dict[str, Any]] = Field(None, alias="_lifecycle_hooks")

    def validate_custom_questions(self):
        """Validates that user questions are properly structured."""
        for key, value in self.model_extra.items(): # Process fields matched via 'extra="allow"'
            # Internal keys start with underscore; skip them if unmapped
            if key.startswith("_"):
                continue
            
            # Simple shorthand questions like: my_var: "default_value"
            if isinstance(value, (str, int, float, bool, list)):
                continue
                
            # Deeply nested question maps like: my_var: { type: "str", help: "..." }
            if isinstance(value, dict):
                try:
                    CopierQuestion(**value)
                except ValidationError as e:
                    raise ValidationError.from_exception_data(
                        title=self.__class__.__name__,
                        line_errors=[
                            {
                                "loc": (key, *err["loc"]),
                                "input": err["input"],
                                "type": err["type"],
                                "msg": err["msg"],
                            }
                            for err in e.errors()
                        ]
                    )
            else:
                raise TypeError(f"Invalid type for question '{key}': {type(value).__name__}")

# -------------------------------------------------------------
# 3. Execution & Parsing Engine
# -------------------------------------------------------------
def run_validation():
    yaml_path = Path("copier.yml")
    if not yaml_path.exists():
        yaml_path = Path("copier.yaml")
        
    if not yaml_path.exists():
        print("Error: 'copier.yml' or 'copier.yaml' not found in the root directory.")
        sys.exit(1)

    try:
        # Load Raw YAML data
        with open(yaml_path, "r", encoding="utf-8") as f:
            raw_data = yaml.safe_load(f)
            
        if not isinstance(raw_data, dict):
            print("Error: copier.yml root must be a valid dictionary structure.")
            sys.exit(1)

        # Feed to Pydantic Model parsing layer
        config = CopierConfig.model_validate(raw_data)
        
        # Manually invoke contextual question maps validation
        config.validate_custom_questions()
        
        print("Success: copier.yml matches the Pydantic schema structure perfectly.")
        # sys.exit(0)

    except yaml.YAMLError as yaml_err:
        print(f"Syntax Error: Failed parsing structural YAML syntax: {yaml_err}")
        sys.exit(1)
    except ValidationError as pydantic_err:
        print(f"Validation Error: copier.yml configurations violated the schema:\n")
        print(pydantic_err)
        sys.exit(1)

