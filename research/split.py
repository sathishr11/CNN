from shutil import copyfile, rmtree
import os
from pathlib import Path
import random
from tqdm import tqdm

rmtree(Path('C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs'))

to_create = [
    'C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs',
    'C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/training',
    'C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/testing',
    'C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/training/cats',
    'C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/training/dogs',
    'C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/testing/cats',
    'C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/testing/dogs'
]

for directory in to_create:
    try:
        os.mkdir(directory)
        print(directory, 'created')
    except:
        print(directory, 'failed')

def split_data(SOURCE, TRAINING, TESTING, SPLIT_SIZE):
    all_files = []
    
    for file_name in os.listdir(SOURCE):
        file_path = Path(os.path.join(SOURCE, file_name))

        if os.path.getsize(file_path):
            all_files.append(file_name)
        else:
            print('{} is zero length, so ignoring'.format(file_name))
    
    n_files = len(all_files)
    split_point = int(n_files * SPLIT_SIZE)
    
    shuffled = random.sample(all_files, n_files)
    
    train_set = shuffled[:split_point]
    test_set = shuffled[split_point:]
    
    for file_name in tqdm(train_set, desc='Creating Training set'):
        copyfile(
            Path(os.path.join(SOURCE, file_name)), 
            Path(os.path.join(TRAINING, file_name))
            )
        
    for file_name in tqdm(test_set, desc='Creating Test set'):
        copyfile(
            Path(os.path.join(SOURCE, file_name)), 
            Path(os.path.join(TESTING, file_name))
            )


CAT_SOURCE_DIR = Path("C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/PetImages/Cat")
TRAINING_CATS_DIR = "C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/training/cats/"
TESTING_CATS_DIR = "C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/testing/cats/"
DOG_SOURCE_DIR = Path("C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/PetImages/Dog")
TRAINING_DOGS_DIR = "C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/training/dogs/"
TESTING_DOGS_DIR = "C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/testing/dogs/"

split_size = .9
split_data(CAT_SOURCE_DIR, TRAINING_CATS_DIR, TESTING_CATS_DIR, split_size)
split_data(DOG_SOURCE_DIR, TRAINING_DOGS_DIR, TESTING_DOGS_DIR, split_size)

print(len(os.listdir('C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/training/cats/')))
print(len(os.listdir('C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/training/dogs/')))
print(len(os.listdir('C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/testing/cats/')))
print(len(os.listdir('C:/Users/satsathi/FSDS FT/localrepo/CNN/artifacts/data_ingestion/cats-v-dogs/testing/dogs/')))
