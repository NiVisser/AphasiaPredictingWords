# Predicting words belonging to pauses using ROBERTA-LARGE LM

This repository was made for predicting words belonging to pauses using ROBERTA-LARGE, a large-scale language model. The fine-tuned models that are trained on healthy speech can be used on Huggingface. These are available on this page: https://huggingface.co/Middelz2. 

## Acquiring the dataset
Since the entire dataset is too large to be pushed on Github and may contain sensitive personal information, the data can be made available on request. 

## Installing requirements

This library uses many different libraries. To ensure that all library requirements are met, first create a new virtual environment, locate to the folder and install all requirements using the following command:
```
pip install requirements.txt
```
## Files explained

The following files are most important in this repository.

| File| Information     |
|:---|:----:|
| preprocessing.py | This file is centred around preprocessing the raw (.csv) input sentenced into an extra dataframe column containing preprocessed (clean) text. |
| preprocessing_helper.py | Helper function for preprocessessing.py. Contains all additional functions that is used to clean the input sentences (.cha files) |
| setup_dataframe.py | Setup file that processes raw data (.txt data retrieved from .cha files) into a usable .csv file. |

## Jupyter notebooks

The following notebooks were used to train our roberta model and to make our predictions.


| File| Information     |
|:---|:----:|
| ROBERTA_Aphasia_Finetuning.ipynb | The file used to finetune our Roberta Large model. |
| ROBERTA_Aphasia_Single_[mask]_prediction.ipynb | The notebook used to make the predictions based on our large model. |

