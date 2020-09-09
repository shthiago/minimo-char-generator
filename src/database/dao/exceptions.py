'''Exceptions for dao processes'''


class NegativeSelecionTentative(Exception):
    '''Number of features for random selection must be non-negative'''


class InvalidGender(Exception):
    '''Gender selected for random selection not available'''
