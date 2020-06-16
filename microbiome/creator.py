'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/creator.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome
Created Date: Monday, June 15th 2020, 7:47:00 pm
Author: Shapedsundew9


Copyright (c) 2020 Your Company
'''


from random import choice


def register_creator(creator_profile):
    return ''.join(choice('0123456789abcdef') for i in range(64))


def verify_creator(signature):
    return True
