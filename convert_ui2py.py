import subprocess


def convertCourseExtraFileDownloadDialog():
    subprocess.run(['pyuic5',
 'Design\\qtDesigner\\courseDownloadFilesTypeDialog.ui',
 '-o',
 'courseExtraFileDownloadDialog\\courseExtraFileDownloadDialog.py'])
    print('Ran pyuic5')

def convertAppUI():
    subprocess.run(['pyuic5', 'Design\\qtDesigner\\app.ui', '-o', 'app.py'])
    print('Ran pyuic5')
    subprocess.run(['pyrcc5', 'Design\\qtDesigner\\resources.qrc', '-o', 'resources_rc.py'])
    print('Ran pyrcc5')

def convertWelcomeScreenDialog():
    subprocess.run(['pyuic5',
 'Design\\qtDesigner\\welcomeScreenDialog\\welcomeScreenDialog.ui',
 '-o',
 'welcomeScreenDialog\\welcomeScreenDialog.py'])
    print('Ran pyuic5')
    subprocess.run(['pyrcc5',
 'Design\\qtDesigner\\welcomeScreenDialog\\welcomeDialogResources.qrc',
 '-o',
 'welcomeScreenDialog\\welcomeDialogResources_rc.py'])
    print('Ran pyrcc5')

def convertDownloadEngineDialog():
    subprocess.run(['pyuic5',
                    'Design\\qtDesigner\\downloadEngineDialog\\downloadEngineDialog.ui',
                    '-o',
                    'downloadEngineDialog\\downloadEngineDialog.py'])
    print('Ran pyuic5')
    subprocess.run(['pyrcc5',
                    'Design\\qtDesigner\\downloadEngineDialog\\downloadEngineDialogResources.qrc',
                    '-o',
                    'downloadEngineDialog\\downloadEngineDialogResources_rc.py'])
    print('Ran pyrcc5')

def convertDownloadACDialog():
    subprocess.run(['pyuic5',
                    'Design\\qtDesigner\\downloadACDialog\\downloadACDialog.ui',
                    '-o',
                    'downloadACDialog\\downloadACDialog.py'])
    print('Ran pyuic5')
    subprocess.run(['pyrcc5',
                    'Design\\qtDesigner\\downloadACDialog\\downloadACDialogResources.qrc',
                    '-o',
                    'downloadACDialog\\downloadACDialogResources_rc.py'])
    print('Ran pyrcc5')
    
def convertSplashScreenDialog():
    subprocess.run(['pyuic5',
                    'Design\\qtDesigner\\splashScreenDialog\\splashScreenDialog.ui',
                    '-o',
                    'splashScreenDialog\\splashScreenDialog.py'])
    print('Ran pyuic5')
    subprocess.run(['pyrcc5',
                    'Design\\qtDesigner\\splashScreenDialog\\splashScreenDialogResources.qrc',
                    '-o',
                    'splashScreenDialog\\splashScreenDialogResources_rc.py'])
    print('Ran pyrcc5')



def convertFtpGetUsernamePasswordDialog():
    subprocess.run(['pyuic5',
                    'Design\\qtDesigner\\ftpGetUsernamePasswordDialog\\ftpGetUsernamePasswordDialog.ui',
                    '-o',
                    'ftpGetUsernamePasswordDialog\\ftpGetUsernamePasswordDialog.py'])
    print('Ran pyuic5')
    subprocess.run(['pyrcc5',
                    'Design\\qtDesigner\\ftpGetUsernamePasswordDialog\\ftpGetUsernamePasswordDialogResources.qrc',
                    '-o',
                    'ftpGetUsernamePasswordDialog\\ftpGetUsernamePasswordDialogResources_rc.py'])
    print('Ran pyrcc5')


def convertFtpDownloadDialog():
    subprocess.run(['pyuic5',
                    'Design\\qtDesigner\\ftpDownloadDialog\\ftpDownloadDialog.ui',
                    '-o',
                    'ftpDownloadDialog\\ftpDownloadDialog.py'])
    print('Ran pyuic5')
    subprocess.run(['pyrcc5',
                    'Design\\qtDesigner\\ftpDownloadDialog\\ftpDownloadDialogResources.qrc',
                    '-o',
                    'ftpDownloadDialog\\ftpDownloadDialogResources_rc.py'])
    print('Ran pyrcc5')