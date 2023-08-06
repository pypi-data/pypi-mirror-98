# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 11:37:01 2021

@author: Tim Schreuder
"""

import random

def pull_trigger(patients, spots):
    """Choose one or more patients at random, dependent of how many ICU beds are available.

    Parameters
    ----------
    patients : list
        List of patients
    spots : int
        Number of available ICU beds

    Returns
    -------
    list
        A list of one ore more patients that have been randomly selected for an ICU bed.

    """
    assert type(patients) == list
    assert type(spots) == int
    return random.sample(patients, spots)

def input_patients():
    """Input the MDN numbers of the patients that are eligible for an ICU bed."""
    patients = []
    patient = None
    while patient != '':
        patient = input('Patient number (leave blank and press ENTER after last patient): ')
        if patient != '':
            patients.append(patient)
    return patients

def input_spots():
    """Input the number of IC beds that are available."""
    spots = input('How many ICU beds are available? ')
    return int(spots)

def tell_lucky_ones():
    """Print the patients that were allocated to an IC bed."""
    lucky_ones = pull_trigger(input_patients(), input_spots())
    print()
    for lucky_one in lucky_ones:
        print('Patient {} is selected for an ICU bed.'.format(lucky_one))

if __name__ == '__main__':
    tell_lucky_ones()