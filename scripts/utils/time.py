def parse_gtfs_time(time_str):
    """
    Convert GTFS time string to seconds since midnight
    Handles times > 24:00:00 (e.g., 25:30:00 = 1:30 AM next day)
    """
    try:
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    except:
        return 0

def time_diff(time1_str, time2_str):
    """Calculate difference in seconds between two GTFS times"""
    t1 = parse_gtfs_time(time1_str)
    t2 = parse_gtfs_time(time2_str)
    diff = t2 - t1
    
    # Handle negative times (overnight)
    if diff < 0:
        diff += 24 * 3600
    
    # If time is 0, estimate based on typical speed (30 km/h)
    # This will be overridden by distance calculation anyway
    if diff == 0:
        return 30  # Assume minimum 30 seconds between stops
    
    # Cap at 2 hours (anything longer is overnight error)
    if diff > 7200:
        return 0  # Will be filtered out
    
    return diff