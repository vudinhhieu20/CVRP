#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-

from configparser import ConfigParser

# instantiate
config = ConfigParser()

# parse existing file
config.read("config.ini", encoding="utf-8")

###################Cau hinh service###################
APP_HOST = config.get("section service", "APP_HOST")
APP_PORT = config.getint("section service", "APP_PORT")
APP_RELOAD = config.get("section service", "APP_RELOAD")
APP_NUM_THREAD = config.get("section service", "APP_NUM_THREAD")


