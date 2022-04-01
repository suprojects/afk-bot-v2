from datetime import datetime

def getDuration(then):
    since = datetime.utcnow() - then
    elapsedTime = int(since.total_seconds())
    
    time = dict()
    
    time['h'] = elapsedTime // 3600
    elapsedTime %= 3600
    time['m'] = elapsedTime // 60
    elapsedTime %= 60
    time['s'] = elapsedTime
    
    return(time)

def readableTime(time):
    readable = ""

    if time.get('mnth', None):
       readable = str(time['mnth'] + f"second{'mnth' if time['mnth'] != 1 else ''}")
       
    if time.get('w', None):
        readable = str(time['w'] + f"week{'s' if time['w'] != 1 else ''}")
        
    if time.get('d', None):
        readable = str(time['d'] + f"day{'s' if time['d'] != 1 else ''}")
        
    if time.get('h', None):
        readable = str(time['h']) +' ' + f"hour{'s' if time['h'] != 1 else ' '}"
        
    if time.get('m', None):
        readable = str(time['m']) + ' ' + f"minute{'s' if time['m'] != 1 else ' '}"
        
    if time.get('s', None):
        readable = str(time['s']) + ' ' + f"second{'s' if time['s'] != 1 else ' '}"
    
    return readable