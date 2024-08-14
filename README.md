# Predicting words belonging to pauses using ROBERTA-LARGE LM

This repository was made for predicting words belonging to pauses using ROBERTA-LARGE, a large-scale language model. This repository was made for the fulfilment of the master’s thesis information science at the Rijksuniversiteit Groningen.  The fine-tuned models that are trained on healthy speech can be used on Huggingface. These are available on this page: https://huggingface.co/Middelz2. 

## Acquiring the dataset
Since the entire dataset is too large to be pushed on Github and may contain sensitive personal information, the data can be made available on request. 

## Installing requirements

This library uses many different libraries. To ensure that all library requirements are met, first create a new virtual environment, locate to the folder and install all requirements using the following command:
```
pip install requirements.txt
```
## Folder explained

| Folder| Committed status | Information     |
|:---|:----:|---:|
| data | NO | All .cha data unpacked and converted to .txt files (original source).   |
| data_packed | NO | All .cha data packed in .zip files (original source). |
| deprecated | NO| Deprecated files that are no longer needed. |
| google_collab | YES| Contains the files to fine-tune and predict words using ROBERTA. |
| predictions | YES| Contains the final predictions of ROBERTA.  |
| qualtrics | YES| Contains files belonging to the survey.  |

## Files explained

The following files are most important in this repository.

| File| Information     |
|:---|:----:|
| data_exploration.py | This file was used to for an exploratory data analysis of the thesis.|  
| preprocessing.py | This file is centred around preprocessing the raw data into clean text. |
| remove_repetitions.py | Helper function for preprocessessing.py that helps remove stuttering.|
| setup_dataframe.py | Setup file that processes raw data into a usable .csv file. |

