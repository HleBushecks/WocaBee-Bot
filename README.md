# WocaBee-Bot

## About
#### This selenium app can complit tasks in WocaBee. This app can't complit all tasks, app can complite only "Translate", "Choose the correct translation", "Fill in the missing characters", "Select the correct pair"

## How it's working?
#### The app use "Google Translate" for translating words, if translated word from "Google Translate" is not correct for WocaBee than word with correct translate will save to file and will use this word from file

## Requirements
> Python3, WebDriver
#### Python modules
> selenium==4.8.0 
###### and
> googletrans==3.1.0a0 

## How to start?
#### For starting run the command
> python main.py
#### The app has autologin if you set login and password in config.py and run with flag
> python main.py --autologin

## How to use config?
#### First and second languages are languages use in a test

