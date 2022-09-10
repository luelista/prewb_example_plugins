"""
This plugin always shows a project selection dialog prior to starting the application, instead
of automatically opening the most recent project.

"""

from pre_workbench.macros.macroenv import *
from pre_workbench.configs import *
from pre_workbench.guihelper import qApp
from pre_workbench.mainwindow import WorkbenchMain
import sys
def projectchooser():
    lastprj = getValue("ProjectMru",[])
    if qApp().args.choose_project or qApp().args.project_dir:
        return
    answer = showListSelectDialog(list(zip(lastprj,lastprj))+[("--choose-project", "Ordner wählen...")],qApp().project.projectFolder,"Welches Projekt möchtest du öffnen?")
    if not answer:
        sys.exit(0)
    if answer != qApp().project.projectFolder:
        WorkbenchMain.openProjectInNewWindow(None, answer)
        import time; time.sleep(1)
        sys.exit(0)

projectchooser()
