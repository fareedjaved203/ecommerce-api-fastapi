import uuid

def uuid_to_bin(uuid_val):
    return uuid_val.bytes if isinstance(uuid_val, uuid.UUID) else uuid.UUID(uuid_val).bytes

def bin_to_uuid(bin_val):
    return str(uuid.UUID(bytes=bin_val))
