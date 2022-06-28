import os
import sys
import re
from os import walk
from tkinter import Tk, filedialog
from pathlib import Path
import shutil

# enable VT100 to color the console.
import ctypes
kernel32 = ctypes.WinDLL('kernel32')
hStdOut = kernel32.GetStdHandle(-11)
mode = ctypes.c_ulong()
kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
mode.value |= 4
kernel32.SetConsoleMode(hStdOut, mode)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



#print(f"{bcolors.FAIL}Warning: No active frommets remain. Continue?{bcolors.ENDC}")

# =============================== Options =======================================
opt_copySrc = True;
opt_copyRes = True;
opt_copyTest = False;
# =============================== Functions =====================================


def copySRC(src,pkg,filepath):
    
    sorc = filepath
    dest = src + "\\" + pkg.replace(".","\\")
    Path(dest).mkdir(parents=True, exist_ok=True)
    shutil.copy(sorc,dest)
    print("from: " + sorc + "\nDest: " + dest + "\n")

def copyRES(res,filepath,name):
    #first extract dest path.
    sFol = str(Path(filepath).parent.absolute())
    #now split on resources.
    try:    #TODO: this is dirty method.
        sPaths = sFol.split("\\resources\\")
        dest = res + "\\" + sPaths[1]
        sorc = filepath
        Path(dest).mkdir(parents=True, exist_ok=True)
        shutil.copy(sorc,dest)
        print("from: " + sorc + "\nDest: " + dest + "\n")
    except:
        #print(f"{bcolors.FAIL}split did not work for:" + name + "|" + filepath + f"{bcolors.ENDC}\n")
        shutil.copy(filepath,res)

def copyLIB(lib,filepath):
    shutil.copy(filepath,lib)


def addd(name):
    tmp = name.split(":")
    outt = '\t<dependency>\n\t\t<groupId>' + tmp[0] + '</groupId>\n\t\t<artifactId>' + tmp[1] + '</artifactId>\n\t\t<version>' + tmp[2] + '</version>\n\t</dependency>\n'
    return outt

def copyDEP(filepath):
    regex = "['\"]+([\w\d\.\-\_]+:[\w\d\.\-\_]+:[\w\d\.\-\_\$\{\}]+)['\"]+"
    data = ""
    ret = ""
    f = open(filepath,'r', encoding='utf-8')
    try:
        data=f.read()
        f.close()
    except:
        print(f"{bcolors.FAIL}Error: cant open build.gradle{bcolors.ENDC}")
        return ""
    result = re.findall(regex, data)
    if len(result)>0:
        for r in result:
           ret += addd(r)
    return ret

def collectProps(filepath):
    global gprops
    data = ""
    f = open(filepath,'r', encoding='utf-8')
    try:
        data=f.read()
        f.close()
    except:
        print(f"{bcolors.FAIL}Error: cant open build.properties{bcolors.ENDC}")
        return ""
    lines = data.split('\n')
    for l in lines:
        l = l.strip()
        if l=="":
            continue
        if "=" in l:
            pdata = l.split("=")
            key = pdata[0]
            val = pdata[1]
            gprops[key] = val
        #gprops[pdata[0]] = pdata[1]


root = Tk() # pointing root to Tk() to use it as Tk() in program.
root.withdraw() # Hides small tkinter window.
root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
open_file = filedialog.askdirectory() # Returns opened path as str
desktopPath_no_slash = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

rootpath = open_file
#Path("/my/directory").mkdir(parents=True, exist_ok=True)
#first of create a folder and sub folders named - res and src and lib.

project_path =  str(Path(rootpath).parent.absolute()) + "new_project"
#print(project_path)

src_folder = project_path + "\\src"
res_folder = project_path + "\\res"
lib_folder = project_path + "\\lib"

Path(src_folder).mkdir(parents=True, exist_ok=True)
Path(res_folder).mkdir(parents=True, exist_ok=True)
Path(lib_folder).mkdir(parents=True, exist_ok=True)

#sys.exit(0)
xml = '<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">\n<modelVersion>4.0.0</modelVersion>\n<groupId>org.manoj.bhakar</groupId>\n<artifactId>my-project</artifactId>\n<version>1.0</version>\n<dependencies>\n';
#pattern = '(\-?\d{8,20}L)\)'
pattern = 'package\s(.*);\n'

gprops = dict()

for root, dirs, files in walk(rootpath):
    for name in files:
        filepath = os.path.join(root, name)
        if name == 'build.gradle':
            xml += copyDEP(filepath)
            continue
        
        if name == 'gradle.properties':
            collectProps(filepath)
            continue
        
        if filepath.endswith(".jar") and "\\libs\\" in filepath:
            copyLIB(lib_folder,filepath)
            continue
            
        
        if not "\\src\\" in filepath:
            print(f"{bcolors.OKCYAN}Skipped [GRADLE]: " + filepath + f"{bcolors.ENDC}")
            continue
        
        if not opt_copyTest:
            if "\\test\\" in filepath:
                print(f"{bcolors.OKCYAN}Skipped [TEST]: " + filepath + f"{bcolors.ENDC}")
                continue
                
                
        if opt_copyRes:
            if "\\resources\\" in filepath:
                copyRES(res_folder,filepath,name)
                continue
            
            
        if not name.endswith(".java"):
            print(f"{bcolors.OKCYAN}Skipped [NOT JAVA]: " + filepath + f"{bcolors.ENDC}")
            continue
            
            
        data = ""
        f = open(filepath,'r', encoding='utf-8')
        try:
            data = f.read()
            f.close()
        except:
            print("Error file:" + filepath)
        result = re.findall(pattern, data)
        if len(result)>0:
            copySRC(src_folder,result[0],filepath)
            
for key,val in gprops.items():
    xml = xml.replace("${" + key + "}",val)
fo = open(project_path + "\\pom.xml", "w")
fo.write(xml + "</dependencies>\n</project>")
fo.close()
print(gprops)
#os.startfile(desktopPath_no_slash + "/pythonSearchOutput.txt")
