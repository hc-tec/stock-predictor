

def md5(user):
    import hashlib
    salt = '1'
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(salt, encoding='utf-8'))
    return m.hexdigest()

def deepcopy(instance):
    import copy
    return copy.deepcopy(instance)













