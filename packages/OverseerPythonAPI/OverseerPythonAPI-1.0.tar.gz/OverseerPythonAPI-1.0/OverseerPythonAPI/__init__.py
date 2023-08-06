import requests as req

CurrentConnectedProjectName = ''
CurrentConnectedProjectPSK = ''

def ConnectProject (UserKey, ShortUserKey, ProjectSecurityKey, Debug):
    global CurrentConnectedProjectPSK
    response = req.get('https://kiber-camp.ru/overseer/api/ConnectProject.php/?userKey={0}&userShortKey={1}&projectKey={2}'.format(UserKey, ShortUserKey, ProjectSecurityKey))
    if (Debug): print (response.text)
    KeyStartPosition = 0
    res = response.text

    i = 0
    while (i < len(res)):
        if (res[i] == ']'):
            KeyStartPosition = i
        i += 1

    PSK = ''
    while (KeyStartPosition < len(response.text) - 1):
        KeyStartPosition += 1
        PSK += response.text[KeyStartPosition]

    CurrentConnectedProjectPSK = PSK
    if (Debug): print ("KEY: {0}".format(PSK))

def SetTrack (TrackName, Debug):
    global CurrentConnectedProjectPSK
    response = req.get('https://kiber-camp.ru/overseer/api/MakeATrack.php/?database={0}&track={1}'.format(CurrentConnectedProjectPSK, TrackName))
    if (Debug): print (response.text)
    if (Debug): print ("Sended data:", CurrentConnectedProjectPSK, " --- ", TrackName)