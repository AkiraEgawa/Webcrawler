from lib.fileParser import fileParser
from lib.webcrawler import crawler

config = fileParser("testConfig.txt")
crawler(config)