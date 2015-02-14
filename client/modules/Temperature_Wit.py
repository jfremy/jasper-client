# -*- coding: utf-8-*-
import re

WORDS = []

def handle(text, mic, profile):
    mic.say("Température pas encore implémentée")

def isValid(text):
    return bool(re.search(r'\bdemande_temperature\b', text, re.IGNORECASE))
