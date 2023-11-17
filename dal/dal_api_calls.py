"""
Module Name: dal_api_calls
Description: This module provides functions to fetch data from an API for a range of years and
perform analysis on the data.
"""
import config
from custom_exceptions import NoResponseException
from logs import get_logger
import requests

logger = get_logger(__name__)


def fetch_data(year, gender, race, education):
    """
    Performs an API call for the year passed to it and returns the count of victims that match the parameters
    in that year.
    :param year: String to determine the year
    :param gender: String for the gender code used by the DOJ
    :param race: String for the racial code used by the DOJ
    :param education: String for the education code used by the DOJ
    :return: the year as a string and the number of victims.
    """
    try:
        points_url = f'{config.base_url}{config.endpoint}' \
                     f'.json?$query=select * where year = "{year}" limit 10000000'
        logger.info(f'Executing {points_url} JSON request')
        response = requests.get(points_url)

        if response.status_code == 200:
            count = 0
            for item in response.json():
                if (
                        item.get('sex') == str(gender) and
                        item.get('race_ethnicity') == str(race) and
                        item.get('educatn1') == str(education)
                ):
                    count += 1

            return year, count
        else:
            logger.error(f'Status Code: {response.status_code}')
            raise NoResponseException("API request failed")
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        raise NoResponseException()


def get_api_data(start_year, end_year, gender, race, education):
    """
    This function retrieves data for a range of years sequentially without using threads.
    :param start_year: User-inputted param that determines where the first year is
    :param end_year: User-inputted param that determines what will be the last year
    :param gender: User-inputted param that represents the identifier of male (1) or female (2)
    :param race: User-inputted param that represents the race using the string number in the API
    :param education: User-inputted param that represents the education level in the API
    :return: Dictionary of incidents
    """
    incidents_count = {}
    start_year_int = int(start_year)
    end_year_int = int(end_year)

    for year in range(start_year_int, end_year_int + 1):
        try:
            year, count = fetch_data(year, gender, race, education)
            logger.info(f'Retrieved Years: {year} and Counts: {count}')
            incidents_count[year] = count
        except NoResponseException as e:
            logger.error(f'Error in year {year}: {str(e)}')
            raise NoResponseException()
    return incidents_count
