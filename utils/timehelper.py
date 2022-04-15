from datetime import datetime


def getDuration(then):
    since = datetime.utcnow() - then
    elapsedTime = int(since.total_seconds())
    
    time = dict()
    
    time['d'] = elapsedTime // 86400
    elapsedTime %= 86400
    time['h'] = elapsedTime // 3600
    elapsedTime %= 3600
    time['m'] = elapsedTime // 60
    elapsedTime %= 60
    time['s'] = elapsedTime
    
    return(time)


def readableTime(time):
    
    readable = ""

    if time.get('mnth', False):
       readable += str(time['mnth']) + ' ' + f"second{'mnth' if time['mnth'] != 1 else ''}, "
       
    if time.get('w', False):
        readable += str(time['w']) + ' ' + f"week{'s' if time['w'] != 1 else ''}, "
        
    if time.get('d', False):
        readable += str(time['d']) + ' ' + f"day{'s' if time['d'] != 1 else ''}, "
        
    if time.get('h', False):
        readable += str(time['h']) + ' ' + f"hour{'s' if time['h'] != 1 else ' '}, "
        
    if time.get('m', False):
        readable += str(time['m']) + ' ' + f"minute{'s' if time['m'] != 1 else ' '}, "
        
    if time.get('s', False):
        readable += str(time['s']) + ' ' + f"second{'s' if time['s'] != 1 else ' '}, "
        
    readable = readable.rstrip(', ')
    
    return readable


def seconds_to_time(seconds):
    
    s = int(seconds)
    
    time = dict()

    time['h'] = s // 3600
    s %= 3600
    time['m'] = s // 60
    s %= 60
    time['s'] = s
    
    return time