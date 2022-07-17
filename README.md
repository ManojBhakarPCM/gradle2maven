# gradle2maven

A Script to Convert Gradle Java Project Folder to Maven Java Project

Necessity is the mother of invention !!

THE NECESSITY::
i was creating and apk editor. then i got need to modify jadx code for faster smali to java conversion. because existing jadx convert it in about 4 seconds.. which was very slow for my app.
so, i downloaded jadx source code and opened in intellij. then the show began.. intellij downloaded about 1 GB of modules.. what the hell ? 
basically, every big company thinks that everyone in this world has very superfast internet and dont want to store anything on their computer.

so somehow i managed it. but then the code structure looked very complicated.. i was unable to understand what is going on in gradle files.

but i know how java works, so i created this script.

THE INVENTION:
so how this script works:
1. you download source code from github.
2. you extract the source zip somewhere.
3. you double click the script.
4. choose folder dialog appears. you select source folder.

*. script creates a new folder named "new_project" near orignal folder.
*. script creates 3 folders in it. lib,src,res.
*. script walks in source dir.
*. if find "build.gradle" then it search defined dependency in it by a regex, and copy dependency to pom.xml in appropriate format.
*. if it finds that file is java and path contains "\src\" then it opens that java file, read package name. and creates folders according to its package names in src folder and then copy it.
*. if it finds that path contains '\resources\' then it copies its file to res folder.
*. depending on the opt_copyTest variable value, it either skips the test folders or include them.
*. if path contains "\libs\" and file name ends with ".jar" then it copy to lib folder.

5. after finishing script, you right click on "new_project" and select open as intellij project.
6. intellij reads pom.xml and downloads the dependencies.
7. sometimes, intellij cant find all dependencies (dont know why.) so you need to manually download and copy them in lib folder. then right click on the copied jar and at the bottom, select option "add as library"
  then rebuild the code. if code is built successfully, be happy, if not , it will show another unresolved dependency. you copy the name of unresoved dependency and search it on google. then download it.. then copy it in lib folder. them add as library. then build.. then repeat..
8. before doing the above.. you need to right click jars on the lib folder and add as library.
9. before doing all of above, you need to right click on src folder and choose "mark as source dir" and for res folder, choose "mark as resources"
10. or perhaps , before doing all of above, you need to select JDK version.
11. if anything goes wrong, you just need to delete the new_project folder, and run the script again. its fast.

NOTE: the actual dependency dont hog data. they are maximum 25 MB combined.
