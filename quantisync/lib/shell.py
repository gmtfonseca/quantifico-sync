from win32com.shell import shell, shellcon


class ShellIcon:

    @staticmethod
    def updateDir(path):
        pidl, _ = shell.SHILCreateFromPath(path, 0)
        shell.SHChangeNotify(shellcon.SHCNE_UPDATEDIR,
                             shellcon.SHCNF_IDLIST | shellcon.SHCNF_FLUSH,
                             pidl,
                             None)
