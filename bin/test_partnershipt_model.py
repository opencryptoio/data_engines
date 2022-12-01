
import os
import openai
import re
from gnews import GNews
from traceback import print_exc
import requests
import re
import json

ai_response = openai.Completion.create(
        model="curie:ft-personal-2022-11-29-01-52-01 ",
        prompt= cut_articletitle + cut_articletext + "#####END#####",
        temperature=0,
        max_tokens=64,
        top_p=0.4,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )