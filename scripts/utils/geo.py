import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two points in meters
    """
    R = 6371000  # Earth radius in meters
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def is_in_melbourne(lat, lon):
    """Check if coordinates are in Melbourne region"""
    return (-38.5 <= lat <= -37.5) and (144.5 <= lon <= 145.5)