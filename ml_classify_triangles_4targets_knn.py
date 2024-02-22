import sys
sys.path.extend(['F:\\coding.jb\\py\\AM', 'F:/coding.jb/py/AM'])

#from triangle_dataset_tools import *
from ml_classifier_tools import *

from sklearn.neighbors import KNeighborsClassifier # do NOT do imports later than this section
from sklearn import model_selection

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
# STAGE 0 - load a dataset from file
# and make available comfortable vars dictDatasetFromJSON, listOfListsEachATrioOfAngles, listOfTargetsForEachTrioOfAngles, listFeatureNames

DEFAULT_DATASET = "datasets.json/triangles_dataset_100_samples_per_target_2022-6-24_1-0-37.JSON"
# DEFAULT_DATASET = "triangles_dataset_2_samples_per_target_2022-06-24 110424.JSON"

print(sys.argv)
if (len(sys.argv) == 2):
    print(f"JSON data set file specified, using {sys.argv[1]}")
    PATH_TO_JSON_FILE_WITH_DATASET = sys.argv[1]
else:
    print("No JSON data set file specified, using default")
    PATH_TO_JSON_FILE_WITH_DATASET = DEFAULT_DATASET

dictDatasetFromJSON, listOfListsEachATrioOfAngles, listOfTargetsForEachTrioOfAngles, listFeatureNames = \
    trianglesDatasetLoaderFromFile(
        pStrFilePath=PATH_TO_JSON_FILE_WITH_DATASET,
        pbVerbose=True
    )

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
# STAGE 1 - get the samples organized in training and testing parts
# made available with the classical names X_train, X_test, y_train, y_test

tupleTrainAndTestsSets = model_selection.train_test_split(
    listOfListsEachATrioOfAngles,
    listOfTargetsForEachTrioOfAngles,
    #random_state=0, #Controls the shuffling applied to the data before applying the split. Pass the same int for reproducible output across multiple function calls.
    shuffle=True
)
X_train, X_test, y_train, y_test = tupleTrainAndTestsSets

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
# STAGE 2 - optional - one observation of the dataset

buildDatasetVisualizationBasedOnScatterMatrix(
    pX_train=X_train,
    py_train=y_train,
    pListFeatureNames=listFeatureNames,
    piTotalSamplesInDataset=len(listOfListsEachATrioOfAngles)
)
#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
# STAGE 3 - build and train a model

#Building a ML model around the KNN algorithm
#KNeighborsClassifier data type
knn = KNeighborsClassifier(
    algorithm="auto", #"auto", "brute", "ball_tree", "kd_tree"
    leaf_size=30, #Leaf size passed to BallTree or KDTree. This can affect the speed of the construction and query, as well as the memory required to store the tree
    metric="minkowski", #The distance metric to use for the tree. The default metric is minkowski, and with p=2 is equivalent to the standard Euclidean metric
    metric_params=None, #Additional keyword arguments for the metric function.
    n_jobs=1, #The number of parallel jobs to run for neighbors search
    n_neighbors=1,
    p=2, # p=1 => manhattan_distance (l1), p=2 => euclidean_distance
    weights="uniform" #All points in each neighborhood are weighted equally
)

# train the model with the available examples
# the result is also KNeighborsClassifier data type (same as knn)
knnResult = knn.fit(
    X_train,
    y_train
)
display (knnResult)

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
# STAGE 4 - assess the model

# the listTargetNamesForClassesToPredict is ONLY used for extracting a human-readable string for the classification
# it does NOT influence the classification process at all
# the code will, at a point, make a simple correspondence between classification (by KNN) numbers and strings,
# so, even if running the 4-targets mode, PLEASE DO PROVIDE the "Right" string @2, or class "Right-Scalene" will be @index 2, and "Right-Isosceles @index 3,
# causing wrong prints and a None classification for class 4, because there would be no string @index 4
# listTargetNamesForClassesToPredict = ["Acute", "Obtuse", "Right"]
listTargetNamesForClassesToPredict = ["Acute", "Obtuse", "Right", "Right-Scalene", "Right-Isosceles"]
strFormat = "Target classes names:" + str(listTargetNamesForClassesToPredict)
print(strFormat)

predictRandomNTriangles(
    pClassifierToUse=knnResult,
    pN=100,
    pbPrintEachGeneratedTriangle=False,
    pListTargetNamesForClassesToPredict=listTargetNamesForClassesToPredict
)

trianglesModelAssessment(
    pTheModelAfterTraining=knnResult,
    pDataSetAsDictFromJSON=dictDatasetFromJSON,
    pPathToJsonFileWithDataset=PATH_TO_JSON_FILE_WITH_DATASET,
    pX_test = X_test,  # samples reserved for testing
    py_test = y_test,  # classification of samples reserved for testing
)

print(f"{__name__} END.")