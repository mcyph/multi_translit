# Microsoft Developer Studio Project File - Name="translit" - Package Owner=<4>
# Microsoft Developer Studio Generated Build File, Format Version 6.00
# ** DO NOT EDIT **

# TARGTYPE "Win32 (x86) Dynamic-Link Library" 0x0102

CFG=translit - Win32 Debug
!MESSAGE This is not a valid makefile. To build this project using NMAKE,
!MESSAGE use the Export Makefile command and run
!MESSAGE 
!MESSAGE NMAKE /f "translit.mak".
!MESSAGE 
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "translit.mak" CFG="translit - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "translit - Win32 Debug" (based on "Win32 (x86) Dynamic-Link Library")
!MESSAGE "translit - Win32 Release" (based on "Win32 (x86) Dynamic-Link Library")
!MESSAGE 

# Begin Project
# PROP AllowPerConfigDependencies 0
# PROP Scc_ProjName ""
# PROP Scc_LocalPath ""
CPP=cl.exe
MTL=midl.exe
RSC=rc.exe

!IF  "$(CFG)" == "translit - Win32 Debug"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 1
# PROP BASE Output_Dir ".\translit___Win32_Debug"
# PROP BASE Intermediate_Dir ".\translit___Win32_Debug"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 1
# PROP Output_Dir ".\translit___Win32_Debug"
# PROP Intermediate_Dir ".\translit___Win32_Debug"
# PROP Target_Dir ""
# ADD BASE CPP /nologo /MTd /ZI /W3 /Od /D "WIN32" /D "_DEBUG" /D "_WINDOWS" /D "_USRDLL" /D "TRANSLIT_EXPORTS" /D "_MBCS" /Fp".\translit___Win32_Debug/translit.pch" /Fo".\translit___Win32_Debug/" /Fd".\translit___Win32_Debug/" /GZ /c /GX 
# ADD CPP /nologo /MTd /ZI /W3 /Od /D "WIN32" /D "_DEBUG" /D "_WINDOWS" /D "_USRDLL" /D "TRANSLIT_EXPORTS" /D "_MBCS" /Fp".\translit___Win32_Debug/translit.pch" /Fo".\translit___Win32_Debug/" /Fd".\translit___Win32_Debug/" /GZ /c /GX 
# ADD BASE MTL /nologo /D"_DEBUG" /mktyplib203 /tlb".\translit___Win32_Debug\translit.tlb" /win32 
# ADD MTL /nologo /D"_DEBUG" /mktyplib203 /tlb".\translit___Win32_Debug\translit.tlb" /win32 
# ADD BASE RSC /l 1033 /d "_DEBUG" 
# ADD RSC /l 1033 /d "_DEBUG" 
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo 
# ADD BSC32 /nologo 
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib odbc32.lib odbccp32.lib boost_python_debug.lib icudt.lib icuio.lib icule.lib iculx.lib icuuc.lib icuin.lib /nologo /dll /out:".\translit___Win32_Debug\translit.dll" /incremental:no /debug /pdb:".\translit___Win32_Debug\translit.pdb" /pdbtype:sept /subsystem:windows /implib:".\translit___Win32_Debug/translit.lib" 
# ADD LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib odbc32.lib odbccp32.lib boost_python_debug.lib icudt.lib icuio.lib icule.lib iculx.lib icuuc.lib icuin.lib /nologo /dll /out:".\translit___Win32_Debug\translit.dll" /incremental:no /debug /pdb:".\translit___Win32_Debug\translit.pdb" /pdbtype:sept /subsystem:windows /implib:".\translit___Win32_Debug/translit.lib" 

!ELSEIF  "$(CFG)" == "translit - Win32 Release"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 0
# PROP BASE Output_Dir ".\translit___Win32_Release"
# PROP BASE Intermediate_Dir ".\translit___Win32_Release"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 0
# PROP Output_Dir ".\translit___Win32_Release"
# PROP Intermediate_Dir ".\translit___Win32_Release"
# PROP Target_Dir ""
# ADD BASE CPP /nologo /MT /W3 /O2 /Ob1 /D "WIN32" /D "NDEBUG" /D "_WINDOWS" /D "_USRDLL" /D "TRANSLIT_EXPORTS" /D "_MBCS" /GF /Gy /Fp".\translit___Win32_Release/translit.pch" /Fo".\translit___Win32_Release/" /Fd".\translit___Win32_Release/" /c /GX 
# ADD CPP /nologo /MT /W3 /O2 /Ob1 /D "WIN32" /D "NDEBUG" /D "_WINDOWS" /D "_USRDLL" /D "TRANSLIT_EXPORTS" /D "_MBCS" /GF /Gy /Fp".\translit___Win32_Release/translit.pch" /Fo".\translit___Win32_Release/" /Fd".\translit___Win32_Release/" /c /GX 
# ADD BASE MTL /nologo /D"NDEBUG" /mktyplib203 /tlb".\translit___Win32_Release\translit.tlb" /win32 
# ADD MTL /nologo /D"NDEBUG" /mktyplib203 /tlb".\translit___Win32_Release\translit.tlb" /win32 
# ADD BASE RSC /l 1033 /d "NDEBUG" 
# ADD RSC /l 1033 /d "NDEBUG" 
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo 
# ADD BSC32 /nologo 
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib odbc32.lib odbccp32.lib icuuc.lib icuin.lib boost_python.lib /nologo /dll /out:".\translit___Win32_Release\translit.dll" /incremental:no /pdb:".\translit___Win32_Release\translit.pdb" /pdbtype:sept /subsystem:windows /implib:".\translit___Win32_Release/translit.lib" 
# ADD LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib odbc32.lib odbccp32.lib icuuc.lib icuin.lib boost_python.lib /nologo /dll /out:".\translit___Win32_Release\translit.dll" /incremental:no /pdb:".\translit___Win32_Release\translit.pdb" /pdbtype:sept /subsystem:windows /implib:".\translit___Win32_Release/translit.lib" 

!ENDIF

# Begin Target

# Name "translit - Win32 Debug"
# Name "translit - Win32 Release"
# Begin Group "Source Files"

# PROP Default_Filter "cpp;c;cxx;rc;def;r;odl;idl;hpj;bat"
# Begin Source File

SOURCE=main.cpp

!IF  "$(CFG)" == "translit - Win32 Debug"

# ADD CPP /nologo /Od /D "WIN32" /D "_DEBUG" /D "_WINDOWS" /D "_USRDLL" /D "TRANSLIT_EXPORTS" /D "_MBCS" /GZ /GX 
!ELSEIF  "$(CFG)" == "translit - Win32 Release"

# ADD CPP /nologo /O2 /D "WIN32" /D "NDEBUG" /D "_WINDOWS" /D "_USRDLL" /D "TRANSLIT_EXPORTS" /D "_MBCS" /GX 
!ENDIF

# End Source File
# End Group
# Begin Group "Header Files"

# PROP Default_Filter "h;hpp;hxx;hm;inl"
# Begin Source File

SOURCE=.\Translit.h
# End Source File
# Begin Source File

SOURCE=.\UniStrConvert.h
# End Source File
# End Group
# Begin Group "Resource Files"

# PROP Default_Filter "ico;cur;bmp;dlg;rc2;rct;bin;rgs;gif;jpg;jpeg;jpe"
# End Group
# End Target
# End Project

