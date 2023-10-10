"""CSCA08: Fall 2022 -- Assignment 3: Hypertension and Low Income

Starter code.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Jacqueline Smith, David Liu, and Anya Tafliovich

"""

from typing import TextIO
import statistics

from constants import (CityData, ID, HT, TOTAL, LOW_INCOME,
                       SEP, HT_ID_COL, LI_ID_COL,
                       HT_NBH_NAME_COL, LI_NBH_NAME_COL,
                       HT_20_44_COL, NBH_20_44_COL,
                       HT_45_64_COL, NBH_45_64_COL,
                       HT_65_UP_COL, NBH_65_UP_COL,
                       POP_COL, LI_POP_COL,
                       HT_20_44_IDX, HT_45_64_IDX, HT_65_UP_IDX,
                       NBH_20_44_IDX, NBH_45_64_IDX, NBH_65_UP_IDX
                       )
SAMPLE_DATA = {
    'West Humber-Clairville': {
        'id': 1,
        'hypertension': [703, 13291, 3741, 9663, 3959, 5176],
        'total': 33230, 'low_income': 5950},
    'Mount Olive-Silverstone-Jamestown': {
        'id': 2,
        'hypertension': [789, 12906, 3578, 8815, 2927, 3902],
        'total': 32940, 'low_income': 9690},
    'Thistletown-Beaumond Heights': {
        'id': 3,
        'hypertension': [220, 3631, 1047, 2829, 1349, 1767],
        'total': 10365, 'low_income': 2005},
    'Rexdale-Kipling': {
        'id': 4,
        'hypertension': [201, 3669, 1134, 3229, 1393, 1854],
        'total': 10540, 'low_income': 2140},
    'Elms-Old Rexdale': {
        'id': 5,
        'hypertension': [176, 3353, 1040, 2842, 948, 1322],
        'total': 9460, 'low_income': 2315}
}

SAMPLE_DATA2 = {
    'Whitehorse': {
        'id': 1,
        'hypertension': [704, 13294, 3744, 9664, 3954, 5174],
        'total': 33234, 'low_income': 5940},
    'Marsh Lake': {
        'id': 2,
        'hypertension': [785, 12906, 3575, 8815, 2922, 3922],
        'total': 32941, 'low_income': 9694},
    'Dawson': {
        'id': 3,
        'hypertension': [240, 3621, 1147, 2824, 1649, 1867],
        'total': 10365, 'low_income': 2044},
    'Carcross': {
        'id': 4,
        'hypertension': [206, 3662, 1137, 3229, 1395, 1855],
        'total': 10365, 'low_income': 2144},
    'Mayo': {
        'id': 5,
        'hypertension': [172, 3356, 1047, 2872, 949, 1342],
        'total': 9461, 'low_income': 2325}
}

EPSILON = 0.005


def get_hypertension_data(nbh_data: dict, hyp_data: TextIO) -> None:
    """Update dictionary nbh_data to contain hypertension data hyp_data, while
    the neighbourhood names in file hyp_data become the keys of the disctionary
    nbh_data and HT and ID become the values. ID and HT contain data from
    hyp_data. If neighbourhood names not in nbh_data, that neighbourhood's
    hypertension data will be added to dictionary nbh_data.
    """
    hyp_data.readline()
    for line in hyp_data:
        hyp_line = line.strip().split(SEP)
        if hyp_line[HT_NBH_NAME_COL] not in nbh_data:
            nbh_data[hyp_line[HT_NBH_NAME_COL]] = {ID: int(hyp_line[HT_ID_COL]
                                                           ), HT: []}
        else:
            nbh_data[hyp_line[HT_NBH_NAME_COL]][HT] = []
        for i in range(HT_20_44_COL, NBH_65_UP_COL+1):
            nbh_data[hyp_line[HT_NBH_NAME_COL]][HT].append(int(hyp_line[i]))


def get_low_income_data(nbh_data: dict, low_data: TextIO) -> None:
    """Update dictionary nbh_data to contain low-income data low_data, while
    the neighbourhood names in file low_data become the keys of the disctionary
    low_data and TOTAL and LOW_INCOME become the values. TOTAL and LOW_INCOME
    contain data from low_data. If neighbourhood names not in nbh_data, that
    neighbourhood's low-income data will be added to dictionary nbh_data.
    """
    low_data.readline()
    for line in low_data:
        low_line = line.strip().split(',')
        if low_line[LI_NBH_NAME_COL] not in nbh_data:
            nbh_data[low_line[LI_NBH_NAME_COL]] = {ID: int(low_line[
                LI_ID_COL]), TOTAL: int(low_line[POP_COL]), LOW_INCOME: int(
                    low_line[LI_POP_COL])}
        else:
            nbh_data[low_line[LI_NBH_NAME_COL]][TOTAL] = int(low_line[POP_COL])
            nbh_data[low_line[LI_NBH_NAME_COL]][LOW_INCOME] = int(low_line[
                LI_POP_COL])


def get_bigger_neighbourhood(city_data: CityData, nbh1: str, nbh2: str) -> str:
    """Return the neighbourhood name that has the higher population in data
    city_data between neighbourhood 1 nbh1 and neighbourhood 2 nbh2. If both of
    them have the same population, return neighbourhood 1 nbh1. Neighbourhood
    not in data city_data has 0 population.

    Precondition: nbh1 != nbh2
                  No neighbourhood in city_data has 0 population.

    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Rexdale-Kipling',
    ... 'Elms-Old Rexdale')
    'Rexdale-Kipling'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Elms-Old Rexdale',
    ... 'Rexdale-Kipling')
    'Rexdale-Kipling'
    >>> get_bigger_neighbourhood(SAMPLE_DATA2, 'Carcross', 'Dawson')
    'Carcross'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'a', 'West Humber-Clairville')
    'West Humber-Clairville'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Rexdale-Kipling', 'e')
    'Rexdale-Kipling'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'b', 'a')
    'b'

    """
    if nbh1 in city_data and nbh2 in city_data:
        if city_data[nbh1][TOTAL] >= city_data[nbh2][TOTAL]:
            return nbh1
    if nbh2 not in city_data:
        return nbh1
    return nbh2


def get_high_hypertension_rate(city_data: CityData,
                               threshold: float) -> list[tuple[str, float]]:
    """Return a list of tuples containing the neighbourhoods' name first whose
    hypertension rates are higher or equal to threshold threshold, and their
    hypertension rates. The hypertension rates are computed by dividing the
    total number of hypertensive patients by the total number of adults in the
    neighbourhood based on data city_data.

    Precondition: 0.0 <= threshold <= 1.0
                  No neighbourhood has 0 population.

    >>> get_high_hypertension_rate(SAMPLE_DATA, 1.0)
    []
    >>> get_hyp_rate1 = [('Thistletown-Beaumond Heights', 0.31797739151574084),
    ... ('Rexdale-Kipling', 0.3117001828153565)]
    >>> get_hyp_rate1 == get_high_hypertension_rate(SAMPLE_DATA, 0.3)
    True
    >>> get_hyp_rate2 = [('West Humber-Clairville', 0.2987202275151084),
    ... ('Mount Olive-Silverstone-Jamestown', 0.28466612028255867),
    ... ('Thistletown-Beaumond Heights', 0.31797739151574084),
    ... ('Rexdale-Kipling', 0.3117001828153565),
    ... ('Elms-Old Rexdale',0.2878808035120394)]
    >>> get_hyp_rate2 == get_high_hypertension_rate(SAMPLE_DATA, 0.0)
    True

    """
    nbh_list = []
    for nbh in city_data:
        hyp_list = city_data[nbh][HT]
        num_hyp = hyp_list[0] + hyp_list[2] + hyp_list[4]
        total_adult = hyp_list[1] + hyp_list[3] + hyp_list[5]
        hyp_rate = num_hyp / total_adult
        if hyp_rate >= threshold:
            nbh_list.append((nbh, hyp_rate))
    return nbh_list


def get_ht_to_low_income_ratios(city_data: CityData) -> dict[str, float]:
    """Return a dictionary that contains keys that are the neighbourhood
    names in data city_data and values that are the proportion of hypertension
    rate to low-income rate for that neighbourhood. Low-income rate is ratio
    of the number of low-income people to total population, while hypertension
    rate is the ratio of total number of hypertensive people to the total
    number of adults in the neighbourhood according to data city-data.

    Precondition: no neighbourhood has 0 population.

    >>> get_low_ratios1 = {'West Humber-Clairville': 1.6683148168616895,
    ... 'Mount Olive-Silverstone-Jamestown': 0.9676885451091314,
    ... 'Thistletown-Beaumond Heights': 1.6438083107534431,
    ... 'Rexdale-Kipling': 1.5351962275111484,
    ... 'Elms-Old Rexdale': 1.1763941257986577}
    >>> get_low_ratios1 == get_ht_to_low_income_ratios(SAMPLE_DATA)
    True
    >>> get_low_ratios2 = {'Whitehorse': 1.6710068838534642,
    ... 'Marsh Lake': 0.9649739864604389, 'Dawson': 1.8521862151059745,
    ... 'Carcross': 1.513451458406572, 'Mayo': 1.165406627746765}
    >>> get_low_ratios2 == get_ht_to_low_income_ratios(SAMPLE_DATA2)
    True

    """
    ratios = {}
    for nbh in city_data:
        hyp_list = city_data[nbh][HT]
        num_hyp = hyp_list[0] + hyp_list[2] + hyp_list[4]
        total_adult = hyp_list[1] + hyp_list[3] + hyp_list[5]
        hyp_rate = num_hyp / total_adult
        low_rate = city_data[nbh][LOW_INCOME] / city_data[nbh][TOTAL]
        ratios[nbh] = hyp_rate / low_rate
    return ratios


def calculate_ht_rates_by_age_group(city_data: CityData,
                                    nbh_name: str) -> tuple[float,
                                                            float, float]:
    """Return a tuple that contains the hypertension percentages of age group
    20-40, 45-64, 65+ of neighbourhood nbh. Each hypertension percentage is
    computed by dividing the number of hypertension patients of the age group
    by the population of the age group according to the data city_data and then
    multuplied by 100.

    Precondition: no neighbourhood has a 0 population.
                  nbh_name in city_data

    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA, 'Elms-Old Rexdale')
    (5.24903071875932, 36.593947923997185, 71.70953101361573)
    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA,
    ... 'Thistletown-Beaumond Heights')
    (6.058936931974663, 37.009544008483566, 76.34408602150538)
    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA, 'Rexdale-Kipling')
    (5.478331970564186, 35.119231960359244, 75.13484358144552)

    """
    hyp_rate_20_44 = (city_data[nbh_name][HT][0] / city_data[nbh_name][HT][1])
    hyp_rate_45_64 = (city_data[nbh_name][HT][2] / city_data[nbh_name][HT][3])
    hyp_rate_65 = (city_data[nbh_name][HT][4] / city_data[nbh_name][HT][5])
    return hyp_rate_20_44 * 100, hyp_rate_45_64 * 100, hyp_rate_65 * 100


def get_age_standardized_ht_rate(city_data: CityData, nbh_name: str) -> float:
    """Return the age standardized hypertension rate from the
    neighbourhood in city_data with neighbourhood name nbh_name.

    Precondition: nbh_name is in city_data

    >>> abs(get_age_standardized_ht_rate(SAMPLE_DATA, 'Elms-Old Rexdale') -
    ...     24.44627) < EPSILON
    True
    >>> abs(get_age_standardized_ht_rate(SAMPLE_DATA, 'Rexdale-Kipling') -
    ...     24.72562) < EPSILON
    True

    """

    rates = calculate_ht_rates_by_age_group(city_data, nbh_name)

    # These rates are normalized for only 20+ ages, using the census data
    # that our datasets are based on.
    canada_20_44 = 11_199_830 / 19_735_665   # Number of 20-44 / Number of 20+
    canada_45_64 = 5_365_865 / 19_735_665    # Number of 45-64 / Number of 20+
    canada_65_plus = 3_169_970 / 19_735_665  # Number of 65+ / Number of 20+

    return (rates[0] * canada_20_44 + rates[1] * canada_45_64 +
            rates[2] * canada_65_plus)


def get_correlation(city_data: CityData) -> float:
    """Return the Pearson’s correlation coefficient for age standardised
    hypertension rates and low income rates for all neighbourhood in data
    city_data.

    >>> get_correlation(SAMPLE_DATA)
    0.28509539188554994
    >>> get_correlation(SAMPLE_DATA2)
    -0.17647340808301218

    """
    age_hyp_rates = []
    low_rates = []
    for nbh_name in city_data:
        age_hyp_rates.append(get_age_standardized_ht_rate(city_data, nbh_name))
        low_rates.append(city_data[nbh_name][LOW_INCOME] / city_data[nbh_name][
            TOTAL])
    return statistics.correlation(age_hyp_rates, low_rates)


def order_by_ht_rate(city_data: CityData) -> list[str]:
    """Return a list of neighborhood names in ascending order of their
    age-standardized hypertension rates based on data city-data.

    Precondition: all neighbourhoods' hypertension rate are unique.

    >>> order_by_ht1 = ['Elms-Old Rexdale', 'Rexdale-Kipling',
    ... 'Thistletown-Beaumond Heights', 'West Humber-Clairville',
    ... 'Mount Olive-Silverstone-Jamestown']
    >>> order_by_ht1 == order_by_ht_rate(SAMPLE_DATA)
    True
    >>> order_by_ht2 = ['Mayo', 'Carcross', 'Whitehorse', 'Marsh Lake',
    ... 'Dawson']
    >>> order_by_ht2 == order_by_ht_rate(SAMPLE_DATA2)
    True

    """
    age_hyp_rates = []
    age_hyp_to_name = {}
    name_order = []
    for nbh_name in city_data:
        age_hyp_rates.append(get_age_standardized_ht_rate(city_data, nbh_name))
        age_hyp_to_name[get_age_standardized_ht_rate(city_data,
                                                     nbh_name)] = nbh_name
    age_hyp_rates.sort()
    for age_hyp in age_hyp_rates:
        name_order.append(age_hyp_to_name[age_hyp])
    return name_order


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Uncomment when ready to test:
    # Using the small data files:
    small_data = {}
    # add hypertension data
    with open('../a3/hypertension_data_small.csv') as ht_small_f:
        get_hypertension_data(small_data, ht_small_f)

    # add low income data
    with open('../a3/low_income_small.csv') as li_small_f:
        get_low_income_data(small_data, li_small_f)

    print('Did we build the dict correctly?', small_data == SAMPLE_DATA)
    print('Correlation in small data file:', get_correlation(small_data))

    # Using the example data files:
    example_neighbourhood_data = {}
    # add hypertension data
    with open('../a3/hypertension_data_2016.csv') as ht_example_f:
        get_hypertension_data(example_neighbourhood_data, ht_example_f)
    # add low income data
    with open('../a3/low_income_2016.csv') as li_example_f:
        get_low_income_data(example_neighbourhood_data, li_example_f)
    print('Correlation in example data file:',
          get_correlation(example_neighbourhood_data))
