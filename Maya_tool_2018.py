import maya.cmds as mc
import asset_import_tool
mc.internalVar(upd=True)

if mc.window("poseWindow", ex=True):
    mc.deleteUI("poseWindow", window=True)
    
#------------------------------------------------Create Wintdow----------------------------------------------------

  
mc.window("poseWindow", t="Maya Tool Box - isafx.com",s=False)
mc.windowPref("poseWindow",widthHeight=(200,150),topLeftCorner=(500,1100)	)

myForm = mc.formLayout()
myTabs = mc.tabLayout()
mc.formLayout(myForm, edit=True, attachForm=[(myTabs, "top", 10), (myTabs, "bottom", 10), (myTabs, "left", 10), (myTabs, "right", 10)])
mkPose_layout = mc.columnLayout()

#-------------------------------------------------1st Tab---------------------------------------------------------
poseShelf = mc.gridLayout(numberOfColumns=2, cellWidthHeight=(200, 50))
savpose_btn = mc.button(l = "Save Poses", w=150, h=150, c="createShelfButton_body(poseShelf2)")
rmvpose_btn = mc.button(l = "Remove All", w=150, h=150, c = "removeUI(poseShelf2)")

mc.setParent("..")

poseShelf2 = mc.gridLayout(numberOfColumns=3, cellWidthHeight=(130, 50))

mc.separator()
mc.text (label="Poses Library", align='center')
mc.separator()

mc.setParent("..")
mc.setParent("..")
#---------------------------------Joint Tool : Rename-------------------------------------------------------------------------            

#---------------------------------------------Ringging Tab-------------------------------------------------------------
Rigging_layout = mc.columnLayout()
RiggingShelf = mc.gridLayout(numberOfColumns=1, cellWidthHeight=(400, 42))
jnt_btn1 = mc.button(l = "Joint Tool : Constraints / Prefix", w=200, h=100, c = "build()")
jnt_btn2 = mc.button(l = "Joint Tool : Rename Hirerachy", w=200, h=100, c = "rename_joints()")
jnt_btn3 = mc.button(l = "Joint Tool : Create Joint on CV", w=200, h=100, c = "jntCV()")
jnt_btn4 = mc.button(l = "Alight Objects (1.Source 2.Target)", w=200, h=100, c = "alignobj()")
jnt_btn5 = mc.button(l = "Create Locator on Selected Obj", w=200, h=100, c = "locator2obj()")
jnt_btn6 = mc.button(l = "Create Slave Rigs (select source joint chain)", w=200, h=100, c = "cslave()")
jnt_btn7 = mc.button(l = "Create Joint Chain Controller / Constraint", w=200, h=100, c = "jntchainCtrl()")


mc.setParent("..")
mc.setParent("..")
#---------------------------------------------File Tab-------------------------------------------------------------
File_layout = mc.columnLayout()
FileShelf = mc.gridLayout(numberOfColumns=1, cellWidthHeight=(400, 50))
file_btn1 = mc.button(l = "Save as Maya Default", w=200, h=150, c = "save(fileName=None, ext=None, applyInfo=False, mayaExts=MAYA_EXTS)")
file_btn2 = mc.button(l = "Save as Maya Ascii", w=200, h=150, c = "saveAscii(applyInfo=False)")
file_btn3 = mc.button(l = "Save as Maya Binary", w=200, h=150, c = "saveBinary(applyInfo=False)")
file_btn4 = mc.button(l = "Save as Maya Ascii and Binary", w=200, h=150, c = "saveAsciiAndBinary(binaryFirst=True, applyInfo=False)")
file_btn5 = mc.button(l = "Set Info to current file", w=200, h=150, c = "setFileInfo()")
file_btn6 = mc.button(l = "Export Animation", w=200, h=150, c = "exportMesh() :")

mc.setParent("..")
mc.setParent("..")
#---------------------------------------------Asset Tab-------------------------------------------------------------
windowName    = "AssetImporterWindow"
assetGrid     = ""
importedList  = ""
from functools import partial

import asset_import_tool
reload(asset_import_tool)

importer = asset_import_tool.AssetImporter()

Asset_layout= mc.gridLayout( numberOfColumns=1, cellWidthHeight=(400, 300))

form = cmds.formLayout(numberOfDivisions=100)
    
reloadLibButton = cmds.button(label="Refresh Library")
scroll = cmds.scrollLayout(width=200)
    
library = cmds.gridLayout( numberOfColumns=5, cellWidthHeight=(100, 120))
    
cmds.setParent(form)
    
importedButtons = cmds.rowLayout(nc=2)
reloadImportedButton = cmds.button(label="Refresh Imported")
    
cmds.setParent(form)
importedList = cmds.textScrollList()
assetGrid     = library
importedList  = importedList    
                    
cmds.formLayout(form, e=True, 
                                attachForm=[(reloadLibButton, 'top', 5), (reloadLibButton, 'left', 5),
                                            (scroll, 'left', 5), (scroll, 'bottom', 5),
                                            (importedButtons, 'right', 5), (importedButtons, 'top', 5),
                                            (importedList, 'right', 5), (importedList, 'bottom', 5),
                                ],
                                attachControl=[(scroll, 'top', 5, reloadLibButton),
                                                (importedButtons, 'left', 5, scroll),
                                                (importedList, 'left', 5, scroll), (importedList, 'top', 5, importedButtons)
                                ],
                            )
def refreshImported(*args):
    cmds.textScrollList(importedList, e=True, removeAll=True)
    for node, asset in importer.findImported():
        cmds.textScrollList(importedList, e=True, append=node)
        
        
        
        
def importedItemSelected( *args):
    nodes = cmds.textScrollList(importedList, q=True, selectItem=True)
    if nodes:
        node = nodes[0]
        if cmds.objExists(node):
            cmds.select(node, r=True)

def refreshAssets( *args):
    
    children = cmds.gridLayout(assetGrid, q=True, childArray=True)
    if children:
        for child in children:
            cmds.deleteUI(child)
    cmds.gridLayout(assetGrid, e=True, vis=False) 
    
    for asset in importer.list(allShows=True):
        cmd = partial(importer.load, asset)
        cmds.iconTextButton(    parent  = assetGrid, 
                                    style   = 'iconAndTextVertical', 
                                    width   = 10, 
                                    height  = 10, 
                                    image1  = asset.image, 
                                    label   = '%s \n(%s)' % (asset.name, asset.show),
                                    command = cmd ) 
    cmds.gridLayout(assetGrid, e=True, vis=True)            
                               
           
            # set up the commands to run
cmds.button(reloadLibButton, e=True, c=refreshAssets)
cmds.button(reloadImportedButton, e=True, c=refreshImported)
cmds.textScrollList(importedList, e=True, selectCommand=importedItemSelected)


#-----------------------------------------------Tab Layout-----------------------------------------------------------
mc.setParent("..")
mc.setParent("..")
mc.tabLayout(myTabs, edit=True, tabLabel=[(mkPose_layout, "Pose Library"), (Rigging_layout, "Rigging Tools"), (File_layout, "File Tools"), (Asset_layout, "Asset Tools")])
mc.showWindow("poseWindow")


#-----------------------------------------------FUNCTIONS-----------------------------------------------------------
def removeUI(removelayout):
    a = mc.layout( removelayout, query=True, childArray=True )
    for i in a:
        if i.startswith('sh')==True:
            mc.deleteUI(i, control = True)


def createShelfButton_body(targetShelf_body):
    storeCmds_body = ""
    
    selPose = mc.ls(sl=True)
    
    if len(selPose) < 1:
        mc.warning("Must select at least one object!")
    else:
        for all in selPose:
            keyable = mc.listAttr(all, k=True, r=True, w=True, c=True, u=True)
            print keyable
            for vals in keyable:
                findVal = mc.getAttr(all + "." + vals)
                print findVal
                startCode = "setAttr "
                endCode = ";\n"
                saveToShelf = (startCode + (all + "." + vals) + " %f" + endCode) % findVal
                storeCmds_body += saveToShelf
                print storeCmds_body
        pd_body = mc.promptDialog(t="", m="Pose Name : ", b="Save")
        if pd_body == "Save":
            pd_body_name = mc.promptDialog(q=True, text=True)
 
            a = mc.shelfButton(l=pd_body_name, annotation=pd_body_name, imageOverlayLabel=pd_body_name, i1="C:/Users/Isabelle/Documents/2018Work/Maya/MayaToolBox_2018/Images/pose.png", command=storeCmds_body, p=targetShelf_body, sourceType="mel")




#----------------------------------Joint Create / Prefix Tool------------------------------------------------------------------------



    
def build():
    if mc.window("cJnt_win", ex=True):
        mc.deleteUI("cJnt_win", window=True)
    
    mc.window("cJnt_win", t="Create Joint @ Github/isascat", w=100, s=True)
    
    mc.columnLayout("c_layout", adj = True)
    
    mc.separator()
    
    mc.text("Select Joint(s)")
    
    mc.separator()
    
    mc.textFieldGrp("jntName", label="Prefix : ")
    mc.textFieldGrp("jntAmount", label="Joints : ")
    mc.textFieldGrp("jntSpacing", label="Spacing :")
    
    mc.separator()
    
    mc.text("Orientation to create joint chain")
    
    mc.separator()
    
    mc.button("b_xyz", label="XYZ", h=30, c="xyz()", p="c_layout")
    mc.button("b_zxy", label="ZXY", h=30, c="zxy()", p="c_layout")
    mc.button("b_yzx", label="YZX", h=30, c="yzx()", p="c_layout")
    
    mc.separator()    
    mc.textScrollList("myList", h=50, a=["Point Constrain", "Orient Constrain", "Parent Constrain"])
    
    mc.checkBox("myChBx", l="Maintain Offset")
    
    mc.button(l="Make Constrain", c="constrain()")
    
    mc.button(l="Remove Constraint(s)", c="rmvConstraint()")
       
    
    mc.showWindow("cJnt_win")

def xyz():
    
    jointName = mc.textFieldGrp("jntName", q=True, tx=True)
    jointAmount = mc.textFieldGrp("jntAmount", q=True, tx=True)
    jointSpacing = mc.textFieldGrp("jntSpacing", q=True, tx=True)
    
    mc.select(cl=True)
    
    if jointAmount == "1":
        
        jntSingle = mc.joint(n=jointName)
        
        mc.setAttr(jntSingle + ".jointOrientX", -90)
        mc.setAttr(jntSingle + ".jointOrientY", 0)
        mc.setAttr(jntSingle + ".jointOrientZ", 90)
    
    else:
        
        for x in range(int(jointAmount)):
            mc.joint(n=(jointName + "_%d") % x)
            jntPos = (x * float(jointSpacing))
            mc.move(0, jntPos, 0)
        
        mc.joint((jointName + "_0"), edit=True, oj="xyz", secondaryAxisOrient="yup", ch=True)
        selLastJnt = mc.ls(sl=True)
        mc.setAttr(selLastJnt[0] + ".jointOrientX", 0)
        mc.setAttr(selLastJnt[0] + ".jointOrientY", 0)
        mc.setAttr(selLastJnt[0] + ".jointOrientZ", 0)
        
def zxy():
    jointName = mc.textFieldGrp("jntName", q=True, tx=True)
    jointAmount = mc.textFieldGrp("jntAmount", q=True, tx=True)
    jointSpacing = mc.textFieldGrp("jntSpacing", q=True, tx=True)
    
    mc.select(cl=True)
    
    if jointAmount == "1":
        jntSingle = mc.joint(n=jointName)
        mc.setAttr(jntSingle + ".jointOrientX", -90)
        mc.setAttr(jntSingle + ".jointOrientY", 0)
        mc.setAttr(jntSingle + ".jointOrientZ", 0)
    else:
        
        for x in range(int(jointAmount)):
            mc.joint(n=(jointName + "_%d") % x)
            jntPos = (x * float(jointSpacing))
            mc.move(0, jntPos, 0)
        
        mc.joint((jointName + "_0"), edit=True, oj="zxy", secondaryAxisOrient="yup", ch=True)
        selLastJnt = mc.ls(sl=True)
        mc.setAttr(selLastJnt[0] + ".jointOrientX", 0)
        mc.setAttr(selLastJnt[0] + ".jointOrientY", 0)
        mc.setAttr(selLastJnt[0] + ".jointOrientZ", 0)
        
def yzx():
    jointName = mc.textFieldGrp("jntName", q=True, tx=True)
    jointAmount = mc.textFieldGrp("jntAmount", q=True, tx=True)
    jointSpacing = mc.textFieldGrp("jntSpacing", q=True, tx=True)
    
    mc.select(cl=True)
    
    if jointAmount == "1":
        jntSingle = mc.joint(n=jointName)
        mc.setAttr(jntSingle + ".jointOrientX", 0)
        mc.setAttr(jntSingle + ".jointOrientY", 0)
        mc.setAttr(jntSingle + ".jointOrientZ", 0)
    else:
        
        for x in range(int(jointAmount)):
            mc.joint(n=(jointName + "_%d") % x)
            jntPos = (x * float(jointSpacing))
            mc.move(0, jntPos, 0)
        
        mc.joint((jointName + "_0"), edit=True, oj="yzx", secondaryAxisOrient="yup", ch=True)
        selLastJnt = mc.ls(sl=True)
        mc.setAttr(selLastJnt[0] + ".jointOrientX", 0)
        mc.setAttr(selLastJnt[0] + ".jointOrientY", 0)
        mc.setAttr(selLastJnt[0] + ".jointOrientZ", 0)
        


    
def constrain():
    
    tsl_item = mc.textScrollList("myList", q=True, si=True)
    
    if mc.checkBox("myChBx", q=True, v=True) == 1:
        if tsl_item[0] == "Parent Constrain":
            mc.parentConstraint(mo=True)
    
    else:
        if tsl_item[0] == "Parent Constrain":
            
            mc.parentConstraint()
            
    if mc.checkBox("myChBx", q=True, v=True) == 1:
        if tsl_item[0] == "Orient Constrain":
            mc.orientConstraint(mo=True)
    else:
        if tsl_item[0] == "Orient Constrain":
            mc.orientConstraint()
            
    if mc.checkBox("myChBx", q=True, v=True) == 1:
        if tsl_item[0] == "Point Constrain":
            mc.pointConstraint(mo=True)
    else:
        if tsl_item[0] == "Point Constrain":
            mc.pointConstraint()
            
def rmvConstraint():
    
    tsl_item = mc.textScrollList("myList", q=True, si=True)
    
    if tsl_item[0] == "Parent Constrain":
        
        selCnsObj = mc.ls(sl=True)
        
        getPrtCns = mc.listRelatives(selCnsObj, type="parentConstraint")
        
        mc.delete(getPrtCns)
        
    if tsl_item[0] == "Orient Constrain":
        selCnsObj = mc.ls(sl=True)
        getOriCns = mc.listRelatives(selCnsObj, type="orientConstraint")
        mc.delete(getOriCns)
        
    if tsl_item[0] == "Point Constrain":
        selCnsObj = mc.ls(sl=True)
        getPtCns = mc.listRelatives(selCnsObj, type="pointConstraint")
        mc.delete(getPtCns)
            
            
#---------------------------------Joint Tool : Rename-------------------------------------------------------------------------            
            
def rename_joints():
 
    if mc.window("window_rename_joints", ex=True):
        mc.deleteUI("window_rename_joints", window=True)   
    window_rename_joints = mc.window( title = "Joint Hierarchy Renamer", widthHeight = ( 500, 55 ) )


    mc.columnLayout( adjustableColumn = True )
    mc.text( label = "Instructions: select top of joint hierarchy" )
    
    selected_joint = mc.ls( sl = True, type = "joint" )    
    mc.select( selected_joint, hierarchy = True )
    joint_hierarchy = mc.ls( sl = True, type = "joint" )
    joint_hierarchy.reverse()

    def joint_name( joint_prefix, idx ):
        return joint_prefix + "_" + chr( ord( "a" ) + idx ) + "01"
    

    def savename():
        joint_prefix = mc.textFieldButtonGrp( textField, text = 1, q = 1 )
        for idx, jnt in enumerate( joint_hierarchy, start = 1 ):
            new_name = joint_name( joint_prefix, len( joint_hierarchy ) - idx )
            mc.rename( jnt, new_name )
        return joint_prefix   
    textField = mc.textFieldButtonGrp( label = "New name prefix:", buttonLabel = "Rename",bc= savename )

    mc.showWindow( window_rename_joints )

#---------------------------------Joint Tool : Rename-------------------------------------------------------------------------            

import pymel.core as pm
import logging
import os
import sys

LOG = logging.getLogger(__name__)
CLEANLOG = logging.getLogger('Maya')

MAYA_EXTS = ['ma', 'mb']

def saveAsciiAndBinary(binaryFirst=True, applyInfo=False):
    if binaryFirst: saveBinary(applyInfo=applyInfo)
    saveAscii(applyInfo=applyInfo)
    if not binaryFirst: saveBinary(applyInfo=applyInfo)

def saveAscii(applyInfo=False):
    save(ext='ma', applyInfo=applyInfo)

def saveBinary(applyInfo=False):
    save(ext='mb', applyInfo=applyInfo)

def save(fileName=None, ext=None, applyInfo=False, mayaExts=MAYA_EXTS):
    saveName = fileName
    if saveName is None:
        saveName = pm.sceneName()
        if 'untitled' in saveName:
            LOG.warning('The current scene has not yet been saved.')
            return None
    if ext is not None:
        if ext not in mayaExts:
            LOG.error('The provided file type `{0}` is not valid.'.format(ext))
            return None
        saveName = forceExt(saveName, ext)
    
    if applyInfo:
        setFileInfo()
    result = pm.saveAs(saveName)
    CLEANLOG.info('Result: {0}'.format(result))


def forceExt(path, ext):
    base = os.path.splitext(path)[0]
    if '.' in ext:
        ext.replace('.', '')
    newPath = '{0}.{1}'.format(base, ext)
    return newPath


def setFileInfo():
    pm.fileInfo['lastUser'] = pm.env.user()
    
#---------------------------------Joint Tool : Create Joint on CV-------------------------------------------------------------------------            

def jntCV():    
    #Find selected components
    selCVs = mc.ls(sl=True, fl=True)
    
    #Get the size of selection
    selSize_CV = len(selCVs)
    
    #For Loop - for all CVs in selection, run the following cmds
    for cvs in range(0, selSize_CV, 1):
        #Find the position of each CV
        findCV_X = mc.getAttr(selCVs[cvs] + ".xValue")
        findCV_Y = mc.getAttr(selCVs[cvs] + ".yValue")
        findCV_Z = mc.getAttr(selCVs[cvs] + ".zValue")
        #Clear selection 
        mc.select(cl=True)#<- this prevents joints from being parented to curve
        #Create a joint for each selected CV.
        mkJnt = mc.joint()#If you're creating an object that's not a joint, query the object's Return Value from the Docs
        #Align a joint to each CV in selection
        #NOTE - If you're making an object whose command creates more that one node, make sure to access the object's transform node with [0]
        #NOTE - In this code, if you swap mc.joint() with mc.polyCube(), we would need [0] after the variable "mkJnt" in order to access the transform node of the object
        mc.setAttr(mkJnt + ".tx", findCV_X)
        mc.setAttr(mkJnt + ".ty", findCV_Y)
        mc.setAttr(mkJnt + ".tz", findCV_Z)
        
#---------------------------------Alight Object-------------------------------------------------------------------------            


def alignobj():
    prtCns = mc.parentConstraint()
    mc.delete(prtCns)
#---------------------------------Locator 2 Object-------------------------------------------------------------------------            
    
def locator2obj():
    ax = mc.getAttr(".translateX")
    ay = mc.getAttr(".translateY")
    az = mc.getAttr(".translateZ")
    
    b = mc.spaceLocator(p=(ax, ay, az))    


#---------------------------------Locator 2 Object-------------------------------------------------------------------------            
def cslave():
    
    sel = mc.ls(sl=1, type = "joint")
    
    for i in sel:
        mc.select(cl=1)
        slJnt = cmds.joint(n = "slave_" + i)
        pc = mc.parentConstraint(i, slJnt, mo = 0)
        mc.delete(pc)
        mc.makeIdentity(slJnt,apply=1)
        mc.pointConstraint(i, slJnt, mo = 0)
        mc.orientConstraint(i,slJnt, mo=0)

#---------------------------------Create Joint Chain Controller-------------------------------------------------------------------------            
        
def jntchainCtrl():        
    sel = mc.ls(sl=1)
    controller = "curve1"
    preparent = None
    
    
    for i in sel:
        mc.select(cl=1)
        if controller == None or mc.objExists(controller) == False:
            controller1 = mc.circle(nr = (1, 0,0), name = i + "_ctrl")[0]
            
        else:
            controller1 = mc.duplicate(controller,name = i+"_ctrl")[0]
            
        grp = mc.group(em =1, name = i+"_grp")
        mc.parent(controller1,grp)
        pc = cmds.parentConstraint(i,grp, mo=0)
        mc.delete(pc)
        mc.pointConstraint(controller1,i, mo=0)                            
        mc.orientConstraint(controller1,i, mo=0)
        
        if preparent != None:
            mc.parent(grp, preparent)
            
        preparent = controller1
                            
#---------------------------------Create Joint Chain Controller-------------------------------------------------------------------------            

from pymel.core import *

FLOAT_PRECISION = 4
NUM_INFLUENCES = 4

def formatJSON(output) :
    export = '{\n'
    export += '\t"animation": {\n'
    export += '\t\t"name": "' + output['animation']['name'] + '",\n'
    export += '\t\t"length": ' + str(output['animation']['length']) + ',\n'
    export += '\t\t"hierarchy": [\n'
    for bone in output['animation']['hierarchy'] :
        export += '\t\t\t{\n'
        export += '\t\t\t\t"parent": ' + str(bone['parent']) + ',\n'
        export += '\t\t\t\t"name": ' + str(bone['name']) + ',\n'
        export += '\t\t\t\t"keys": [\n'
        for key in bone['keys'] :
            export += '\t\t\t\t\t{\n'
            for prop in ['time', 'pos', 'rot', 'scl'] :
                export += '\t\t\t\t\t\t"' + prop + '"' + ': ' + str(key[prop]) + ',\n'
            export = export[:-2] + '\n\t\t\t\t\t},\n'
        export = export[:-2] + '\n'
        export += '\t\t\t\t]\n'
        export += '\t\t\t},\n'
    export = export[:-2] + '\n\t\t],\n'
    export = export[:-2] + '\n\t}\n'
    export += '}\n'
    print export
    return export

def exportMesh() :
    selection = ls(selection=1, type='transform')
    mesh = selection[0]
    skins = filter(lambda skin: mesh.getShape() in skin.getOutputGeometry(), ls(type='skinCluster'))    
    
    if len(selection) == 0 :
        print 'No mesh selected'
    elif len(skins) == 0:
        print 'No skin attached'
    else :
        location = fileDialog2(caption='Export As', fileMode=0)
        return
        
    skin = skins[0]
    
    output = {
    'animation': {
    'name': 'SkeletalAnimation',
    'length': playbackOptions(maxTime=True, query=True) - playbackOptions(minTime=True, query=True),
    'hierarchy':  [],
    },
    }
    skinJoints = skin.influenceObjects()
    root = skinJoints[0]
    while root.getParent() :
        root = root.getParent()
    
    select(root, hierarchy=True, replace=True)
    joints = ls(selection=True, transforms=True, type='joint')
    firstFrame = playbackOptions(minTime=True, query=True)
    lastFrame = playbackOptions(maxTime=True, query=True)
    
    currentTime(firstFrame)
    
    for joint in joints :
        parent = joint.getParent()
        
        keys = []
        time = 0
        for frame in range(int(firstFrame), int(lastFrame) + 1):
            currentTime(frame)
            keys.append({
            'time': time,
            'pos': [round(value, FLOAT_PRECISION) for value in joint.getTranslation()],
            'rot': [round(value, FLOAT_PRECISION) for value in joint.getRotation(quaternion=True) * joint.getOrientation()],
            'scl': [round(value, FLOAT_PRECISION) for value in joint.getScale()]
            })
            undo()
            time += 1
        print keys
        
        output['animation']['hierarchy'].append({
        'parent': joints.index(parent) if parent else -1,
        'name': '"' + joint.name() + '"',
        'keys': keys
        })
    undo()
    undo()
    export = formatJSON(output)
    
    with open(location[0], 'w') as exportFile :
        exportFile.write(export)
    print 'successfully exported as ' + location[0],
exportMesh()