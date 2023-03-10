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

account_schema = {
    "type": "object",
    "properties": {
        "initial_balance": NUMBER,
        "balance_name": STRING,
        "balance_type": STRING,
        "currency": STRING,
        "description": STRING,
    },
    "required": ["initial_balance", "balance_name", "balance_type", "currency"],
    "additionalProperties": False
}

account_update_schema = {
    "type": "object",
    "properties": {
        "initial_balance": NUMBER,
        "balance_name": STRING,
        "balance_type": STRING,
        "currency": STRING,
        "description": STRING,
    },
    "required": [],
    "additionalProperties": False
}

transaction_schema = {
    "type": "object",
    "properties": {
        "type": STRING,
        "amount": NUMBER,
        "category": STRING,
        "description": STRING
    },
    "required": ["type", "amount", "category", "description"],
    "additionalProperties": False
}

transaction_update_schema = {
    "type": "object",
    "properties": {
        "type": STRING,
        "amount": NUMBER,
        "category": STRING,
        "description": STRING
    },
    "required": [],
    "additionalProperties": False
}