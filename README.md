# Comet

## Introduction
Comet processes YouTube videos' comments using Natural Language Processing(NLP).  
The `rating` of each comment is from 1 to 5, 1 being the least positive(most negative).  

## Requirement
Listed in `environment.yml`  

* `Python 3.7 or higher`
* `CUDA 11.1`
## Installation
Initialize the conda environment using `environment.yml`
## Usage
* Make sure to set your `youtubeapikey` variable in `environment.yml`  
* Set your conda environment, activate, then run `uvicorn main:app --reload`  
* Make API requests to `http://127.0.0.1:8000`
## API Endpoint
Refer to `http://127.0.0.1:8000/docs`
