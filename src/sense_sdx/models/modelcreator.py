from pathlib import Path
from pydantic import BaseModel, create_model
import json
import jsonschema
from typing import Any, Dict


class ModelCreator:
    def __init__(self, schema_dir: str, output_dir: str):
        self.schema_dir = Path(schema_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_schema(self, file_path: Path) -> dict:
        if file_path.suffix == ".json":
            with open(file_path, "r") as f:
                schema = json.load(f)
                self.validate_schema(schema)
                return schema
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

    def validate_schema(self, schema: dict):
        try:
            jsonschema.Draft7Validator.check_schema(schema)
        except jsonschema.exceptions.SchemaError as e:
            raise ValueError(f"Invalid JSON schema: {e.message}")

    def create_models(self) -> Dict[str, type]:
        models = {}
        for schema_file in self.schema_dir.glob("*.json"):
            schema_data = self.load_schema(schema_file)
            model_name = schema_file.stem.capitalize()
            model = self.create_model(model_name, schema_data)
            models[model_name] = model
            self.save_model_to_file(model_name, model)
        return models

    def create_model(self, name: str, schema_data: dict) -> type:
        properties = schema_data.get("properties", {})
        required_fields = schema_data.get("required", [])
        annotations = {}
        defaults = {}

        for field_name, field_info in properties.items():
            field_type = self.map_json_type_to_python(field_info)
            annotations[field_name] = field_type
            if field_name not in required_fields:
                defaults[field_name] = None

        return create_model(name, **{**annotations, **defaults})

    def map_json_type_to_python(self, field_info: dict) -> Any:
        json_type = field_info.get("type", "string")
        type_mapping = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict,
        }
        return type_mapping.get(json_type, Any)

    def save_model_to_file(self, model_name: str, model: type):
        file_path = self.output_dir / f"{model_name.lower()}.py"
        with open(file_path, "w") as f:
            f.write(f"from pydantic import BaseModel\n\n\n")
            f.write(f"class {model_name}(BaseModel):\n")
            for field, field_type in model.__annotations__.items():
                f.write(f"    {field}: {field_type.__name__}\n")


# Example usage
if __name__ == "__main__":
    schema_dir = "../../../schemas"
    output_dir = "./"
    creator = ModelCreator(schema_dir, output_dir)
    models = creator.create_models()

    # Example: Accessing a generated model
    for model_name, model in models.items():
        print(f"Generated model: {model_name}")
