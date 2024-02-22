import sys
sys.path.extend(['F:\\coding.jb\\py\\AM', 'F:/coding.jb/py/AM'])

from flask import Flask, render_template, request, make_response, send_file
from amutil.amutil_tools import AmUtil
from ai.triangles2.triangle_dataset_tools import \
    randomTriangleToBeInscribedInImage, drawSingleTriangleToNewImage, \
    generateXRandomTrianglesToBeInscribedInImageAssuringEqualRepresentationOfAll4Targets, \
    TriangleClassification, \
    generateRandomTriangleOfRequestedType, \
    generateRandomAcuteTriangle, generateRandomObtuseTriangle, generateRandomRightTriangle,\
    generateRandomRightIsoscelesTriangle, generateRandomRightScaleneTriangle

from PIL import Image
import json

app = Flask(__name__)

NAME_OF_INPUT_WITH_TYPE_OF_TRIANGLE_SINGLE = "nameSelectTriangleType"
NAME_OF_INPUT_WITH_TYPE_OF_TRIANGLE_PLURAL = "nameSelectTrianglesType"
VALUE_OPTION_ACUTE = "acute"
VALUE_OPTION_OBTUSE = "obtuse"
VALUE_OPTION_RIGHT = "right"
VALUE_OPTION_RIGHT_SCALENE = "right-scalene"
VALUE_OPTION_RIGHT_ISOSCELES = "right-isosceles"

NAME_OF_INPUT_WITH_HOW_MANY_TRIANGLES = "nameNumberHowManyTriangles"
NAME_OF_INPUT_WITH_HOW_MANY_SAMPLES_PER_CLASS_IN_DATASET = "nameNumberHowManySamplesPerClass"

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23 - created
"""
def auxStringToTriangleClassificationDataType(pStr):
    if(pStr==VALUE_OPTION_ACUTE):
        return TriangleClassification.ACUTE

    if(pStr==VALUE_OPTION_OBTUSE):
        return TriangleClassification.OBTUSE

    if(pStr==VALUE_OPTION_RIGHT):
        return TriangleClassification.RIGHT

    if(pStr==VALUE_OPTION_RIGHT_ISOSCELES):
        return TriangleClassification.RIGHT_ISOSCELES

    if(pStr==VALUE_OPTION_RIGHT_SCALENE):
        return TriangleClassification.RIGHT_SCALENE

    return False
# def auxStringToTriangleClassificationDataType

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-19 - created
"""
def auxRandomSingleWebTriangle(
    pStrStorageSubFolderInStatic:str= ""
):
    strDestinationPath = "static/" + pStrStorageSubFolderInStatic + "/"
    createDirResult = AmUtil.createDir(strDestinationPath)

    t = randomTriangleToBeInscribedInImage()

    fileWithTriangle = drawSingleTriangleToNewImage(
        pListTriangle=t,
        pbShowTriangleImage=False,  # if True, the O.S.'s default viewer will be launched
        pbSaveTriangleToFile=True,
        pStrPathWereToSave="static/" + pStrStorageSubFolderInStatic
    )

    return t, fileWithTriangle
# def auxRandomSingleWebTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-23 - created
"""
def auxRandomSingleWebTriangleOfType(
    pTypeOfTriangle:TriangleClassification,
    pStrStorageSubFolderInStatic:str= "",
    pbPrintTriangle:bool=False
):
    strDestinationPath = "static/" + pStrStorageSubFolderInStatic + "/"
    createDirResult = AmUtil.createDir(strDestinationPath)

    t = generateRandomTriangleOfRequestedType(
        pTypeOfTriangleWanted=pTypeOfTriangle,
        pbPrintTriangle=pbPrintTriangle # prints will NOT show on a Web page
    )

    fileWithTriangle = drawSingleTriangleToNewImage(
        pListTriangle=t,
        pbShowTriangleImage=False,  # if True, the O.S.'s default viewer will be launched
        pbSaveTriangleToFile=True,
        pStrPathWereToSave="static/" + pStrStorageSubFolderInStatic
    )

    return t, fileWithTriangle
# def auxRandomSingleWebTriangleOfType

# _.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-20 - created
2022-06-23 - edited to support a new param stating the exact type of triangle wanted
2022-06-23 - renamed to auxRandomPluralWebTrianglesOfType
"""
def auxRandomPluralWebTrianglesOfType(
    pTypeOfTriangle:TriangleClassification,
    piHowManyTriangles:int,
    pStrStorageSubFolderInStatic: str = "",
    pbPrintTriangle:bool=False
):
    strDestinationPath = "static/" + pStrStorageSubFolderInStatic + "/"
    createDirResult = AmUtil.createDir(strDestinationPath)

    dictResult = dict()

    for i0based in range(piHowManyTriangles):
        i1based = i0based+1

        strMsg = f"Generating triangle #{i1based} of {piHowManyTriangles}\n"
        print(strMsg)

        t = generateRandomTriangleOfRequestedType(
            pTypeOfTriangleWanted=pTypeOfTriangle,
            pbPrintTriangle=pbPrintTriangle # plain text print will not show on a web page
        )

        fileWithTriangle = drawSingleTriangleToNewImage(
            pListTriangle=t,
            pbShowTriangleImage=False,  # if True, the O.S.'s default viewer will be launched
            pbSaveTriangleToFile=True,
            pStrPathWereToSave=strDestinationPath
        )

        strKeyForTriangle = str(t)
        dictResult[strKeyForTriangle] = fileWithTriangle

        i0based+=1
    # for

    return dictResult, strDestinationPath
# def auxRandomPluralWebTrianglesOfType

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-21 - created
"""
def auxOutputDatasetAsJSONFromGeneratedDatasetAsDict(
    pDatasetAs5KeysDict:dict,
    piHowManySamplesPerTarget:int,
    pStrPathForTheJSONFile:str
):
    # getting ready to output a JSON file corresponding to the dataset
    strYMDHMS = AmUtil.utilNowYMDHMS()
    strJSONFileName = "triangles_dataset_%d_samples_per_target_%s.JSON" % (piHowManySamplesPerTarget, strYMDHMS)
    strJSONFileName = AmUtil.sanitizeFileName(strJSONFileName)
    if (pStrPathForTheJSONFile != ""):
        strJSONFileName = pStrPathForTheJSONFile + "/" + strJSONFileName
    # if

    testdict = {"R_T":123}
    jTestDict = json.dumps(testdict)

    strJSONData = json.dumps(pDatasetAs5KeysDict)
    fw = open(strJSONFileName, 'wt')
    fw.write(strJSONData)
    fw.close()

    return strJSONFileName
# def auxOutputDatasetAsJSONFromGeneratedDatasetAsDict

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-20 - created
"""
def auxRandomSingleWebDataset(
    piHowManySamplesPerTarget:int,
    pStrPathForGeneratedImages:str
):
    randomDatasetAs5KeysDict = \
        generateXRandomTrianglesToBeInscribedInImageAssuringEqualRepresentationOfAll4Targets(
            pSamplesPerTarget=piHowManySamplesPerTarget,
            pStrPathWereToSave=pStrPathForGeneratedImages
        )

    iTotalTriangles = len(randomDatasetAs5KeysDict['triangles'])

    """
    aux function "dictTrianglesCompatibleWithCreateSingleImage"
    expects to received a dict
    keys being a triangles's coordinates (e.g. [(1,2,3), (4,5,6), (7,8,9)]
    values being a path to an image of the triangle
    so, before calling it, make sure the argument is in the proper format
    """
    dictTrianglesCompatibleWithCreateSingleImage = dict()
    for t in range(iTotalTriangles):
        strCoordinates = str(randomDatasetAs5KeysDict['triangles'][t])
        imageFilePath = randomDatasetAs5KeysDict['files'][t]
        dictTrianglesCompatibleWithCreateSingleImage[strCoordinates]=imageFilePath
    # for

    # calling the function that build a combined image from the entire triangles dataset
    strPathOfCombinedImage = auxCreateSingleImageFromMultipleImagesOfSameSizeEachRepresentingTriangle(
        pDictTriangles=dictTrianglesCompatibleWithCreateSingleImage,
        pStrDestinationPath=pStrPathForGeneratedImages
    )

    strDatasetAsJSONFilename = auxOutputDatasetAsJSONFromGeneratedDatasetAsDict(
        pDatasetAs5KeysDict=randomDatasetAs5KeysDict,
        piHowManySamplesPerTarget=piHowManySamplesPerTarget,
        pStrPathForTheJSONFile=pStrPathForGeneratedImages
    )

    """
    just to remember the keys of a dataset as dict
    triangles (list of coordinates)
    angles (list of internal angles)
    lengths (list sides' lengths),
    targets (list of CORRECT targets, good for training)
    files (list of file paths to images)
    """

    strHtmlDataset = f"<h1>Your dataset of {iTotalTriangles} triangles is ready: <a href='/dl/{strDatasetAsJSONFilename}'>download it</a></h1>"
    strHtmlDataset += f"<h1>Dataset is available in JSON format: <a href='{strDatasetAsJSONFilename}'>view it</a></h1>"

    strHtmlDataset += "<ol>"

    for t in range(iTotalTriangles):
        strHtmlTriangle = "<ul>\n"

        coordinates = randomDatasetAs5KeysDict['triangles'][t]
        angles = randomDatasetAs5KeysDict['angles'][t]
        lengths = randomDatasetAs5KeysDict['lengths'][t]
        target = randomDatasetAs5KeysDict['targets'][t]
        imageFile = randomDatasetAs5KeysDict['files'][t]

        strCoordinates = str(coordinates)
        strAngles = str(angles)
        strLengths = str(lengths)
        strTarget = str(target)
        #strImageFile = f"<details><summary>{imageFile}</summary><img src=\"{imageFile}\"></details>" # it is crucial do properly delimit the path - if there are white spaces, not delimiting it, will result in broken paths
        strImageFile = f"<details><summary><a href='/dl/{imageFile}'>download</a> or expand to view the image.</summary><img src=\"{imageFile}\"></details>"  # it is crucial do properly delimit the path - if there are white spaces, not delimiting it, will result in broken paths

        strHtmlTriangle += f"<li><mark>coordinates</mark>: {strCoordinates}</li>\n"
        strHtmlTriangle += f"<li><mark>angles</mark>: {strAngles}</li>\n"
        strHtmlTriangle += f"<li><mark>lengths</mark>: {strLengths}</li>\n"
        strHtmlTriangle += f"<li><mark>target</mark>: {strTarget}</li>\n"
        strHtmlTriangle += f"<li>{strImageFile}</li>\n"

        strHtmlTriangle += "</ul>\n"
        strHtmlDataset += f"<li>{strHtmlTriangle}</li>\n"
    # for every triangle in dataset

    strHtmlDataset += "</ol>\n"

    strHtmlDataset +="<hr>"
    strHtmlDataset +=f"<img src='{strPathOfCombinedImage}'>" # crucial to delimit the path!

    return strHtmlDataset
# def auxRandomSingleWebDataset
#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def auxCreateSingleImageFromMultipleImagesOfSameSizeEachRepresentingTriangle(
    pDictTriangles,
    pColumns:int=2,
    pEachImageW:int=640,
    pEachImageH:int=480,
    pStrDestinationPath:str="",
    pBackgroundColorForCombinedImage=(255, 255, 255)
):
    iHowManyTriangles:int = len(pDictTriangles)
    iHowManyLinesAreNecessary:int = int(iHowManyTriangles/pColumns) # e.g. 2.5
    if(iHowManyTriangles%pColumns!=0):
        iHowManyLinesAreNecessary+=1

    # Image is PIL.Image
    iTotalW = pColumns * pEachImageW
    iTotalH = iHowManyLinesAreNecessary * pEachImageH
    imageSingle = Image.new(
        mode = 'RGB',
        size = (iTotalW,iTotalH), # size must be a tuple
        color = pBackgroundColorForCombinedImage
    )

    iCollageULX = iCollageULY = 0
    iCurrentCollage = 1
    for tCoordinates in pDictTriangles.keys():
        strPathToImage = pDictTriangles[tCoordinates]
        img =\
            Image.open(
                strPathToImage
            )
        imageSingle.paste(
            img,
            (iCollageULX, iCollageULY)
        )
        if(iCurrentCollage%2!=0): # odd 1,3,5, etc.
            iCollageULX+=img.width
        else: # eve´n 2,4,6, etc.
            iCollageULX=0
            iCollageULY+=img.height
        # else
        iCurrentCollage+=1
    # for

    if(pStrDestinationPath!=""):
        strFullDestinationPath = pStrDestinationPath+"/combined.PNG"
    else:
        strFullDestinationPath="combined.PNG"

    imageSingle.save(
        strFullDestinationPath
    )
    return strFullDestinationPath
# def auxCreateSingleImageFromMultipleImagesOfSameSizeEachRepresentingTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
@app.route("/", methods=["GET"])
def viewRootPresentTrianglesGenForm():
    render = render_template(
        "triangles_gen.html"
    )
    resp = make_response(
        render
    )
    return resp
# def viewRootPresentTrianglesGenForm

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-20 - created
notice the pImgStaticPath param alone, only catches paths up to the 1st /

this was relevant: https://riptutorial.com/flask/example/19420/catch-all-route
"""
#@app.route("/dl/<pImgStaticPath>", methods=["GET"]) # this will not work
@app.route("/dl/<path:pImgStaticPath>", methods=["GET"])
def dl(pImgStaticPath):
    # return pImgStaticPath # just to check that the route is being handled

    sendFileRet = send_file(
        pImgStaticPath,
        as_attachment=True # without this, the image would just be displayed
    )

    return sendFileRet
# def dl

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-19 - created
2022-06-21 - renamed to viewOutputSingleRandomTriangle
2022-06-23 - renamed to viewOutputSingleRandomTriangleOfType
"""
@app.route("/random_triangle_of_type_singular", methods=["POST"])
def viewOutputSingleRandomTriangleOfType():
    strNow = AmUtil.utilNowYMDHMS()
    strSubFolderInStatic = AmUtil.sanitizeFileName(strNow)

    method: str = request.method

    # GET method not in use - here kept just to remember how to handle GET
    if (method == "GET"):
        iHowManyTriangles: int = int(
            request.args[NAME_OF_INPUT_WITH_HOW_MANY_TRIANGLES]
        )
    # if

    if (method == "POST"):
        strTypeOfTriangle = request.form[NAME_OF_INPUT_WITH_TYPE_OF_TRIANGLE_SINGLE]
        typeOfTriangle:TriangleClassification = auxStringToTriangleClassificationDataType(strTypeOfTriangle)
    # if

    t, fileWithTriangle = auxRandomSingleWebTriangleOfType(
        pTypeOfTriangle = typeOfTriangle,
        pStrStorageSubFolderInStatic=strSubFolderInStatic
    )

    render = render_template(
        "gen_single_random_triangle_of_type.html",
        requestedTypeOfTriangle = typeOfTriangle,
        listTriangleCoordinates = t,
        pathToStaticImageWithATriangle=fileWithTriangle
    )

    resp = make_response(
        #str(t)
        render
    )
    return resp
# def viewOutputSingleRandomTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
"""
2022-06-20 - created named "random_triangle_v01_multiple"
2022-06-21 - renamed to "viewOuputPluralRandomTriangles"
2022-06-23 - renamed to viewOuputPluralRandomTrianglesOfType
"""
@app.route("/random_triangles_of_type_multiple", methods=["POST"])
def viewOuputPluralRandomTrianglesOfType():
    strNow = AmUtil.utilNowYMDHMS()
    strSubFolderInStatic = AmUtil.sanitizeFileName(strNow)

    method:str = request.method

    # GET method not in use - here kept just to remember how to handle GET
    if(method=="GET"):
        iHowManyTriangles:int = int(
            request.args[NAME_OF_INPUT_WITH_HOW_MANY_TRIANGLES]
        )
    # if

    if(method=="POST"):
        strTypeOfTriangle = request.form[NAME_OF_INPUT_WITH_TYPE_OF_TRIANGLE_PLURAL]
        typeOfTriangle: TriangleClassification = auxStringToTriangleClassificationDataType(strTypeOfTriangle)

        iHowManyTriangles:int = int(
            request.form[NAME_OF_INPUT_WITH_HOW_MANY_TRIANGLES]
        )
    # if

    """
    dictTriangles is a dictionary with keys being the coordinates of each triangle
    and value being the path to an image that illustrates the triangle (when using Python Flask, an image somewhere in the static folder) 
    """
    dictTriangles, strDestinationPath = auxRandomPluralWebTrianglesOfType(
        pTypeOfTriangle = typeOfTriangle,
        piHowManyTriangles=iHowManyTriangles,
        pStrStorageSubFolderInStatic=strSubFolderInStatic
    )

    # new 2022-06-21
    strDestinationPathOfCombinedImage = auxCreateSingleImageFromMultipleImagesOfSameSizeEachRepresentingTriangle(
        dictTriangles,
        pStrDestinationPath = strDestinationPath
    )

    render = render_template(
        "gen_multiple_random_triangles_of_type.html",
        iHowManyTriangles = iHowManyTriangles,
        dictGeneratedTriangles = dictTriangles,
        pStrDestinationPathOfCombinedImage = strDestinationPathOfCombinedImage
    )

    resp = make_response(
        render
    )

    return resp
# def viewOuputPluralRandomTriangles

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
@app.route("/random_dataset1", methods=["POST"])
def viewRandomDatasetWithRequestedNumberOfSamplesPerTarget():
    strNow = AmUtil.utilNowYMDHMS() # e.g. '2022-06-20 11:14:34'
    strSubFolderInStatic = AmUtil.sanitizeFileName(strNow) # e.g. '2022-06-20 111434'

    strDestinationPath = "static/" + strSubFolderInStatic + "/"
    createDirResult = AmUtil.createDir(strDestinationPath)

    method: str = request.method
    if (method == "GET"):
        iHowManySamplesPerClass: int = int(
            request.args[NAME_OF_INPUT_WITH_HOW_MANY_SAMPLES_PER_CLASS_IN_DATASET]
        )
    # if

    if (method == "POST"):
        iHowManySamplesPerClass: int = int(
            request.form[NAME_OF_INPUT_WITH_HOW_MANY_SAMPLES_PER_CLASS_IN_DATASET]
        )
    # if

    strHtmlForDataset =\
        auxRandomSingleWebDataset(
            piHowManySamplesPerTarget=iHowManySamplesPerClass,
            pStrPathForGeneratedImages=strDestinationPath
        )

    render = render_template(
        "gen_single_random_dataset.html",
        datasetAsDictAsString = strHtmlForDataset
    )

    resp = make_response(
        render
    )

    return resp
# def viewRandomDatasetWithRequestedNumberOfSamplesPerTarget

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
if (__name__=="__main__"):
    app.run(
        port=5000,
        debug=True
    )