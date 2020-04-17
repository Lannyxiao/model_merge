import maya.cmds as cmds 
import maya.mel as mel 
import os

def convert():
    cmds.file(f=1,new=1)
    #模型的文件路径，请自行改动
    path = "C:/Users/Lan/Desktop/jf_lan/Test" 
    files = os.listdir(path)
    index = 0
    groupIndex = 0
    lastString = "0000"
    currentString = "0000"
    fileIndexToName = {}

    for afile in files:
        if(str.isdigit(afile[3:7])):
            if index == 0:
                fileIndexToName[groupIndex] = {afile}
            else:
                if afile[3:7] == lastString:
                    fileIndexToName[groupIndex].add(afile)
                else:
                    lastString = afile[3:7]
                    groupIndex += 1
                    fileIndexToName[groupIndex] = {afile}
            index += 1
            
    if cmds.pluginInfo("fbxmaya",q=1,l=1) !=1: 
        mds.loadPlugin("fbxmaya",qt=1)
        
    axis = ['x', 'y', 'z']
    attrs = ['t', 'r', 's']
 
    for groupName, value in fileIndexToName.items():
        for apath in value: 
            cmds.file(path+"/"+apath, i=True, mergeNamespacesOnClash=True, namespace=':')
        cmds.select('NULL',r=1)
        cmds.delete()
        cmds.select(all=1)
        sel = cmds.ls(sl=1, transforms=1 )
        for obj in sel:
            for ax in axis:
                for attr in attrs:
                    cmds.setAttr(obj+'.'+attr+ax, lock=0)
        cmds.select(all=1)
        fbxExportName = path + "/" + str(groupName) + list(value)[0] + ".fbx"
        mel.eval('FBXExportScaleFactor 1;')
        mel.eval('FBXExportInAscii -v 1;')
        mel.eval('FBXExportSmoothingGroups -v 1;')
        mel.eval('FBXExportSmoothMesh -v 1;')
        mel.eval('FBXExportTriangulate -v 0;')
        mel.eval('FBXExportUpAxis y;')
        mel.eval('FBXExport -f "'+ fbxExportName +'" -s;')
        cmds.select(all=1) 
        cmds.delete()
        cmds.flushUndo()
        cmds.clearCache( all=True )
        cmds.DeleteHistory()
convert()
