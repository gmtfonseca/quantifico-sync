from pathlib import Path
import wx

ICONS_PATH = Path(__file__).parent / 'images' / 'icons'


class ClienteConfigDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(ClienteConfigDialog, self).__init__(*args, **kw)
        self._initLayout()
        self.Centre()

    def _initLayout(self):
        self.panel = wx.Panel(self)

        sizer = wx.GridBagSizer(4, 4)

        lblDirNfs = wx.StaticText(self.panel, label='Diretório NFs')
        font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        lblDirNfs.SetFont(font)
        sizer.Add(lblDirNfs, pos=(0, 0), flag=wx.ALL, border=10)

        self.txtDirNfs = wx.TextCtrl(self.panel, size=(250, 35))
        # iconSelecionar = wx.Bitmap(iconPath, wx.BITMAP_TYPE_ANY)
        btnSelecionar = wx.Button(self.panel, size=(50, 35))
        # btnSelecionar = wx.BitmapButton(self.panel, bitmap=iconSelecionar, size=(50, 35))
        sizer.Add(self.txtDirNfs, pos=(1, 0), span=(1, 4), flag=wx.LEFT | wx.EXPAND, border=10)
        sizer.Add(btnSelecionar, pos=(1, 4))

        btnCancelar = wx.Button(self.panel, wx.ID_CANCEL, label='Cancelar', size=(90, 30))
        btnOk = wx.Button(self.panel, wx.ID_OK, label='Ok', size=(90, 30))
        sizer.Add(btnCancelar, pos=(3, 3))
        sizer.Add(btnOk, pos=(3, 4), flag=wx.RIGHT | wx.BOTTOM, border=10)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)

        self.panel.SetSizer(sizer)
        sizer.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.onSelecionar, btnSelecionar)
        self.Show()

    def onSelecionar(self, evt):
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           # | wx.DD_DIR_MUST_EXIST
                           # | wx.DD_CHANGE_DIR
                           )

        if dlg.ShowModal() == wx.ID_OK:
            self.txtDirNfs.SetValue(dlg.GetPath())

        dlg.Destroy()
