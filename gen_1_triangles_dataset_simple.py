from triangle_dataset_tools import produceDatasetWithCorrectClassificationsForSupervisedLearningSaveAsJSON

#_.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-._.-~^~-.
HOW_MANY_DATASETS_DO_YOU_WANT = 1
NUMBER_OF_SAMPLES_PER_TARGET = 100
STEP = 100
for idx in range(HOW_MANY_DATASETS_DO_YOU_WANT):
    strDatasetFilename = \
        produceDatasetWithCorrectClassificationsForSupervisedLearningSaveAsJSON(
            pNumberOfSamplesPerClass = NUMBER_OF_SAMPLES_PER_TARGET,
            pbGenerateFilesForImages=True
        )
    NUMBER_OF_SAMPLES_PER_TARGET+=STEP
    print ("Wrote new dataset to: ", strDatasetFilename)
#for