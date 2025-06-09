def map_params(normalized_params, param_bounds):
    """Convert normalized [0,1] to actual values based on bounds with automatic type handling."""
    mapped_params = {}
    for param, value in normalized_params.items():
        min_val, max_val = param_bounds[param][:2]
        raw_value = min_val + value * (max_val - min_val)
        mapped_params[param] = int(round(raw_value)) if isinstance(min_val, int) else round(raw_value, 6)
    return mapped_params