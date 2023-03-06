# Property types
STRING = {"type": "string"}
NUMBER = {"type": "number"}
BOOLEAN = {"type": "boolean"}
ARRAY = {"type": "array"}

# API Schema
user_update_schema = {
    "type": "object",
    "properties": {
        "phone_number": STRING,
        "date_of_birth": STRING,
        "gender": STRING,
        "address": STRING,
        "occupations": STRING,
    },
    "required": [],
    "additionalProperties": False
}
