'''
Simple start to see how the API works and also how i can then use that data and push it into 
a simple website to get some Astros stats!
'''

import statsapi
import logging


logger = logging.getLogger('statsapi')
logger.setLevel(logging.DEBUG)
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)8s - %(name)s(%(thread)s) - %(message)s")
ch.setFormatter(formatter)

rootLogger.addHandler(ch)


############ Code for stats

astrosID = 117

sched = statsapi.get('team', {'teamId' : astrosID})

print(sched)
