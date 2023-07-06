import boto3
import os
from os import system
import pandas as pd


c = boto3.client("s3")
path = c.path("s3://bucket1/employee/")
jdbc_url = "jdbc:https://192.168.0.1:8080/mydatabase/"
table = "table1"
