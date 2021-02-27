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
* Set your conda environment, activate, then run `python main.py`  
* Input the video id from the desired YouTube video in the frontend UI  

## TODO
Currently only analyzing the newest 20 comments. Soon it will cover the entire video.  
This will be change its course and be a self-hosted API using FastAPI
