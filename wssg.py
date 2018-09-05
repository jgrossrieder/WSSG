import click
import getpass
import os
import ntpath
import filecmp
from shutil import copyfile
from PIL import Image



@click.command()
@click.argument('targetpath', type=click.Path())
def importScreens(targetpath):
    sourcePath = computeSourcePath()
    checkfolder(sourcePath)
    createfolder(targetpath)

    click.echo("Importing Windows startup screens from %s to %s" % (sourcePath, targetpath))
    for sourceFile in os.listdir(sourcePath):
        importfile(os.path.join(sourcePath,sourceFile), targetpath)

def importfile(sourcefile,targetpath):
    destinationpath = computetargetfile(sourcefile, targetpath)+".jpg"
    if mustbeimported(sourcefile,destinationpath):
        click.echo("Importing %s to %s" % (sourcefile, destinationpath))
        copyfile(sourcefile, destinationpath)

def mustbeimported(sourcepath, destinationpath):
    image = Image.open(sourcepath)
    if image.size[0] >=1920:
        return not os.path.exists(destinationpath) or filecmp.cmp(sourcepath, destinationpath)
    return False

def computetargetfile(sourcefile, targetpath):
    filename = ntpath.basename(sourcefile)
    return os.path.join(targetpath,filename)

def checkfolder(foldertocheck):
    if not os.path.isdir(foldertocheck):
        raise FileNotFoundError()

def createfolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    elif not os.path.isdir(folder):
        raise NotADirectoryError()

def computeSourcePath():
    return  "C:\\Users\\"+getpass.getuser()+"\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"


if __name__ == '__main__':
    importScreens()