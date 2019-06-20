# -*- coding: utf-8 -*-
import os
import keyword
import wx, wx.aui
import wx.stc as stc
from toolkit.encodings.DIPA import DIPA

class SplSplitter(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, -1, style = wx.SP_LIVE_UPDATE)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.on_sash_changed)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.on_sash_changing)
        
    def on_sash_changed(self, evt): pass
    def on_sash_changing(self, evt): pass

class FrmMain(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, size=(1152, 864), title="Transliteration Editor")
        self.SetIcon(wx.Icon('../flazzle.ico', wx.BITMAP_TYPE_ICO))
        
        # Create the top-level sizer and splitter
        Szr = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(Szr)
        self.SplSplitter = SplSplitter(self)
        Szr.Add(self.SplSplitter, 1, wx.EXPAND)
        
        # Add the tree/notebook
        self.Tree = TreTree(self.SplSplitter, -1, style=wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        self.Tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_activate)
        self.Panel = wx.Panel(self.SplSplitter, -1)
        self.Panel.parent = self
        self.PanelSzr = wx.BoxSizer(wx.VERTICAL)
        self.Panel.SetSizer(self.PanelSzr)
        self.SplSplitter.SetMinimumPaneSize(20)
        self.SplSplitter.SplitVertically(self.Tree, self.Panel, 250)
        
        # Create the toolbar
        self._CreateToolbar()
        self.CenterOnScreen()
        
        # A dict from Path -> panel
        self.DFileSTC = {}
        
    def on_tree_activate(self, evt):
        Item = evt.GetItem()
        Data = self.Tree.GetPyData(Item)
        if not Data: 
            evt.Skip()
            return
        else:
            self.SelItem = Item
            self.Tree.SetItemBold(Item)
            
            self.Panel.Freeze()
            try:
                for k in self.DFileSTC:
                    self.DFileSTC[k].Hide()
                
                if Data in self.DFileSTC:
                    self.DFileSTC[Data].Show()
                    wx.CallAfter(self.Layout)
                else:
                    STC = PythonSTC(self.Panel, Data)
                    self.DFileSTC[Data] = STC
                    self.PanelSzr.Add(STC, 1, wx.EXPAND)
                self.DFileSTC[Data].SetSize(self.Panel.GetSize())
            except Exception as exc:
                try: self.DFileSTC[Data].Destroy()
                except: pass
                raise exc
            self.Panel.Thaw()
            evt.Skip()
        
    def _CreateToolbar(self):
        TBFLAGS = wx.TB_HORIZONTAL|wx.NO_BORDER|wx.TB_FLAT
        self.TbToolBar = self.CreateToolBar(TBFLAGS)
        
        LBmp = []; Sz = (16,16)
        LBmp.append(['new',  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, Sz)])
        LBmp.append(['save', wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, Sz)])
        LBmp.append([None, None])
        LBmp.append(['copy', wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, Sz)])
        LBmp.append(['paste', wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, Sz)])
        LBmp.append([None, None])
        LBmp.append(['undo', wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, Sz)])
        LBmp.append(['redo', wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, Sz)])
        LBmp.append([None, None])
        LBmp.append(['find', wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_TOOLBAR, Sz)])
        LBmp.append(['replace', wx.ArtProvider.GetBitmap(wx.ART_FIND_AND_REPLACE, wx.ART_TOOLBAR, Sz)])
        LBmp.append([None, None])
        self.TbToolBar.SetToolBitmapSize(Sz)
        
        for k, Bmp in LBmp:
            if Bmp:
                # TODO: Bind on events!
                Id = wx.NewId()
                Tool = self.TbToolBar.AddSimpleTool(Id, Bmp, k, k)
            else:
                # Add a separator
                self.TbToolBar.AddSeparator()
        
        e = wx.FontEnumerator()
        e.EnumerateFacenames()
        LFaceNames = e.GetFacenames()
        LFaceNames = [(i.lower(), i) for i in LFaceNames]
        LFaceNames.sort()
        LFaceNames = [i[1] for i in LFaceNames]
        self.CmbFonts = wx.Choice(self.TbToolBar, -1, choices=LFaceNames, size=(200,-1))
        self.TbToolBar.AddControl(self.CmbFonts)
        self.TbToolBar.Realize()
        
    def on_new(self, evt): pass
    def on_save(self, evt): pass
    def on_copy(self, evt): pass
    def on_paste(self, evt): pass
    def on_undo(self, evt): pass
    def on_replace(self, evt): pass
        
    def on_find(self, event):
        editor = self.codePage.editor
        self.nb.SetSelection(1)
        end = editor.GetLastPosition()
        textstring = editor.GetRange(0, end).lower()
        findstring = self.finddata.GetFindString().lower()
        backward = not (self.finddata.GetFlags() & wx.FR_DOWN)
        if backward:
            start = editor.GetSelection()[0]
            loc = textstring.rfind(findstring, 0, start)
        else:
            start = editor.GetSelection()[1]
            loc = textstring.find(findstring, start)
        if loc == -1 and start != 0:
            # string not found, start at beginning
            if backward:
                start = end
                loc = textstring.rfind(findstring, 0, start)
            else:
                start = 0
                loc = textstring.find(findstring, start)
        if loc == -1:
            dlg = wx.MessageDialog(self, 'Find String Not Found',
                          'Find String Not Found in Demo File',
                          wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        if self.finddlg:
            if loc == -1:
                self.finddlg.SetFocus()
                return
            else:
                self.finddlg.Destroy()
                self.finddlg = None
        editor.ShowPosition(loc)
        editor.SetSelection(loc, loc + len(findstring))
        
    def on_find_next(self, event):
        if self.finddata.GetFindString():
            self.on_find(event)
        else:
            self.OnHelpFind(event)
        
    def on_find_close(self, event):
        event.GetDialog().Destroy()
        self.finddlg = None

class TreTree(wx.TreeCtrl):
    def __init__(self, *args, **kwargs):
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        self.Dir = os.getcwd()+'/BySound'
        self.Dir = self.Dir.replace('\\', '/')
        Sz = 16, 16
        self.il = wx.ImageList(*Sz)
        self.fldridx = self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, Sz))
        self.fldropenidx = self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, Sz))
        self.fileidx = self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, Sz))
        self.SetImageList(self.il)
        self.populate()
        
    def populate(self):
        # Clear items and recreate the root
        self.DeleteAllItems()
        self.Root = self.AddRoot("The Root Item")
        self.SetItemImage(self.Root, self.fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.Root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        # Get all files/dirs and sort them
        LDirs = []
        DUniqueDirs = {}
        LFiles = []
        for Root, tLDirs, tLFiles in os.walk(self.Dir):
            if '.svn' in Root: continue
            elif Root in DUniqueDirs: continue 
            DUniqueDirs[Root] = None
            LDirs.append(Root)
            LFiles.extend([(Root, i) for i in tLFiles])
        LDirs.sort()
        LFiles.sort()
        
        # Create the directory objects
        DDirs = {}
        for Dir in LDirs:
            Dir = Dir.replace('\\', '/')
            DispDir = Dir.replace(self.Dir, '').lstrip('/')
            if not Dir.strip(): continue
            
            if '/' in DispDir:
                # Create an item using the next up directory
                Parent = DDirs['/'.join(Dir.split('/')[:-1])]
                DDirs[Dir] = self.AppendItem(Parent, DispDir.split('/')[-1])
                self.SetPyData(DDirs[Dir], None)
            else: 
                # Create an item directly off the root
                DDirs[Dir] = self.AppendItem(self.Root, DispDir)
                self.SetPyData(DDirs[Dir], None)
            
            # And set the icons
            self.SetItemImage(DDirs[Dir], self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(DDirs[Dir], self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        # Create the file objects
        for Dir, File in LFiles:
            Parent = DDirs[Dir.replace('\\', '/')]
            FileName = os.path.split(File)[-1]
            Item = self.AppendItem(Parent, FileName)
            self.SetPyData(Item, '%s/%s' % (Dir, FileName))
            
            # And set the icons
            self.SetItemImage(Item, self.fileidx, wx.TreeItemIcon_Normal)
            self.SetItemImage(Item, self.fileidx, wx.TreeItemIcon_Expanded)
        #self.expand(self.Root)

faces = {'times': 'Arial Unicode MS',
         'mono' : 'Arial Unicode MS',
         'helv' : 'Arial Unicode MS',
         'other': 'Arial Unicode MS',
         'size' : 11,
         'size2': 11}

class PythonSTC(stc.StyledTextCtrl):
    fold_symbols = 2
    def __init__(self, parent, Path):
        stc.StyledTextCtrl.__init__(self, parent, -1)
        self.parent = parent
        self.AbsParent = parent.parent.Tree
        
        # Open the existing file
        self.Path = Path
        self.File = open(Path, 'r', encoding='utf-8', errors='replace')
        Text = self.File.read()#.encode('utf-8')
        #Text += '\n' # HACK!
        self.SetText(Text)
        self.File.close()

        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(list(keyword.kwlist)+['None', 'True', 'False']))

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0,0)

        #self.SetViewWhiteSpace(True)
        #self.SetBufferedDraw(False)
        #self.SetViewEOL(True)
        self.SetWrapMode(True)
        self.SetEOLMode(stc.STC_EOL_CRLF)
        self.SetUseAntiAliasing(True)
        
        self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78)

        # Setup a margin to hold fold markers
        #self.SetFoldFlags(16)  ###  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        if self.fold_symbols == 0:
            # Arrow pointing right for contracted folders, arrow pointing down for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_ARROWDOWN, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_ARROW, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY,     "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY,     "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY,     "white", "black")
            
        elif self.fold_symbols == 1:
            # Plus for contracted folders, minus for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_MINUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_PLUS,  "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.fold_symbols == 2:
            # Like a flattened tree control using circular headers and curved joins
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040")

        elif self.fold_symbols == 3:
            # Like a flattened tree control using square headers
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS,          "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,             "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,           "white", "#808080")

        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

        # Python styles
        # Default 
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)
        self.SetCaretForeground("BLUE")

        # register some images for use in the AutoComplete box.
        #self.RegisterImage(1, images.getSmilesBitmap())
        self.RegisterImage(2, wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16,16)))
        self.RegisterImage(3, wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16,16)))
        
        # Bind on various events
        self.Changed = False
        self.Bind(stc.EVT_STC_CHARADDED, self.on_changed)
        #self.Bind(stc.EVT_STC_CHANGE, self.on_changed)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.on_margin_click)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)
        
    def on_changed(self, evt):
        # Add an asterisk to indicate the page is modified
        self.Changed = True
        self.AbsParent.SetItemText(self.parent.parent.SelItem, '%s *' % os.path.split(self.Path)[-1])
        evt.Skip()
        
    def save(self):
        # save the file and remove the asterisk if present
        Text = self.GetText()#.decode('utf-8', 'ignore')
        self.File = open(self.Path, 'w', encoding='utf-8', errors='replace')
        self.File.write(Text)
        self.File.close()
        self.AbsParent.SetItemText(self.parent.parent.SelItem, os.path.split(self.Path)[-1])
        
    def on_key_pressed(self, evt):
        if self.CallTipActive(): self.CallTipCancel()
        Ctrl = evt.ControlDown()
        Code = evt.GetKeyCode()
        
        if Ctrl and Code == 32:
            # Code completion
            self.AutoCompSetIgnoreCase(False)
            self.AutoCompShow(0, DIPA[self.LastKey])
        elif Ctrl and Code == 83:
            # save (Ctrl+S)
            self.save()
        else:
            if not evt.ControlDown():
                self.LastKey = chr(evt.GetRawKeyCode()).lower()
                #print 'LASTKEY:', self.LastKey.encode('utf-8')
            evt.Skip()

    def on_margin_click(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.fold_all()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def fold_all(self):
        lineCount = self.GetLineCount()
        expanding = True
        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break
        
        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:
                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)
                    if lastChild > lineNum: self.HideLines(lineNum+1, lastChild)
            lineNum = lineNum + 1

    def expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0: self.ShowLines(line, line)
                else: self.HideLines(line, line)
            elif doExpand: self.ShowLines(line, line)
            
            if level == -1: level = self.GetFoldLevel(line)
            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1: self.SetFoldExpanded(line, True)
                    else: self.SetFoldExpanded(line, False)
                    line = self.expand(line, doExpand, force, visLevels-1)
                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.expand(line, True, force, visLevels-1)
                    else: line = self.expand(line, False, force, visLevels-1)
            else: line = line + 1
        return line

App = wx.PySimpleApp()
Frame = FrmMain()
Frame.Show()
App.MainLoop()
