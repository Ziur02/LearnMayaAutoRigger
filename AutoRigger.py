import maya.cmds as cmds

editMode = True

cmds.window("Auto Rigger")

cmds.rowColumnLayout(nc = 2)

cmds.button(l = "Create Locators", w = 200, c = "createLocators()")
cmds.button(l = "Delete Locators", w = 200, c = "deleteLocators()")

cmds.text("Spine Count", l = "Spine Count")
spineCountField = cmds.intField(minValue = 1, maxValue = 10, value = 4)
spineCount = cmds.intField(spineCountField, query=True, value=True)

cmds.button(l = "Edit Mode", w = 200, c = "lockAll(editMode)")

cmds.showWindow()

################################################# ACTUAL CODE #################################################

def createLocators():
    print("create locators")
    if cmds.objExists("Loc_Master"):
        print("Loc_Master already exists")
    else:
        cmds.group(em = True, name = "Loc_Master")
    
    root = cmds.spaceLocator(n = "Loc_ROOT")
    cmds.scale(0.1, 0.1, 0.1, root)
    cmds.move(0, 1, 0, root)
    cmds.parent(root, "Loc_Master")
    
    createSpine()
    
def createSpine():
    print("create spine")
    for i in range(0, spineCount):
        spine = cmds.spaceLocator(n = "Loc_SPINE_" + str(i))
        cmds.scale(0.1, 0.1, 0.1, spine)
        if i == 0:
            cmds.parent(spine, "Loc_ROOT")
        else:
            cmds.parent(spine, "Loc_SPINE_" + str(i - 1))
        cmds.move(0, 1.25 + (0.25 * i), 0, spine)

    createArms(1)
    createArms(-1)

def createArms(side):
    
    global editMode
    
    print("create arm")
    if side == 1: # left arm
        if cmds.objExists("L_Arm_GRP"):
            print("do nothing")
        else:
            L_arm = cmds.group(em = True, name = "L_Arm_GRP")
            cmds.parent(L_arm, "Loc_SPINE_" + str(spineCount - 1))
            
            # upper arm
            upperArm = cmds.spaceLocator(n = "Loc_L_UpperArm")
            cmds.scale(0.1, 0.1, 0.1, upperArm)
            cmds.parent(upperArm, L_arm)

            
            # elbow
            elbow = cmds.spaceLocator(n = "Loc_L_Elbow")
            cmds.scale(0.1, 0.1, 0.1, elbow)
            cmds.parent(elbow, upperArm)
            
            # wrist
            wrist = cmds.spaceLocator(n = "Loc_L_wrist")
            cmds.scale(0.1, 0.1, 0.1, wrist)
            cmds.parent(wrist, elbow)
            
            # move arm
            cmds.move(0.35 * side, 1 + (0.25 * spineCount), 0, L_arm)
            # move elbow
            cmds.move(0.6 * side, 1.4, -0.2, elbow)
            # move wrist
            cmds.move(0.8 * side, 1, 0, wrist)
            
    else: # right arm
        if cmds.objExists("R_Arm_GRP"):
            print("do nothing")
        else:
            R_arm = cmds.group(em = True, name = "R_Arm_GRP")
            cmds.parent(R_arm, "Loc_SPINE_" + str(spineCount - 1))
            
            # upper arm
            upperArm = cmds.spaceLocator(n = "Loc_R_UpperArm")
            cmds.scale(0.1, 0.1, 0.1, upperArm)
            cmds.parent(upperArm, R_arm)
            
            # elbow
            elbow = cmds.spaceLocator(n = "Loc_R_Elbow")
            cmds.scale(0.1, 0.1, 0.1, elbow)
            cmds.parent(elbow, upperArm)
            
            # wrist
            wrist = cmds.spaceLocator(n = "Loc_R_wrist")
            cmds.scale(0.1, 0.1, 0.1, wrist)
            cmds.parent(wrist, elbow)
            
            # move arm
            cmds.move(0.35 * side, 1 + (0.25 * spineCount), 0, R_arm)
            # move elbow
            cmds.move(0.6 * side, 1.4, -0.2, elbow)
            # move wrist
            cmds.move(0.8 * side, 1, 0, wrist)
            
            lockAll(1)
            
def lockAll(lock):    
    global editMode
    
    axis = ['x', 'y', 'z']
    attr = ['t', 'r', 's']
    
    nodes = cmds.listRelatives("Loc_*", allParents = True)
    
    for axe in axis:
        for att in attr:
            for node in nodes:
                cmds.setAttr(node + '.' + att + axe, lock = lock)
                
    if editMode == False:
        editMode = True
    else:
        editMode = False
                        
def deleteLocators():
    print("delete test")
    nodes = cmds.ls("Loc_*")
    cmds.delete(nodes)