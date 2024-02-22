import random

from triangle_dataset_tools import classifyTriangle, computeTriangleAnglesAndLengths
from triangle_dataset_tools import generateRandomAcuteTriangle, generateRandomObtuseTriangle, generateRandomRightScaleneTriangle, generateRandomRightIsoscelesTriangle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from IPython.display import display

from triangle_dataset_tools import *

RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0000FF"
CYAN = "#00BCE3"
PURPLE = "#9F2B68"
SOME_ORANGE = "#E36900"
BLACK = "#000000"
YELLOW = "#FFFF00"

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def createListOfColorsForEachDataPoint(
    pDataPoints, #typically X_train
    pCorrespondingTargetClasses, #typically y_train
    pdictCorrespondencesBetweenEachTargetClassAndDesiredColor: dict #typically a dictionary corresponding NUMERICAL target classes to colors as strings
)->list:
    listRet = []
    iHowManyDataPoints = len(pDataPoints)
    iHowManyTargetClasses = len(pCorrespondingTargetClasses)
    bCheckSameSize:bool = iHowManyDataPoints == iHowManyTargetClasses
    if (bCheckSameSize):
        for targetClass in pCorrespondingTargetClasses:
            iTargetClass = int(targetClass)
            strColorForCurrentTargetClass = pdictCorrespondencesBetweenEachTargetClassAndDesiredColor[iTargetClass]
            listRet.append(strColorForCurrentTargetClass)
        #for
    #if
    return listRet
#def

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def buildDatasetVisualizationBasedOnScatterMatrix(
    pX_train,
    py_train,
    pListFeatureNames,
    piTotalSamplesInDataset:int
):
    # Pandas is used ONLY FOR VISUALIZATION - for building a scatter matrix of the same data (X_train) that will train the model
    df = pd.DataFrame(
        data=pX_train,  # the 2D data as provided in the tuple returned by train_test_split
        # index = index to use for resulting frame. Will default to RangeIndex if no indexing information part of input data and no index provided.
        # columns = y_train, #the 1D numerical classes as provided in the tuple returned by train_test_split (x and y axes would display numbers)
        columns=pListFeatureNames  # keys for the angles ['P1P2_P1P3', 'P3P1_P3P2', 'P2P3_P2P1']
    )
    print(df)  # e.g. DataFrame shaped (300, 3), so size 300*3 = 900

    head = df.head()
    display(head)  # TODO: read about display vs print

    # an array of colors can be directly used as value for the named param c for pandas' scatter_matrix, IF IT IS THE SAME SIZE of the data points array
    dictColorsForEachTargetClassAsDesired = {
        0: RED,  # Acute # Red
        1: GREEN,  # Obtuse # Green
        2: BLACK,  # Right
        3: BLUE,  # Right-Scalene
        4: YELLOW  # Right-Isosceles
    }  # RGB color model

    listColorsToUsePerSampleInData = createListOfColorsForEachDataPoint(
        pX_train,
        py_train,
        dictColorsForEachTargetClassAsDesired
    )

    # while debugging in PyCharm scatter_matrix caused an exception, but it ran fine when called without debugger!
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.plotting.scatter_matrix.html
    pd.plotting.scatter_matrix(
        frame=df,
        alpha=0.7,
        # amount of opacity per plot (0 - can NOT see the plots ; 1 - makes it difficult to observe overlaps)
        diagonal="hist",
        # kde or hist #Pick between 'kde' and 'hist' for either Kernel Density Estimation or Histogram plot in the diagonal
        figsize=(15, 15),  # in inches
        marker='o',  # not just aesthetics - different markers might support color differently
        hist_kwds={"bins": piTotalSamplesInDataset},  # number of bars per histogram
        # c=py_train, #(112,) controls the color of the plots (received by kwargs) : will use matplotlib get_plot_backend("matplotlib")
        c=listColorsToUsePerSampleInData,
        s=40,  # scale of each plot
    )
    # plt.show() #without this, the plot might NOT appear

    # print ("END VISUALIZATION")
# def buildDatasetVisualizationBasedOnScatterMatrix

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def predictSingleTriangle(
    pClassifierToUse,
    pListOfPointsCorrespondingToTriangle,
    pListTargetNamesForClassesToPredict
):
    dictTrioOfAnglesLengths = computeTriangleAnglesAndLengths(pListOfPointsCorrespondingToTriangle)
    listTrioOfAngles = auxConvertDictAsTrioOfAnglesToListOfAngles(dictTrioOfAnglesLengths["angles"])
    correctClassification = classifyTriangle(pListOfPointsCorrespondingToTriangle)

    # the features of a triangle are its angles
    # the predict method of a KNN classifier object expect a numpy array argument
    compatibleRepresentationOfFeaturesIEAngles = np.array(
        [listTrioOfAngles]
    )

    #use knnResult, not knn?
    #aPredictionClassLabelsForEachSample is a numpy array
    aPredictionClassLabelsForEachSample = pClassifierToUse.predict(
        compatibleRepresentationOfFeaturesIEAngles
    ) # [0]

    strCorrectClass = pListTargetNamesForClassesToPredict[correctClassification]

    predictedClassForTheSingleSample = aPredictionClassLabelsForEachSample[0]
    bMachineLearnedOK = correctClassification == predictedClassForTheSingleSample

    strCorrect = "OK!"
    if (not bMachineLearnedOK):
        strCorrect = f"*WRONG* (correct is {correctClassification}:{strCorrectClass})"

    try:
        strPredictedClassByML = pListTargetNamesForClassesToPredict[predictedClassForTheSingleSample]

        """
        strFormat = "{} {} angles {} shaped {} predicted as class {} = {}".format(
            strCorrect,
            pListOfPointsCorrespondingToTriangle,
            compatibleRepresentationOfFeaturesIEAngles,
            compatibleRepresentationOfFeaturesIEAngles.shape,
            # pListOfPointsCorrespondingToTriangle,
            aPredictionClassLabelsForEachSample,
            strPredictedClassByML
        )
        """
        # removed the "shaped" info
        strFormat = f"{strCorrect} {pListOfPointsCorrespondingToTriangle} angles {listTrioOfAngles} " \
                    f"predicted {predictedClassForTheSingleSample}:{strPredictedClassByML}"

        print(strFormat)
    except Exception as e:
        # NOT EXPECTED!
        print("listTargetNamesForClassesToPredict", aPredictionClassLabelsForEachSample)
        print ("aPredictionClasses", aPredictionClassLabelsForEachSample)
        print (str(e))
    # try-except

#def  predictSingleTriangle

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
# pN just sets a number of tests
def predictRandomNTriangles(
    pClassifierToUse,
    pListTargetNamesForClassesToPredict:list,
    pN=100,
    pbPrintEachGeneratedTriangle:bool=False
):
    t = None

    for i in range(pN):
        # force a right triangle every 3 triangles
        if (i%3==0):
            # 50% chance it is isosceles
            x = random.randint(0,1)
            if(x):
                t = generateRandomRightIsoscelesTriangle(
                    pbPrintTriangle=pbPrintEachGeneratedTriangle
                )
            # 50% chance it is scalene
            else:
                t = generateRandomRightScaleneTriangle(
                    pbPrintTriangle=pbPrintEachGeneratedTriangle
                )
            #else
        else:
            # 50% chance it is acute
            x = random.randint(0, 1)
            if (x):
                t = generateRandomAcuteTriangle(
                    pbPrintTriangle=pbPrintEachGeneratedTriangle
                )
            # 50% chance it is obtuse
            else:
                t = generateRandomObtuseTriangle(
                    pbPrintTriangle=pbPrintEachGeneratedTriangle
                )
            # else
        #else

        predictSingleTriangle(
            pClassifierToUse=pClassifierToUse,
            pListOfPointsCorrespondingToTriangle=t,
            pListTargetNamesForClassesToPredict=pListTargetNamesForClassesToPredict
        )
        print("__"*30)
    #for
# def predictRandomNTriangles

# _.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
def trianglesModelAssessment(
    pTheModelAfterTraining,
    pDataSetAsDictFromJSON:dict,
    pPathToJsonFileWithDataset:str,
    pX_test, # samples reserved for testing
    py_test, # classification of samples reserved for testing
):
    # _.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
    # Evaluate the ML model around

    # the test data was NOT used to build the model
    # BUT the correct target classes / classifications are known
    y_pred = pTheModelAfterTraining.predict(
        pX_test
    )

    print("Known classes [correct classification of samples reserved for testing]:\n", py_test)
    print("Predicted classes [actual classification assigned to the samples reserved for testing]:\n", y_pred)

    npaMatches = y_pred == py_test
    print("Matches: ", npaMatches)

    fAverageMatches = np.mean(npaMatches)
    print("Model accuracy / average matches: ", fAverageMatches)

    fModelScoreComputedBySelf = pTheModelAfterTraining.score(pX_test, py_test)
    print("Model score by knn.score ", fModelScoreComputedBySelf)

    iSamplesPerTarget = len(pDataSetAsDictFromJSON["angles"]) // 4  # 4 target classes
    strTextForPlot = f"Dataset JSON file:\n{pPathToJsonFileWithDataset}\n" \
                     f"Samples per target: {iSamplesPerTarget}\n" \
                     f"Accuracy: {fModelScoreComputedBySelf}"
    # 0,0 is the bottom-left ; 1,1 is the top-right
    plt.text(0, 20, strTextForPlot)  # higher y, higher pos

    strFileName = f"{pPathToJsonFileWithDataset}.PNG"
    plt.savefig(strFileName)
    plt.show()  # without this, the plot might NOT appear
# def trianglesModelAssessment