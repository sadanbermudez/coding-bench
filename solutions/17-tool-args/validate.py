TYPES = {
    "object": lambda v: isinstance(v, dict), "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str), "boolean": lambda v: isinstance(v, bool), "null": lambda v: v is None,
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
}


def validate(v, s, path="$"):
    if "type" in s and not TYPES[s["type"]](v):
        return [f"{path}: expected {s['type']}"]
    e = []
    if "enum" in s and v not in s["enum"]:
        e.append(f"{path}: not one of {s['enum']}")
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if "minimum" in s and v < s["minimum"]: e.append(f"{path}: below minimum")
        if "maximum" in s and v > s["maximum"]: e.append(f"{path}: above maximum")
    if isinstance(v, str):
        if "minLength" in s and len(v) < s["minLength"]: e.append(f"{path}: too short")
        if "maxLength" in s and len(v) > s["maxLength"]: e.append(f"{path}: too long")
    if isinstance(v, dict):
        props = s.get("properties", {})
        for r in s.get("required", []):
            if r not in v: e.append(f"{path}: missing {r}")
        for k, x in v.items():
            if k in props: e += validate(x, props[k], f"{path}.{k}")
            elif s.get("additionalProperties") is False: e.append(f"{path}.{k}: not allowed")
    if isinstance(v, list) and "items" in s:
        for i, x in enumerate(v):
            e += validate(x, s["items"], f"{path}[{i}]")
    return e
