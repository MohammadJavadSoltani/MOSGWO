def mirror_boundary(value, min_val, max_val):
    """Reflects values that exceed boundaries back inside with proportional scaling."""
    range_val = max_val - min_val  

    # Check and reflect values exceeding the max boundary
    if value > max_val:
        excess = value - max_val
        value = max_val - (excess % range_val) 
    # Check and reflect values below the min boundary
    elif value < min_val:
        deficit = min_val - value
        value = min_val + (deficit % range_val)  

    return value
