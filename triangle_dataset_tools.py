import enum
import json

import PIL
from PIL import ImageDraw
from PIL import Image
import math

class TriangleClassification(enum.IntEnum):
    ACUTE = 0
    OBTUSE = 1
    RIGHT = 2

    RIGHT_SCALENE = 3
    RIGHT_ISOSCELES = 4
#class TriangleClassification

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
MARGIN = 50
COLOR_BLACK = "#00000000"
COLOR_RED = "#FF0000"
COLOR_WHITE = "#FFFFFF"
COLOR_CYAN = "#00FFFF"
COLOR_GREEN = "#00FF00"
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def utilNowYMDHMS():
    from datetime import date
    dateToday = date.today()
    y, m, d = dateToday.year, dateToday.month, dateToday.day
    strYMD = "%d-%d-%d"%(y, m, d)

    from datetime import datetime
    timeNow = datetime.now()
    hh, mm, ss = timeNow.hour, timeNow.minute, timeNow.second
    strHMS = "%d-%d-%d"%(hh, mm, ss)

    strRet = "%s_%s"%(strYMD, strHMS)

    return strRet
#def utilNowYMDHMS

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-19 - added param pStrPathWereToSave
"""
def drawTriangle(
    pImageWhereToDraw:PIL.Image,
    pListOfTriangleCoordinates:list,
    pStrFillColor = COLOR_BLACK,
    pStrOutlineColor = COLOR_RED,
    pStrColorForText = COLOR_GREEN,
    pbShowImage:bool = True,
    pbSaveToFile:bool = False,
    pStrPathWereToSave:str="",
    pb4TargetsInsteadOfOnly3:bool=True
):
    idraw2D: ImageDraw = ImageDraw.Draw(pImageWhereToDraw)  # A simple 2D drawing interface for PIL images
    idraw2D.polygon(
        pListOfTriangleCoordinates,
        fill=pStrFillColor,
        outline=pStrOutlineColor
    )

    strCoordinates = ""
    for idx, tuple2DPoint in enumerate(pListOfTriangleCoordinates):
        strPoint = "P{}={}".format(idx+1, tuple2DPoint)
        idraw2D.text(
            tuple2DPoint,
            strPoint,
            fill=pStrColorForText
        )
        strCoordinates+=str(tuple2DPoint)
    #for every coordinate

    strTriangleMultilineCanNotBeUsedForFileName = triangleToString(pListOfTriangleCoordinates)
    idraw2D.text(
        (0,0),
        strTriangleMultilineCanNotBeUsedForFileName,
        fill=pStrColorForText
    )

    strClassification = classifyTriangle(
        pTriangleAsListOfTuples=pListOfTriangleCoordinates,
        pb4TargetsInsteadOfOnly3=pb4TargetsInsteadOfOnly3
    )

    if (pbShowImage):
        pImageWhereToDraw.show()

    strNow = utilNowYMDHMS()
    strFilename = "triangle_%s_%s_%s.PNG" % (strCoordinates, strClassification, strNow)

    if(pStrPathWereToSave!=""):
        strFilename = pStrPathWereToSave+"/"+strFilename

    if (pbSaveToFile):
        pImageWhereToDraw.save(
            strFilename
        )

    return strFilename
#def drawTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def triangleToString(
    pListTriangle:list,
    pbDisplayCorrectClassification = True
):
    strCoordinates = ""
    for idx, p in enumerate(pListTriangle):
        strCoordinates+="P{}={} ".format(idx+1, p)

    dictTriangleAnglesAndLenghts = computeTriangleAnglesAndLengths(pListTriangle)
    dictAngles = dictTriangleAnglesAndLenghts["angles"]
    dictLengths = dictTriangleAnglesAndLenghts["lengths"]

    strAngles = strLengths = ""

    for keyAngle in dictAngles.keys():
        strAngles+="{}={} ".format(keyAngle, dictAngles[keyAngle])

    for keyLength in dictLengths.keys():
        strLengths += "{}={} ".format(keyLength, dictLengths[keyLength])

    strClassification = classifyTriangle(pListTriangle)
    strTriangle = "%s\n%s\n%s\n%s\n"%(strCoordinates, strAngles, strLengths, strClassification)

    return strTriangle
#def triangleToString

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23
modified to give the caller the option to force the output of an isosceles (right) triangle
"""
def randomTriangleToBeInscribedInImage(
    pbForceRightTriangle = False, #if totally random, it is very hard to get a triangle rectangle (with a 90 degrees angle)
    pImageWidthInPixels:int = IMAGE_WIDTH,
    pImageHeightInPixels:int = IMAGE_HEIGHT,
    pMarginInPixels = MARGIN,
    pbPrintTriangle:bool = True,
    pbForceRightIsosceles = False # 2022-06-23 - in the case of right triangles, if totally random, it is very hard for both the other angles to be 45, unless forced
):
    import random
    listTriangle = []
    if (not pbForceRightTriangle):
        for idx in range (3): #3 points
            px = random.randint(0+pMarginInPixels, pImageWidthInPixels-pMarginInPixels)
            py = random.randint(0+pMarginInPixels, pImageHeightInPixels-pMarginInPixels)
            tupleXY = (px, py)
            listTriangle.append(tupleXY)
        #for
    else:
        # forced the output of a right triangle
        if (not pbForceRightIsosceles):
            px1 = random.randint(0 + pMarginInPixels, pImageWidthInPixels - pMarginInPixels)
            py1 = random.randint(0 + pMarginInPixels, pImageHeightInPixels - pMarginInPixels)
            tupleXY = (px1, py1)
            listTriangle.append(tupleXY)

            px2 = random.randint(0 + pMarginInPixels, pImageWidthInPixels - pMarginInPixels)
            tupleXY = (px2, py1)
            listTriangle.append(tupleXY)

            iSizeOfSegmentX1ToX2 = math.fabs(px2 - px1)

            py2 = random.randint(0 + pMarginInPixels, pImageHeightInPixels - pMarginInPixels)
            iSizeOfSegmentY1ToY2 = math.fabs(py2-py1)

            bIsoscelesByChance = iSizeOfSegmentX1ToX2==iSizeOfSegmentY1ToY2 # highly improbable
            if (not bIsoscelesByChance):
                bScalene = True
            else:
                bScalene = False

            tupleXY = (px1, py2)
            listTriangle.append(tupleXY)
        else:
            # 2022-06-23
            # forcing a right AND isosceles triangle
            # https://www.cuemath.com/geometry/right-angled-triangle/

            # randomly pick a 1st tuple (px1, py1)
            px1 = random.randint(0 + pMarginInPixels, pImageWidthInPixels - pMarginInPixels)
            py1 = random.randint(0 + pMarginInPixels, pImageHeightInPixels - pMarginInPixels)
            tupleXY = (px1, py1)
            listTriangle.append(tupleXY)

            # randomly pick a x2, indirectly a 2nd tuple (px2, py1)
            # by KEEPING y at y1 it is ASSURED that the 1st and the 2nd tuples are aligned on y
            # if, next, the 3rd and final tuple is assured to be aligned on x, by only varying y, then one angle is surely 90
            px2 = random.randint(0 + pMarginInPixels, pImageWidthInPixels - pMarginInPixels)
            tupleXY = (px2, py1)
            listTriangle.append(tupleXY)

            # do not vary the x of the 3rd tuple, to assure a 90 degrees angle in the triangle
            # make sure the new y is such that length of the side that connects to the 3rd point is the same of the previous side, for having an isosceles triangle
            # so, py2 can NOT be random
            iRequiredYSizeForHavingAnIsoscelesTriangleComputedFromTheRandomSizeOnX = math.fabs(px2-px1)
            py2 = 0 + pMarginInPixels + iRequiredYSizeForHavingAnIsoscelesTriangleComputedFromTheRandomSizeOnX
            tupleXY = (px1, py2)
            listTriangle.append(tupleXY)
    #else

    if (pbPrintTriangle):
        strTriangle = triangleToString(listTriangle)
        print(strTriangle)
    #if

    return listTriangle
#def randomTriangleToBeInscribedInImage

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-19 - added param pStrPathWereToSave
"""
def drawSingleTriangleToNewImage(
    pListTriangle:list,

    #about the image
    pImageWidth:int = IMAGE_WIDTH,
    pImageHeight:int = IMAGE_HEIGHT,
    pStrImageBackgroundColor = COLOR_WHITE,

    #about the triangle
    pStrTriangleFillColor = COLOR_BLACK,
    pStrTriangleOutlineColor = COLOR_RED,
    pStrTriangleColorForTextForCoordinates = COLOR_GREEN,
    pbShowTriangleImage:bool = True,
    pbSaveTriangleToFile:bool = False,
    pStrPathWereToSave:str="",
    pb4TargetsInsteadOfOnly3:bool=True # 2022-06-23

):
    img:Image = Image.new(
        mode='RGB',
        size=(pImageWidth, pImageHeight),
        color=pStrImageBackgroundColor
    )

    strFileNameForTheTriangleIfSaved = \
        drawTriangle(
            img,
            pListTriangle,
            pStrTriangleFillColor,
            pStrTriangleOutlineColor,
            pStrTriangleColorForTextForCoordinates,
            pbShowTriangleImage,
            pbSaveTriangleToFile,
            pStrPathWereToSave=pStrPathWereToSave,
            pb4TargetsInsteadOfOnly3=pb4TargetsInsteadOfOnly3
        )

    return strFileNameForTheTriangleIfSaved
#def drawSingleTriangleToNewImage

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def generateXRandomTrianglesToBeInscribedInImage(
    pX=24,
    pImageWidthInPixels:int = IMAGE_WIDTH,
    pImageHeightInPixels:int = IMAGE_HEIGHT,
    pMarginInPixels = MARGIN,
    pbPrintTriangle:bool = True,
    pbGenerateFilesForImages = True,
    pStrPathWereToSave:str=""
):
    listTriangles = []
    listCorrectClassificationForSupervisedLearning = []
    listAngles = []
    listLengths = []

    for nTriangle in range(pX):
        t = randomTriangleToBeInscribedInImage(
            nTriangle%3==0, #a square triangle every 3 triangles
            pImageWidthInPixels,
            pImageHeightInPixels,
            pMarginInPixels,
            pbPrintTriangle
        )
        dictAnglesAndLengths = computeTriangleAnglesAndLengths(t)
        listAngles.append(dictAnglesAndLengths["angles"])
        listLengths.append(dictAnglesAndLengths["lengths"])

        classification = classifyTriangle(t)

        listTriangles.append(t)
        listCorrectClassificationForSupervisedLearning.append(classification)
    #for

    listFileNamesForTriangles = []
    for t in listTriangles:
        strFilenameForTheTriangleIfSaved = \
            drawSingleTriangleToNewImage(
                t,
                pbShowTriangleImage=False,
                pbSaveTriangleToFile=pbGenerateFilesForImages,
                pStrPathWereToSave=pStrPathWereToSave
            )

        listFileNamesForTriangles.append(strFilenameForTheTriangleIfSaved)
    #for2

    dictRet = {}
    dictRet["triangles"] = listTriangles
    dictRet["angles"] = listAngles
    dictRet["lengths"] = listLengths
    dictRet["targets"] = listCorrectClassificationForSupervisedLearning
    dictRet["files"] = listFileNamesForTriangles

    #return listFileNamesForTriangles
    return dictRet
#def generateXRandomTrianglesToBeInscribedInImage

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-20 - added the pStrPathWereToSave param
"""
def generateXRandomTrianglesToBeInscribedInImageAssuringEqualRepresentationOfAllTargets(
    pSamplesPerTarget=24,
    pImageWidthInPixels:int = IMAGE_WIDTH,
    pImageHeightInPixels:int = IMAGE_HEIGHT,
    pMarginInPixels = MARGIN,
    pbPrintTriangle:bool = True,
    pbGenerateFilesForImages = True,
    pStrPathWereToSave:str=""
):
    iSquare = iAcute = iObtuse = 0
    listTriangles = []
    listCorrectClassificationForSupervisedLearning = []
    listAngles = []
    listLengths = []

    while(iAcute<pSamplesPerTarget):
        t = randomTriangleToBeInscribedInImage(
            False, #do NOT force square triangle
            pImageWidthInPixels,
            pImageHeightInPixels,
            pMarginInPixels,
            pbPrintTriangle
        )
        dictAnglesAndLengths = computeTriangleAnglesAndLengths(t)
        classification = classifyTriangle(t)
        bAcute = classification==TriangleClassification.ACUTE
        if (bAcute):
            listTriangles.append(t)
            listCorrectClassificationForSupervisedLearning.append(classification)
            listAngles.append(dictAnglesAndLengths["angles"])
            listLengths.append(dictAnglesAndLengths["lengths"])
            iAcute += 1
        #if
    #while not enough acute

    while (iObtuse<pSamplesPerTarget):
        t = randomTriangleToBeInscribedInImage(
            False,  # do NOT force square triangle
            pImageWidthInPixels,
            pImageHeightInPixels,
            pMarginInPixels,
            pbPrintTriangle
        )
        dictAnglesAndLengths = computeTriangleAnglesAndLengths(t)
        classification = classifyTriangle(t)
        bObtuse = classification == TriangleClassification.OBTUSE
        if (bObtuse):
            listTriangles.append(t)
            listCorrectClassificationForSupervisedLearning.append(classification)
            listAngles.append(dictAnglesAndLengths["angles"])
            listLengths.append(dictAnglesAndLengths["lengths"])
            iObtuse += 1
        # if
    # while not enough obtuse

    while(iSquare<pSamplesPerTarget):
        t = randomTriangleToBeInscribedInImage(
            True,  # do FORCE square triangle
            pImageWidthInPixels,
            pImageHeightInPixels,
            pMarginInPixels,
            pbPrintTriangle
        )
        dictAnglesAndLengths = computeTriangleAnglesAndLengths(t)
        classification = classifyTriangle(t)
        bRight = classification == TriangleClassification.RIGHT
        if (bRight):
            listTriangles.append(t)
            listCorrectClassificationForSupervisedLearning.append(classification)
            listAngles.append(dictAnglesAndLengths["angles"])
            listLengths.append(dictAnglesAndLengths["lengths"])
            iSquare += 1
        # if
    #while not enough square

    listFileNamesForTriangles = []
    for t in listTriangles:
        strFilenameForTheTriangleIfSaved = \
            drawSingleTriangleToNewImage(
                t,
                pbShowTriangleImage=False,
                pbSaveTriangleToFile=pbGenerateFilesForImages,
                pStrPathWereToSave=pStrPathWereToSave
            )

        listFileNamesForTriangles.append(strFilenameForTheTriangleIfSaved)
    #for

    dictRet = {}
    dictRet["triangles"] = listTriangles
    dictRet["angles"] = listAngles
    dictRet["lengths"] = listLengths
    dictRet["targets"] = listCorrectClassificationForSupervisedLearning
    dictRet["files"] = listFileNamesForTriangles

    #return listFileNamesForTriangles
    return dictRet
#def generateXRandomTrianglesToBeInscribedInImageAssuringEqualRepresentationOfAllTargets

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23 - now supporting 4 targets
"""
def generateXRandomTrianglesToBeInscribedInImageAssuringEqualRepresentationOfAll4Targets(
    pSamplesPerTarget=24,
    pImageWidthInPixels:int = IMAGE_WIDTH,
    pImageHeightInPixels:int = IMAGE_HEIGHT,
    pMarginInPixels = MARGIN,
    pbPrintTriangle:bool = True,
    pbGenerateFilesForImages = True,
    pStrPathWereToSave:str="",
    pb4Targets = True # new on 2022-06-23
):
    iRight = iRightScalene = iRightIsosceles = iAcute = iObtuse = 0
    listTriangles = []
    listCorrectClassificationForSupervisedLearning = []
    listAngles = []
    listLengths = []

    while(iAcute<pSamplesPerTarget):
        t = generateRandomAcuteTriangle()
        dictAnglesAndLengths = computeTriangleAnglesAndLengths(t)
        listTriangles.append(t)
        listCorrectClassificationForSupervisedLearning.append(TriangleClassification.ACUTE)
        listAngles.append(dictAnglesAndLengths["angles"])
        listLengths.append(dictAnglesAndLengths["lengths"])
        iAcute += 1
    #while not enough acute triangles

    while (iObtuse < pSamplesPerTarget):
        t = generateRandomObtuseTriangle()
        dictAnglesAndLengths = computeTriangleAnglesAndLengths(t)
        listTriangles.append(t)
        listCorrectClassificationForSupervisedLearning.append(TriangleClassification.OBTUSE)
        listAngles.append(dictAnglesAndLengths["angles"])
        listLengths.append(dictAnglesAndLengths["lengths"])
        iObtuse += 1
    # while not enough obtuse triangles

    if (not pb4Targets):
        # only 3-targets (acute, obtuse, right)
        while (iRight < pSamplesPerTarget):
            t = generateRandomRightTriangle()
            dictAnglesAndLengths = computeTriangleAnglesAndLengths(t)
            listTriangles.append(t)
            listCorrectClassificationForSupervisedLearning.append(TriangleClassification.RIGHT)
            listAngles.append(dictAnglesAndLengths["angles"])
            listLengths.append(dictAnglesAndLengths["lengths"])
            iRight += 1
        # while not enough right triangles
    else:
        # 4-targets (acute, obtuse, right-scalene, right-isosceles)

        # produce scalene
        while (iRightScalene < pSamplesPerTarget):
            t = generateRandomRightScaleneTriangle()
            dictAnglesAndLengths = computeTriangleAnglesAndLengths(t)
            listTriangles.append(t)
            listCorrectClassificationForSupervisedLearning.append(TriangleClassification.RIGHT_SCALENE)
            listAngles.append(dictAnglesAndLengths["angles"])
            listLengths.append(dictAnglesAndLengths["lengths"])
            iRightScalene += 1
        # while not enough right-scalene triangles

        # produce isosceles
        while (iRightIsosceles < pSamplesPerTarget):
            t = generateRandomRightIsoscelesTriangle()
            dictAnglesAndLengths = computeTriangleAnglesAndLengths(t)
            listTriangles.append(t)
            listCorrectClassificationForSupervisedLearning.append(TriangleClassification.RIGHT_ISOSCELES)
            listAngles.append(dictAnglesAndLengths["angles"])
            listLengths.append(dictAnglesAndLengths["lengths"])
            iRightIsosceles += 1
        # while not enough right-isosceles triangles
    #if-else

    listFileNamesForTriangles = []
    for t in listTriangles:
        strFilenameForTheTriangleIfSaved = \
            drawSingleTriangleToNewImage(
                t,
                pbShowTriangleImage=False,
                pbSaveTriangleToFile=pbGenerateFilesForImages,
                pStrPathWereToSave=pStrPathWereToSave
            )

        listFileNamesForTriangles.append(strFilenameForTheTriangleIfSaved)
    #for

    dictRet = {}
    dictRet["triangles"] = listTriangles
    dictRet["angles"] = listAngles
    dictRet["lengths"] = listLengths
    dictRet["targets"] = listCorrectClassificationForSupervisedLearning
    dictRet["files"] = listFileNamesForTriangles

    #return listFileNamesForTriangles
    return dictRet
#def generateXRandomTrianglesToBeInscribedInImageAssuringEqualRepresentationOfAll4Targets

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.

# returns square of distance between two points
def cartesianDistance(
    pTuplePoint1,
    pTuplePoint2
):
    xDiff = pTuplePoint1[0] - pTuplePoint2[0]
    yDiff = pTuplePoint1[1] - pTuplePoint2[1]
    distance = xDiff**2 + yDiff**2
    return distance
#def cartesianDistance

# _.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23 - created
in the case of right triangles, this function transparently supports BOTH vague 3-targets ("right") and exact 4-targets classification systems ("right-scalene", "right-isosceles")
"""
def generateRandomTriangleOfRequestedType(
    pTypeOfTriangleWanted:TriangleClassification,
    pbPrintTriangle:bool = True
):
    bSuccess = False

    triangleAsList = None
    while (not bSuccess):
        # do a totally random triangle
        listOfTuplesRepresentingSomeRandomTriangle = randomTriangleToBeInscribedInImage(
            pbPrintTriangle=pbPrintTriangle
        )

        # check the cases for right triangles and, if so was requested, REPLACE the previously generated triangle with a surely right one
        if (pTypeOfTriangleWanted==TriangleClassification.RIGHT):
            listOfTuplesRepresentingSomeRandomTriangle = randomTriangleToBeInscribedInImage(
                pbForceRightTriangle=True,
                pbPrintTriangle=pbPrintTriangle
            )

        if (pTypeOfTriangleWanted==TriangleClassification.RIGHT_SCALENE):
            listOfTuplesRepresentingSomeRandomTriangle = randomTriangleToBeInscribedInImage(
                pbForceRightTriangle=True,
                pbForceRightIsosceles=False,
                pbPrintTriangle=pbPrintTriangle
            )

        if (pTypeOfTriangleWanted==TriangleClassification.RIGHT_ISOSCELES):
            listOfTuplesRepresentingSomeRandomTriangle = randomTriangleToBeInscribedInImage(
                pbForceRightTriangle=True,
                pbForceRightIsosceles=True,
                pbPrintTriangle=pbPrintTriangle
            )

        # check the type of the generated triangle
        c = classificationForTheTriangle = classifyTriangle(
            pTriangleAsListOfTuples=listOfTuplesRepresentingSomeRandomTriangle,
            pb4TargetsInsteadOfOnly3=True
        )

        bExactMatch = classificationForTheTriangle == pTypeOfTriangleWanted

        bGeneratedTriangleIsRight = c==TriangleClassification.RIGHT_SCALENE or c==TriangleClassification.RIGHT_ISOSCELES or c==TriangleClassification.RIGHT

        bVagueRightMatch = bGeneratedTriangleIsRight and (pTypeOfTriangleWanted == TriangleClassification.RIGHT)

        # do we have a classification match?
        # obtuse and acute triangle will probably required 1+ attempts until a situation of bExactMatch
        # right_scalene and right_isosceles will require exactly 1 call, because they can be outputed on demand
        # right_scalene and right_isosceles will match because of bExactMatch
        # vague "right" tirangles will match because of bVagueRightMatch and will also require a single call
        bClassificationMatch = bExactMatch or bVagueRightMatch

        if (bClassificationMatch):
            bSuccess = True
            triangleAsList = listOfTuplesRepresentingSomeRandomTriangle
        # if

        # this while will only repeat itself for obtuse and acute triangles, because they are totally random
        # the right triangles are "fabricated", no trully random
    # while

    return triangleAsList
# def generateRandomTriangleOfRequestedType

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23 - created
"""
def generateRandomAcuteTriangle(
    pbPrintTriangle:bool=True
):
   return generateRandomTriangleOfRequestedType(
       pTypeOfTriangleWanted=TriangleClassification.ACUTE,
       pbPrintTriangle=pbPrintTriangle
   )
# def generateRandomAcuteTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23 - created
"""
def generateRandomObtuseTriangle(
    pbPrintTriangle:bool=True
):
   return generateRandomTriangleOfRequestedType(
       pTypeOfTriangleWanted=TriangleClassification.OBTUSE,
       pbPrintTriangle=pbPrintTriangle
   )
# def generateRandomObtuseTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23 - created
"""
def generateRandomRightTriangle(
    pbPrintTriangle:bool=True
):
   return generateRandomTriangleOfRequestedType(
       pTypeOfTriangleWanted=TriangleClassification.RIGHT,
       pbPrintTriangle=pbPrintTriangle
   )
# def generateRandomRightTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23 - created
"""
def generateRandomRightScaleneTriangle(
    pbPrintTriangle:bool=True
):
   return generateRandomTriangleOfRequestedType(
       pTypeOfTriangleWanted=TriangleClassification.RIGHT_SCALENE,
       pbPrintTriangle=pbPrintTriangle
   )
# def generateRandomRightScaleneTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23 - created
"""
def generateRandomRightIsoscelesTriangle(
    pbPrintTriangle:bool=True
):
   return generateRandomTriangleOfRequestedType(
       pTypeOfTriangleWanted=TriangleClassification.RIGHT_ISOSCELES,
       pbPrintTriangle=pbPrintTriangle
   )
# def generateRandomRightIsoscelesTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23 - added an optional param to force triangle classification in 4 target classes (obtuse, acute, right-isosceles, right-scalene)
instead of only in 3 target classes (obtuse, acute, right)
"""
def classifyTriangle (
    pTriangleAsListOfTuples:list,
    pb4TargetsInsteadOfOnly3:bool = True
):
    dictAnglesAndLengths = computeTriangleAnglesAndLengths(pTriangleAsListOfTuples)
    dictAngles = dictAnglesAndLengths["angles"]
    #dictLengths = dictAnglesAndLengths["lengths"]

    bThereIsOne90 = False
    for angle in dictAngles.values():
        if angle==90.0:
            bThereIsOne90=True
            break
        # if
    # for

    if bThereIsOne90:
        if(pb4TargetsInsteadOfOnly3):
            bThereAreTwo45 = False
            iCount45 = 0

            for angle in dictAngles.values():
                if (angle == 45.0):
                    iCount45 += 1
                # if
            # for
            if (iCount45 == 2):
                bThereAreTwo45 = True
            # if

            if(bThereAreTwo45):
                return TriangleClassification.RIGHT_ISOSCELES
            else:
                return TriangleClassification.RIGHT_SCALENE
            # if
        #if
        else:
            return TriangleClassification.RIGHT
    # if
    else:
        #not "right" triangle
        biggestAngle = None
        for angle in dictAngles.values():
            if (biggestAngle==None):
                biggestAngle=angle
            else:
                if (angle>biggestAngle):
                    biggestAngle=angle
                #if
            #else
        #for

        #now have the biggest angle
        if (biggestAngle<90):
            return TriangleClassification.ACUTE
        else:
            return TriangleClassification.OBTUSE
#def classifyTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def computeTriangleAnglesAndLengths(
    pListTriangle:list,
    pbRoundToNDecimalDigits = 2,
    pDivisionByZeroFixer = 0.0001
):
    P1 = pListTriangle[0]
    P2 = pListTriangle[1]
    P3 = pListTriangle[2]

    #distances
    dP2toP3 = cartesianDistance(P2, P3)
    dP1toP3 = cartesianDistance(P1, P3)
    dP1toP2 = cartesianDistance(P1, P2)

    #lengths
    lengthSideP2toP3 = math.sqrt(dP2toP3)
    lengthSideP1toP3 = math.sqrt(dP1toP3)
    lengthSideP1toP2 = math.sqrt(dP1toP2)

    #cosine law
    denominator = (2 * lengthSideP1toP3 * lengthSideP1toP2)
    if (denominator==0):
        denominator+=pDivisionByZeroFixer
    alphaAngleBetweenSidesP1toP3andP1toP2 = math.acos((dP1toP3 + dP1toP2 - dP2toP3) / denominator)

    denominator = (2 * lengthSideP2toP3 * lengthSideP1toP2)
    if (denominator == 0):
        denominator += pDivisionByZeroFixer
    gammaAngleBetweenSidesP2toP1andP2toP3 = math.acos((dP2toP3 + dP1toP2 - dP1toP3) / denominator)

    denominator = (2 * lengthSideP2toP3 * lengthSideP1toP3)
    if (denominator == 0):
        denominator += pDivisionByZeroFixer
    betaAngleBetweenSidesP1toP3andP3toP2 = math.acos((dP2toP3 + dP1toP3 - dP1toP2) / denominator)

    #converting to degrees
    a1 = alphaAngleBetweenSidesP1toP2andP1toP3 = alphaAngleBetweenSidesP1toP3andP1toP2 * 180 / math.pi
    a2 = betaAngleBetweenSidesP3toP1andP3toP2 = betaAngleBetweenSidesP1toP3andP3toP2 * 180 / math.pi
    a3 = gammaAngleBetweenSidesP2toP3andP2toP1 = gammaAngleBetweenSidesP2toP1andP2toP3 * 180 / math.pi

    dictAngles = {}
    dictAngles["P1P2_P1P3"] = a1
    dictAngles["P3P1_P3P2"] = a2
    dictAngles["P2P3_P2P1"] = a3

    dictLenghts = {}
    dictLenghts["P1P2"] = lengthSideP1toP2
    dictLenghts["P1P3"] = lengthSideP1toP3
    dictLenghts["P2P3"] = lengthSideP2toP3

    if (pbRoundToNDecimalDigits):
        for k in dictAngles.keys():
            dictAngles[k]=round(dictAngles[k], pbRoundToNDecimalDigits)

        for k in dictLenghts.keys():
            dictLenghts[k] = round(dictLenghts[k], pbRoundToNDecimalDigits)

    dictRet = {}
    dictRet["angles"] = dictAngles
    dictRet["lengths"] = dictLenghts

    #return (a1, a2, a3)
    return dictRet
#def computeTriangleAnglesAndLengths

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
DEFAULT_TOTAL_NUMBER_OF_SAMPLES = 1000 #not in use
DEFAULT_NUMBER_OF_SAMPLES_OF_EACH_TARGET = 100
def produceDatasetWithCorrectClassificationsForSupervisedLearningSaveAsJSON(
    pNumberOfSamplesPerClass:int = DEFAULT_NUMBER_OF_SAMPLES_OF_EACH_TARGET,
    pbGenerateFilesForImages = False
):
    #dictTrianglesTargetsFiles = generateXRandomTrianglesToBeInscribedInImage(pNumberOfSamples) #total number, NOT per targetg
    dictTrianglesTargetsFiles = generateXRandomTrianglesToBeInscribedInImageAssuringEqualRepresentationOfAll4Targets(
        pSamplesPerTarget = pNumberOfSamplesPerClass,
        pbGenerateFilesForImages = pbGenerateFilesForImages,
        pb4Targets=True #2022-06-23
    )

    strYMDHMS = utilNowYMDHMS()
    strJSONFileName = "triangles_dataset_%d_samples_per_target_%s.JSON"%(pNumberOfSamplesPerClass, strYMDHMS)

    strJSON = json.dumps(dictTrianglesTargetsFiles)
    fw = open(strJSONFileName, 'wt')
    fw.write(strJSON)
    fw.close()

    return strJSONFileName
#def produceDatasetWithCorrectClassificationsForSupervisedLearningSaveAsJSON

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def auxConvertDictAsTrioOfAnglesToListOfAngles (pDictOfAngles):
    listCurrentTrio = []
    for strKey in pDictOfAngles.keys():
        currentAngleValue = pDictOfAngles[strKey]
        listCurrentTrio.append(currentAngleValue)
    # for every angle
    return listCurrentTrio
#def auxConvertDictAsTrioOfAnglesToListOfAngles

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def trianglesDatasetLoaderFromFile(
    pStrFilePath:str,
    pbVerbose:bool=True
):
    fr = open(pStrFilePath, "rt")
    dictDatasetFromJSON = json.load(fr)
    fr.close()

    dictKeys = dictDatasetFromJSON.keys()
    strFormat = "Keys in loaded dataset:\n" + str(dictKeys)
    if(pbVerbose):
        print(strFormat)

    iTotalSamples = len(dictDatasetFromJSON["angles"])
    if(pbVerbose):
        print("The dataset containts a total of %d samples" % (iTotalSamples))

    # other then 0 index will ALSO work - all members of the dataset have the same keys
    listFeatureNames = dictDatasetFromJSON["angles"][0].keys()
    strFormat = "Feature names:\n" + str(listFeatureNames)
    if(pbVerbose):
        print(strFormat)

    # [{'P1P2_P1P3': 75.32, 'P3P1_P3P2': 50.92, 'P2P3_P2P1': 53.76}, ... ]
    datasetAsListOfDictsOfAngles = dictDatasetFromJSON['angles']
    listOfListsEachATrioOfAngles = []
    for dictTrio in datasetAsListOfDictsOfAngles:
        listCurrentTrio = auxConvertDictAsTrioOfAnglesToListOfAngles(dictTrio)
        listOfListsEachATrioOfAngles.append(listCurrentTrio)
    # for every sample

    if(pbVerbose):
        print(listOfListsEachATrioOfAngles)

    listOfTargetsForEachTrioOfAngles = dictDatasetFromJSON["targets"]
    if(pbVerbose):
        print(listOfTargetsForEachTrioOfAngles)

    return dictDatasetFromJSON, listOfListsEachATrioOfAngles, listOfTargetsForEachTrioOfAngles, listFeatureNames
# def trianglesDatasetLoaderFromFile

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
#dictTrianglesTargetsFiles = generateXRandomTrianglesToBeInscribedInImage()

#strDatasetFilename = produceDatasetWithCorrectClassificationsForSupervisedLearningSaveAsJSON(DEFAULT_NUMBER_OF_SAMPLES_OF_EACH_TARGET)
#print ("DONE. Check ", strDatasetFilename)