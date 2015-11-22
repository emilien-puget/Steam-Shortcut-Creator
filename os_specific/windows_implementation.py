import os
import urllib.request
import zipfile
from . import os_specific_interface
import subprocess


class WindowsImplementation(os_specific_interface.OsSpecific):
    shortcut_folder = False

    def __init__(self):
        print('starting windows process')
        self.shortcut_folder = os.getenv('APPDATA') + '\Microsoft\Windows\Start Menu\Programs\steamlnk_shortcuts'
        if not os.path.isdir(self.shortcut_folder):
            os.mkdir(self.shortcut_folder)

    def download_steamcmd(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        steamcmd = 'D:\Jeux\Steam\steamcmd.exe'
        if os.path.isfile(steamcmd):
            return steamcmd

        print('Steamcmd is not found, downloading ...')
        archive = path + '/steamcmd.archive'
        try:
            urllib.request.urlretrieve('https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip',
                                       archive)
        except Exception as error:
            print('steamcmd can\'t be downloaded : ' + error.__str__())
            exit()

        zipfile.ZipFile(archive).extractall(path)

        os.remove(archive)
        if os.path.isfile(steamcmd):
            return steamcmd
        else:
            return False

    def create_shortcut(self, game):
        shortcut_file = self.shortcut_folder + "\\" + game['name'].replace(':', '') + '.lnk'
        clienticon = ''
        if game['clienticon'] and os.path.isfile('D:\Jeux\Steam\steam\games\\' + game['clienticon'] + '.ico'):
            clienticon = 'D:\Jeux\Steam\steam\games\\' + game['clienticon'] + '.ico'
        else:
            clienticon = 'D:\Jeux\Steam\Steam.exe'

        command = r'$shell = New-Object -comObject WScript.Shell ; ' \
                  r'$lnk = $shell.CreateShortcut("' + shortcut_file + '") ; ' \
                                                                      '$lnk.TargetPath = "D:\Jeux\Steam\steam.exe" ; $lnk.Arguments = "-applaunch ' + \
                  game['id'] + '" ; ' \
                               '$lnk.IconLocation="' + clienticon + '" ; $lnk.Save()'
        print('Creating shortcut for: ' + game['name'] + ' with icon: '+clienticon)
        subprocess.Popen(['powershell.exe', command])

    @staticmethod
    def get_os_name():
        return 'windows'
