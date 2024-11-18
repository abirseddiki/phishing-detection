import pandas as pd
import selenium
from bs4 import BeautifulSoup
import requests
import tldextract
import sklearn
import numpy as np
from requests_html import HTMLSession
from sentence_transformers import SentenceTransformer
import spacy

# Load spacy model
nlp = spacy.load("en_core_web_sm")

print("All libraries installed successfully!")
