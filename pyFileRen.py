# coding: UTF-8

"""
fileRenamer
An open-source software written in Python for renaming a batch of files. 

This program was coded and tested in macOS 10.13.

Jinook Oh, Cognitive Biology department, University of Vienna
September 2019.

Dependency:
    wxPython (4.0)

------------------------------------------------------------------------
Copyright (C) 2019 Jinook Oh, W. Tecumseh Fitch 
- Contact: jinook.oh@univie.ac.at, tecumseh.fitch@univie.ac.at

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation, either version 3 of the License, or (at your 
option) any later version.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License along 
with this program.  If not, see <http://www.gnu.org/licenses/>.
------------------------------------------------------------------------
"""

import sys
from os import path, getcwd, mkdir, rename
from copy import copy
from glob import glob
from math import ceil
from datetime import datetime

import wx, wx.richtext
import wx.lib.scrolledpanel as SPanel 
import wx.lib.agw.multidirdialog as MDD

DEBUG = False 
CWD = getcwd()
__version__ = "0.2"
"""
Changelog

v.0.1: 
  - Initial development.
v.0.2: 2019.Sept.17
  - Converted to wxPython app.
"""

#-----------------------------------------------------------------------

def GNU_notice(idx=0):
    """ Function for printing GNU copyright statements

    Args:
        idx (int): Index to determine which statement to print out.

    Returns:
        None

    Examples:
        >>> GNU_notice(0)
        Copyright (c) ...
        ...
        run this program with option '-c' for details.
    """
    if DEBUG: print("GNU_notice()")

    if idx == 0:
        year = datetime.now().year
        msg = "Copyright (c) %i Jinook Oh, W. Tecumseh Fitch.\n"%(year)
        msg += "This program comes with ABSOLUTELY NO WARRANTY;"
        msg += " for details run this program with the option `-w'."
        msg += "This is free software, and you are welcome to redistribute"
        msg += " it under certain conditions;"
        msg += " run this program with the option `-c' for details."
    elif idx == 1:
        msg = "THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED"
        msg += " BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING"
        msg += " THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE"
        msg += " PROGRAM 'AS IS' WITHOUT WARRANTY OF ANY KIND, EITHER"
        msg += " EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE"
        msg += " IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A"
        msg += " PARTICULAR PURPOSE."
        msg += " THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE"
        msg += " PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU"
        msg += " ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR"
        msg += " CORRECTION."
    elif idx == 2:
        msg = "You can redistribute this program and/or modify it under" 
        msg += " the terms of the GNU General Public License as published"
        msg += " by the Free Software Foundation, either version 3 of the"
        msg += " License, or (at your option) any later version."
    print(msg)

#-----------------------------------------------------------------------

def writeFile(file_path, txt='', mode='a'):
    """ Function to write a text or numpy file.

    Args:
        file_path (str): File path for output file.
        txt (str): Text to print in the file.
        mode (str, optional): File opening mode.

    Returns:
        None

    Examples:
        >>> writeFile('logFile.txt', 'A log is written.', 'a')
    """
    if DEBUG: print("writeFile()")
    
    f = open(file_path, mode)
    f.write(txt)
    f.close()

#-----------------------------------------------------------------------

def get_time_stamp(flag_ms=False):
    """ Function to return string which contains timestamp.

    Args:
        flag_ms (bool, optional): Whether to return microsecond or not

    Returns:
        ts (str): Timestamp string

    Examples:
        >>> print(get_time_stamp())
        2019_09_10_16_21_56
    """
    if DEBUG: print("get_time_stamp()")
    
    ts = datetime.now()
    ts = ('%.4i_%.2i_%.2i_%.2i_%.2i_%.2i')%(ts.year, 
                                            ts.month, 
                                            ts.day, 
                                            ts.hour, 
                                            ts.minute, 
                                            ts.second)
    if flag_ms == True: ts += '_%.6i'%(ts.microsecond)
    return ts

#-----------------------------------------------------------------------

def getWXFonts(initFontSz=8, numFonts=5, fSzInc=2, fontFaceName=""):
    """ For setting up several fonts (wx.Font) with increasing size.

    Args:
        initFontSz (int): Initial (the smallest) font size.
        numFonts (int): Number of fonts to return.
        fSzInc (int): Increment of font size.
        fontFaceName (str, optional): Font face name.

    Returns:
        fonts (list): List of several fonts (wx.Font)

    Examples:
        >>> fonts = getWXFonts(8, 3, fSzInc=2)
    """
    if DEBUG: print("getWXFonts()")

    if fontFaceName == "":
        if 'darwin' in sys.platform: fontFaceName = "Monaco"
        else: fontFaceName = "Courier"
    fontSz = initFontSz 
    fonts = []  # larger fonts as index gets larger 
    for i in range(numFonts):
        fonts.append(
                        wx.Font(
                                fontSz, 
                                wx.FONTFAMILY_SWISS, 
                                wx.FONTSTYLE_NORMAL, 
                                wx.FONTWEIGHT_BOLD,
                                False, 
                                faceName=fontFaceName,
                               )
                    )
        fontSz += fSzInc 
    return fonts

#-----------------------------------------------------------------------

def setupStaticText(panel, label, name=None, size=None, 
                    wrapWidth=None, font=None, fgColor=None, bgColor=None):
    """ Initialize wx.StatcText widget with more options
    
    Args:
        panel (wx.Panel): Panel to display wx.StaticText.
        label (str): String to show in wx.StaticText.
        name (str, optional): Name of the widget.
        size (tuple, optional): Size of the widget.
        wrapWidth (int, optional): Width for text wrapping.
        font (wx.Font, optional): Font for wx.StaticText.
        fgColor (wx.Colour, optional): Foreground color 
        bgColor (wx.Colour, optional): Background color 

    Returns:
        wx.StaticText: Created wx.StaticText object.

    Examples:
        >>> self.sTxt1 = setupStaticText(self.panel, 'Test')
    """ 
    if DEBUG: print("setupStaticText()")

    sTxt = wx.StaticText(panel, -1, label)
    if name != None: sTxt.SetName(name)
    if size != None: sTxt.SetSize(size)
    if wrapWidth != None: sTxt.Wrap(wrapWidth)
    if font != None: sTxt.SetFont(font)
    if fgColor != None: sTxt.SetForegroundColour(fgColor) 
    if bgColor != None: sTxt.SetBackgroundColour(bgColor)
    return sTxt

#-----------------------------------------------------------------------

def updateFrameSize(wxFrame, w_sz):
    """ Set window size exactly to a user-defined window size (w_sz)
    , excluding counting menubar/border/etc.

    Args:
        wxFrame (wx.Frame): Frame to resize.
        w_sz (tuple): Client size. 

    Returns:
        None

    Examples:
        >>> updateFrameSize(self, (800,600))
    """
    if DEBUG: print("updateFrameSize()")

    ### set window size to w_sz, excluding counting menubar/border/etc.
    _diff = (wxFrame.GetSize()[0]-wxFrame.GetClientSize()[0], 
             wxFrame.GetSize()[1]-wxFrame.GetClientSize()[1])
    _sz = (w_sz[0]+_diff[0], w_sz[1]+_diff[1])
    wxFrame.SetSize(_sz) 
    wxFrame.Refresh()

#-----------------------------------------------------------------------

#=======================================================================

class FileRenamerFrame(wx.Frame):
    """ Frame for FileRenamer
    """

    def __init__(self):
        if DEBUG: print("FileRenamerFrame.__init__()")

        ### init frame
        w_pos = [0, 25]
        wg = wx.Display(0).GetGeometry()
        w_sz = (wg[2], int(wg[3]*0.9))
        wx.Frame.__init__(
              self, 
              None, 
              -1, 
              "File Renamer v.%s"%(__version__), 
              pos = tuple(w_pos), 
              size = tuple(w_sz),
              style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX),
                         ) 
        self.SetBackgroundColour('#333333')

        ##### beginning of setting up attributes ----- 
        self.w_pos = w_pos
        self.w_sz = w_sz
        self.fonts = getWXFonts(initFontSz=8, numFonts=3)
        pi = self.setPanelInfo()
        self.pi = pi # pnael information
        self.gbs = {} # for GridBagSizer
        self.panel = {} # panels
        self.timers = {} # timers
        self.selectedFolders = [] # list of selected folders
        self.folder2moveRenFile = "" # folder to move renamed files
        self.fileList = [] # file list to be renamed
        self.nFileList = [] # file list with new file names
        self.newFFO = [
                        'oFileN', 
                        'folderN', 
                        'incNum', 
                        'incNumInFolder', 
                        'ts',
                      ] # new file format options 
        self.newFFOD = dict(
                            oFileN = 'Original file-name',
                            folderN = 'Folder name', 
                            incNum = 'Increasing Number (overall)',
                            incNumInFolder = 'Increasing Number (in each folder)',
                            ts = 'Timestamp',
                            ) # new file format options - description
        self.logFile = "log_pyFileRen.txt"
        ##### end of setting up attributes -----  
        
        logHeader = "Timestamp, Origianl file, Renamed file\n"
        logHeader += "----------------------------------------\n"
        if not path.isfile(self.logFile): # log file doesn't exist
            writeFile(self.logFile, logHeader) # write header

        ### create panels
        for pk in pi.keys():
            self.panel[pk] = SPanel.ScrolledPanel(
                                                  self, 
                                                  name="%s_panel"%(pk), 
                                                  pos=pi[pk]["pos"], 
                                                  size=pi[pk]["sz"], 
                                                  style=pi[pk]["style"],
                                                 )
            self.panel[pk].SetBackgroundColour(pi[pk]["bgCol"]) 

        ##### beginning of setting up top UI panel interface -----
        bw = 5 # border width for GridBagSizer
        vlSz = (-1, 20) # size of vertical line seprator
        self.gbs["tUI"] = wx.GridBagSizer(0,0)
        row = 0
        col = 0
        btn = wx.Button(
                            self.panel["tUI"],
                            -1,
                            label="Select folders",
                            name="selFolders_btn",
                       )
        btn.Bind(wx.EVT_LEFT_DOWN, self.onButtonPressDown)
        self.gbs["tUI"].Add(
                            btn, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        col += 1
        chk = wx.CheckBox(
                            self.panel["tUI"],
                            -1,
                            label="Include sub-folders",
                            name="subFolders_chk",
                         )
        chk.SetValue(False)
        self.gbs["tUI"].Add(
                            chk, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        col += 1
        self.gbs["tUI"].Add(
                            wx.StaticLine(
                                            self.panel["tUI"],
                                            -1,
                                            size=vlSz,
                                            style=wx.LI_VERTICAL,
                                         ),
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           ) # vertical line separator
        col += 1
        chk = wx.CheckBox(
                            self.panel["tUI"],
                            -1,
                            label="Move renamed files to a folder",
                            name="moveRenFiles_chk",
                         )
        chk.SetValue(False)
        chk.Bind(wx.EVT_CHECKBOX, self.onCheckBox)
        self.gbs["tUI"].Add(
                            chk, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        col += 1
        btn = wx.Button(
                            self.panel["tUI"],
                            -1,
                            label="Select folder to move renamed Files",
                            name="selFolder2move_btn",
                       )
        btn.Disable()
        btn.Bind(wx.EVT_LEFT_DOWN, self.onButtonPressDown)
        self.gbs["tUI"].Add(
                            btn, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        col += 1
        txt = wx.TextCtrl(
                            self.panel["tUI"], 
                            -1, 
                            value="",
                            name="selFolder2move_txt",
                            size=(200,-1),
                            style=wx.TE_READONLY,
                         )
        txt.Disable()
        txt.SetBackgroundColour('#999999')
        self.gbs["tUI"].Add(
                            txt, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        col += 1
        self.gbs["tUI"].Add(
                            wx.StaticLine(
                                            self.panel["tUI"],
                                            -1,
                                            size=vlSz,
                                            style=wx.LI_VERTICAL,
                                         ),
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           ) # vertical line separator
        col += 1
        btn = wx.Button(
                            self.panel["tUI"],
                            -1,
                            label="Run renaming",
                            name="run_btn",
                       )
        btn.Bind(wx.EVT_LEFT_DOWN, self.onButtonPressDown)
        self.gbs["tUI"].Add(
                            btn, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        self.panel["tUI"].SetSizer(self.gbs["tUI"])
        self.gbs["tUI"].Layout()
        self.panel["tUI"].SetupScrolling()
        ##### end of setting up top UI panel interface -----

        ##### beginning of setting up renaming parameter panel interface -----
        mw = bw*6 # margin in width
        mpSz = pi["mp"]["sz"]
        hlSz = (mpSz[0]-mw, -1) # size of horizontal line separator
        self.gbs["mp"] = wx.GridBagSizer(0,0)
        row = 0
        col = 0
        sTxt = setupStaticText(
                            self.panel["mp"], 
                            "Selected folders for renaming", 
                            font=self.fonts[2],
                              )
        self.gbs["mp"].Add(
                            sTxt, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        row += 1
        txt = wx.TextCtrl(
                            self.panel["mp"], 
                            -1, 
                            value="[EMPTY]; Please select folders",
                            name="selDir_txt",
                            size=(int(mpSz[0]*0.95), int(mpSz[1]*0.2)),
                            style=wx.TE_MULTILINE|wx.TE_READONLY,
                         )
        txt.SetBackgroundColour('#999999')
        self.gbs["mp"].Add(
                            txt, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           ) 
        row += 1
        self.gbs["mp"].Add(
                            wx.StaticLine(
                                            self.panel["mp"],
                                            -1,
                                            size=hlSz,
                                            style=wx.LI_HORIZONTAL,
                                         ),
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                          ) # horizontal line separator
        row += 1
        lbl = "Target files (you can use wildcard characters)."
        sTxt = setupStaticText(
                            self.panel["mp"], 
                            lbl, 
                            font=self.fonts[2],
                              )
        self.gbs["mp"].Add(
                            sTxt, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        row += 1
        txt = wx.TextCtrl(
                            self.panel["mp"], 
                            -1, 
                            value="*.*",
                            name="targetFN_txt",
                            size=(int(mpSz[0]*0.95), -1),
                            style=wx.TE_PROCESS_ENTER,
                         )
        txt.Bind(wx.EVT_TEXT_ENTER, self.onEnteredInTC)
        self.gbs["mp"].Add(
                            txt, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                          )
        row += 1
        col = 0
        self.gbs["mp"].Add(
                            wx.StaticLine(
                                            self.panel["mp"],
                                            -1,
                                            size=hlSz,
                                            style=wx.LI_HORIZONTAL,
                                         ),
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                          ) # horizontal line separator
        row += 1
        sTxt = setupStaticText(
                            self.panel["mp"], 
                            "List of files to be renamed.", 
                            font=self.fonts[2],
                              )
        self.gbs["mp"].Add(
                            sTxt, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        row += 1
        txt = wx.richtext.RichTextCtrl(
                            self.panel["mp"], 
                            -1, 
                            name="selFile_txt",
                            size=(int(mpSz[0]*0.95), int(mpSz[1]*0.4)),
                            style=wx.TE_MULTILINE|wx.TE_READONLY,
                         ) # selected files to be renamed
        txt.SetBackgroundColour('#999999')
        self.gbs["mp"].Add(
                            txt, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        row += 1
        self.gbs["mp"].Add(
                            wx.StaticLine(
                                            self.panel["mp"],
                                            -1,
                                            size=hlSz,
                                            style=wx.LI_HORIZONTAL,
                                         ),
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                          ) # horizontal line separator
        row += 1
        lbl = "New file-name format. (Don't put extension here."
        lbl += " It will be same as original file extension.)"
        sTxt = setupStaticText(
                            self.panel["mp"], 
                            lbl, 
                            font=self.fonts[2],
                            wrapWidth=int(mpSz[0]*0.95),
                              )
        self.gbs["mp"].Add(
                            sTxt, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        row += 1
        txt = wx.TextCtrl(
                            self.panel["mp"], 
                            -1, 
                            value="[oFileN]",
                            name="newFN_txt",
                            size=(int(mpSz[0]*0.95), -1),
                            style=wx.TE_PROCESS_ENTER,
                         )
        txt.Bind(wx.EVT_TEXT_ENTER, self.onEnteredInTC)
        self.gbs["mp"].Add(
                            txt, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        row += 1
        _choices = ['']
        for i in range(len(self.newFFO)):
            k = self.newFFO[i]
            _choices.append("[%s], %s"%(k, self.newFFOD[k]))
        cho = wx.Choice(
                            self.panel["mp"], 
                            -1,
                            name="newFNOption_cho",
                            choices=_choices,
                            size=(int(mpSz[0]*0.333), -1),
                       )
        cho.Bind(wx.EVT_CHOICE, self.onChoice)
        self.gbs["mp"].Add(
                            cho, 
                            pos=(row,col), 
                            flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                            border=bw,
                           )
        self.panel["mp"].SetSizer(self.gbs["mp"])
        self.gbs["mp"].Layout()
        self.panel["mp"].SetupScrolling()
        ##### end of setting up renaming parameter panel interface -----

        ### set up menu
        menuBar = wx.MenuBar()
        fileRenMenu = wx.Menu()
        selectFolders = fileRenMenu.Append(
                            wx.Window.NewControlId(), 
                            item="Select folders\tCTRL+O",
                                        )
        self.Bind(wx.EVT_MENU,
                  lambda event: self.onButtonPressDown(event, 'selectFolders'),
                  selectFolders)
        quit = fileRenMenu.Append(
                            wx.Window.NewControlId(), 
                            item="Quit\tCTRL+Q",
                                 )
        menuBar.Append(fileRenMenu, "&FileRenamer")
        self.SetMenuBar(menuBar)
        
        ### set up hot keys
        idSelFolders = wx.Window.NewControlId()
        idQuit = wx.Window.NewControlId()
        self.Bind(wx.EVT_MENU,
                  lambda event: self.onButtonPressDown(event, 'selectFolders'),
                  id=idSelFolders)
        self.Bind(wx.EVT_MENU, self.onClose, id=idQuit)
        accel_tbl = wx.AcceleratorTable([ 
                                    (wx.ACCEL_CMD,  ord('O'), idSelFolders), 
                                    (wx.ACCEL_CMD,  ord('Q'), idQuit), 
                                        ]) 
        self.SetAcceleratorTable(accel_tbl)

        ### set up status-bar
        self.statusbar = self.CreateStatusBar(1)
        self.sbBgCol = self.statusbar.GetBackgroundColour()
        self.timers["sbTimer"] = None 

        updateFrameSize(self, w_sz)

        self.Bind(wx.EVT_MENU, self.onClose, quit)

    #-------------------------------------------------------------------

    def setPanelInfo(self):
        """ Set panel information.

        Args: None

        Returns:
            pi (dict): Panel information.
        """
        if DEBUG: print("FileRenamerFrame.setPanelInfo()")

        w_sz = self.GetSize() # window size
        
        pi = {} # panel information 
        # top panel for UI 
        pi["tUI"] = dict(pos=(0, 0), 
                         sz=(w_sz[0], 40), 
                         bgCol="#cccccc", 
                         style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        tUISz = pi["tUI"]["sz"]
        # panel for setting parameters 
        pi["mp"] = dict(pos=(0, tUISz[1]),
                         sz=(w_sz[0], int(w_sz[1]-tUISz[1])),
                         bgCol="#cccccc",
                         style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        return pi
    
    #-------------------------------------------------------------------
   
    def onButtonPressDown(self, event, flag=''):
        """ wx.Butotn was pressed.

        Args:
            event (wx.Event)
            flag (str, optional): Specifying intended operation of 
              the function call.

        Returns: None
        """
        if DEBUG: print("FileRenamerFrame.onButtonPressDown()")

        objName = ''
        if flag == '':
            obj = event.GetEventObject()
            objName = obj.GetName()

        if flag == "selectFolders" or objName == "selFolders_btn":
        # select folders to rename
            dlg = MDD.MultiDirDialog(
                         None, 
                         title="Select folders to apply renaming operations.",
                         defaultPath=CWD,
                         agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST,
                                    ) # select multiple folders
            if dlg.ShowModal() == wx.ID_OK:
                self.selectedFolders = dlg.GetPaths()
                ### remove root string, due to MultiDirDialog's some return string 
                for i, fp in enumerate(self.selectedFolders):
                    si = fp.find("/")
                    if si != -1:
                        fp = fp[fp.index("/"):] # cut off the fisrt directory name,
                          # MultiDirDialog returns with disk name as root
                          # Instead of '/tmp', it returns 'Macintosh HD/tmp'.
                    self.selectedFolders[i] = fp 

                ### include sub folder, if "including sub folder" option was checked.
                sfChk = wx.FindWindowByName("subFolders_chk", self.panel["tUI"])
                if sfChk.GetValue() == True:
                    ### update folder lists
                    folderL = copy(self.selectedFolders)
                    self.selectedFolders = []
                    for dp in folderL:
                    # go through folder which use selected
                        self.selectedFolders.append(dp) # append the selected folder
                        self.addFolders(dp) # add folders in this folder

                ### show folder list in UI
                selDir_txt = wx.FindWindowByName("selDir_txt", 
                                                 self.panel["mp"])
                _txt = str(self.selectedFolders)
                _txt = _txt.strip("[]").replace("'","").replace(", ","\n\n")
                selDir_txt.SetValue(_txt) # show list of selected folders

                self.updateFileList() # update files to be renamed
            dlg.Destroy()

        elif objName == "selFolder2move_btn":
        # select folder to move renamed files
            dlg = wx.DirDialog(self, 
                               "Select a folder to move renamed files.", 
                               CWD) # select folder
            if dlg.ShowModal() == wx.ID_OK:
                self.folder2moveRenFile = dlg.GetPath() # get folder path
                tc = wx.FindWindowByName("selFolder2move_txt", self.panel["tUI"])
                tc.SetValue(self.folder2moveRenFile) # show it on UI
                self.updateFileList() # update files to be renamed
            dlg.Destroy()
        
        elif objName == "run_btn":
            msg = "Renamed files -----\n\n" # result message 
            msg4log = "" # log message
            for i, fp in enumerate(self.fileList):
                newFP = self.nFileList[i]
                rename(fp, newFP) # rename file
                msg4log += "%s, %s, %s\n\n"%(get_time_stamp(), fp, newFP)
                msg += "%s\n\n"%(newFP)
            writeFile(self.logFile, msg4log) # logging results
            self.initList() # clear all file lists
            wx.MessageBox(msg, 'Results', wx.OK)

    #-------------------------------------------------------------------
    
    def onCheckBox(self, event):
        """ wx.CheckBox was checked/unchecked.
        
        Args: event (wx.Event)

        Returns: None
        """
        obj = event.GetEventObject()
        objName = obj.GetName()

        if objName == "moveRenFiles_chk":
            chk = wx.FindWindowByName(objName, self.panel["tUI"])
            btn = wx.FindWindowByName("selFolder2move_btn", self.panel["tUI"])
            txt = wx.FindWindowByName("selFolder2move_txt", self.panel["tUI"])
            if chk.GetValue() == True:
                btn.Enable()
                txt.Enable()
                txt.SetBackgroundColour('#ffffff')
            else:
                btn.Disable()
                txt.SetValue('')
                txt.Disable()
                txt.SetBackgroundColour('#999999')
                self.folder2moveRenFile = ""
    
    #-------------------------------------------------------------------

    def onChoice(self, event):
        """ wx.Choice was changed.

        Args: event (wx.Event)

        Returns: None
        """
        if DEBUG: print("FileRenamerFrame.onChoice()")
        
        obj = event.GetEventObject()
        objName = obj.GetName()

        ### update newFN_txt with option choice.
        if objName == 'newFNOption_cho':
            chosenOStr = obj.GetString(obj.GetSelection()) # chosen option 
            if chosenOStr == '': return
            chosenOStr = chosenOStr.split(',')[0].strip()
            txtCtrlName = objName.replace("Option","").replace("_cho","_txt")
            txtCtrl = wx.FindWindowByName(txtCtrlName, self.panel["mp"])
            ### add option string to its textctrl value
            _txt = txtCtrl.GetValue()
            _txt += "%s"%(chosenOStr)
            txtCtrl.SetValue(_txt)
            self.updateFileList()
                    
    #-------------------------------------------------------------------

    def onEnteredInTC(self, event):
        """ 'Enter' was pressed in wx.TextCtrl.

        Args: event (wx.Event)

        Returns: None
        """
        if DEBUG: print("FileRenamerFrame.onEnteredInTC()")
        
        obj = event.GetEventObject()
        objName = obj.GetName()
        
        if objName in ['targetFN_txt', 'newFN_txt']:
        # target file format or new file format has changed
            self.updateFileList()
    
    #-------------------------------------------------------------------
    
    def addFolders(self, dp):
        """ Adding sub-folders in the 'self.selectedFolders' list.

        Args:
            dp (str): Folder path to look for any other sub folders in it.

        Returns:
            None
        """
        if DEBUG: print("FileRenamerFrame.addFolders()")

        for fp in glob(path.join(dp, '*')):
        # go through everything in the selected folder
            if path.isdir(fp) == True: # this is a folder
                self.selectedFolders.append(fp) # add this sub-folder 
                self.addFolders(fp) # add folders in this sub-folder
    
    #-------------------------------------------------------------------
    
    def updateFileList(self):
        """ This function is called when selected folders or target file 
        name or extension has changed. 
        This function updates file list, which will be renamed.

        Args: None

        Returns: None
        """
        if DEBUG: print("FileRenamerFrame.updateFileList()")

        fL = []
        tcFN = wx.FindWindowByName("targetFN_txt", self.panel["mp"])
        fileForm = "%s"%(tcFN.GetValue()) 

        ### update self.fileList
        for dp in self.selectedFolders:
            p = path.join(dp, fileForm)
            fL += glob(p)
        self.fileList = fL

        ### update TextCtrl to show files to be renamed
        self.nFileList = [] # new file path list 
        tcNew = wx.FindWindowByName("newFN_txt", self.panel["mp"])
        newForm = tcNew.GetValue() # new file format
        _txt = ""
        incN = 1 
        zeroPadN = len(str(len(self.fileList)))
        folderPath = ""
        prevFolderP = ""
        tc = wx.FindWindowByName("selFile_txt", self.panel["mp"])
        tc.SetValue("") # delete the current contents
        for i, fp in enumerate(self.fileList):
            bn = path.basename(fp)
            _fp = fp.replace(bn, "")
            tc.WriteText(_fp)
            tc.BeginTextColour('#cccccc')
            tc.WriteText(bn)
            tc.EndTextColour()
            tc.Newline()
            tc.WriteText(" --->> ")
            folderPath = fp.replace(bn, "")
            if i == 0: prevFolderP = copy(folderPath)
            fn = bn.split('.')
            oFN, oFExt= fn[0], fn[-1] # origianl file-name and extension
            newFN = copy(newForm) 
            for k in self.newFFO:
                tStr = "[%s]"%(k) # target string
                if not tStr in newFN: continue

                if k == "incNumInFolder":
                    if folderPath != prevFolderP: # folder path changed
                        incN = 1 
                
                ### determine replacement string
                if k == "oFileN":
                    rStr = oFN 
                elif k == "folderN":
                    _fp = folderPath.split("/")
                    while '' in _fp: _fp.remove('')
                    if len(_fp) > 0: rStr = _fp[-1]
                    else: rStr = ""
                elif k.startswith("incNum"):
                    rStr = str(incN)
                    rStr = rStr.zfill(zeroPadN)
                elif k == "ts":
                    rStr = get_time_stamp()
                
                if k.startswith("incNum"): incN += 1
                newFN = newFN.replace(tStr, rStr) # replace string
           
            if self.folder2moveRenFile != "":
            # there's a different folder path to move renamed files
                newFP = path.join(self.folder2moveRenFile, "%s.%s"%(newFN, oFExt))
            else:
                newFP = path.join(folderPath, "%s.%s"%(newFN, oFExt))
            self.nFileList.append(newFP) # store the new file-path
            newFN = path.basename(newFP)
            newFP = newFP.replace(newFN, "")
            tc.WriteText(newFP) # write file-path
            tc.BeginTextColour('#aa0000')
            tc.WriteText(newFN) # write new file-name
            tc.EndTextColour()
            for x in range(2): tc.Newline()
            prevFolderP = copy(folderPath)
    
    #-------------------------------------------------------------------
   
    def initList(self):
        """ Clear all the lists (after renaming)

        Args: None

        Returns: None
        """
        if DEBUG: print("FileRenamerFrame.initList()")
        self.selectedFolders = [] # list of selected folders
        self.fileList = [] # file list to be renamed
        self.nFileList = [] # file list with new file names
        txt = wx.FindWindowByName("selDir_txt", self.panel["mp"])
        txt.SetValue("")
        txt = wx.FindWindowByName("targetFN_txt", self.panel["mp"])
        txt.SetValue("*.*")
        txt = wx.FindWindowByName("selFile_txt", self.panel["mp"])
        txt.SetValue("")
        txt = wx.FindWindowByName("newFN_txt", self.panel["mp"])
        txt.SetValue("[oFileN]")
    
    #-------------------------------------------------------------------

    def onClose(self, event):
        """ Close this frame.

        Args: event (wx.Event)

        Returns: None
        """
        if DEBUG: print("FileRenamerFrame.onClose()")

        for k in self.timers.keys():
            if isinstance(self.timers[k], wx.Timer):
                self.timers[k].Stop()
        self.Destroy()

    #-------------------------------------------------------------------

#=======================================================================

class FileRenamerApp(wx.App):
    """ Initializing FileRenamer app with FileRenamerFrame.

    Attributes:
        frame (wx.Frame): FileRenamerFrame.
    """
    def OnInit(self):
        if DEBUG: print("FileRenamerApp.OnInit()")
        self.frame = FileRenamerFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

#=======================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-w': GNU_notice(1)
        elif sys.argv[1] == '-c': GNU_notice(2)
    else:
        GNU_notice(0)
        app = FileRenamerApp(redirect = False)
        app.MainLoop()
