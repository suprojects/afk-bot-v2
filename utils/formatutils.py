
truelist = [1, '1', 'yes', 'true', True]
falselist = [0, '0', 'false', 'no', False]

def autobool(param):
    
    param = str(param).lower()
    
    if param in truelist:
        return {'bool': True, 'int': 1, 'str': 'true'}
    
    else:
        return {'bool': False, 'int': 0, 'str': 'false'}