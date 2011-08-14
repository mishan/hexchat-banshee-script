# shamelessly stolen from dom96's Exaile script

import xchat, dbus, os
__module_name__ = "Banshee"
__module_version__ = "1.0"
__module_description__ = "Banshee now playing script with some other cool features"

bus = dbus.SessionBus()

def getSongInfo():
  try:
    banshee = bus.get_object("org.bansheeproject.Banshee", "/org/bansheeproject/Banshee/PlayerEngine")

    if banshee.GetCurrentState() == "playing":
      npDict = banshee.GetCurrentTrack()
      title = str(npDict['name'])
      album = str(npDict['album'])
      artist = str(npDict['artist'])
      secs = int(banshee.GetPosition() / 1000)
      if secs > 0:
        pos = '%d:%02d' % (float(secs) / 60, float(secs) % 60)
      else:
        pos = "0:00"

      length = int(npDict['length'])
      if length > 0:
        length = '%d:%02d' % (float(length) / 60, float(length) % 60)
      else:
        length = "0:00"

      return (artist, title, album, pos, length)
    else:
      return 0
  except dbus.exceptions.DBusException:
    return 1


def printSong(word, word_eol, userdata):
  songInfo = getSongInfo()
  if songInfo == 0:
    xchat.prnt("Banshee is not playing")
  elif songInfo == 1:
    xchat.prnt("Banshee is not running")
  else:
    if not userdata:
      xchat.command("me is listening to %s - %s [%s] (%s/%s)" % songInfo)
    else:
      xchat.command("me is listening to \x0303%s\x03 - \x0303%s\x03 [\x0303%s\x03] (\x0305%s\x03/\x0305%s\x03)" % songInfo)

  return xchat.EAT_ALL


def chooseSong(word, word_eol, next):
  if next:
    if os.system("banshee-1 --next") == 0:
      xchat.prnt("Song changed")
    else:
      xchat.prnt("Song changing failed")
  else:
    if os.system("banshee-1 --prev") == 0:
      xchat.prnt("Song changed")
    else:
      xchat.prnt("Song changing failed")

def playPause(word, word_eol, ud):
  try:
    b = bus.get_object("org.bansheeproject.Banshee", "/org/bansheeproject/Banshee/PlayerEngine")
    b.TogglePlaying()

    xchat.prnt("Pause/play")

  except dbus.exceptions.DBusException:
    xchat.prnt("Pause/play failed")

xchat.prnt("Banshee script initialized")
xchat.prnt("Use /np to announce the currently played song")
xchat.hook_command("np", printSong, False)
xchat.hook_command("npc", printSong, True)
xchat.hook_command("bnext", chooseSong, True)
xchat.hook_command("bprev", chooseSong, False)
xchat.hook_command("pause", playPause)
