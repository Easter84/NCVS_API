"""
Module Name: Business Logic Layer
This module handles all communication between the presentation layer and the data access layer, it also
checks for faulty user input, and adjusts data types as necessary.
Author: Timothy Easter
"""
from dal import get_api_data
from custom_exceptions import NoResponseException, InvalidDataException
from logs import get_logger


logger = get_logger(__name__)


def verify_items_selected(start_year, end_year, race, education):
    """
    Checks to ensure that the combo boxes are selected, if not returns a logger warning
    :param Start_year: Variable from the combo box.
    :param End_year: Variable from combo box.
    :param Race: Variable from combo box.
    :param Education: Variable from combo box.
    :return: True or False
    """
    logger.info(f'Checking Year {start_year}')
    if start_year is not None:
        logger.info(f'Checking Year {end_year}')
        if end_year is not None:
            logger.info(f'Checking race {race}')
            if race is not None:
                if education is not None:
                    logger.info(f'Checking Education: {education}')
                    logger.info("Combo Boxes Values are good.")
                    return True
                else:
                    logger.warning('Education not selected.')
                    return False
            else:
                logger.warning('Race not selected.')
                return False
        else:
            logger.warning('End Year not selected.')
            return False
    else:
        logger.warning('Start Year not selected.')
        return False


def check_dates(start_year, end_year):
    """
    This function checks to ensure that the user selected appropriate date ranges
    :param Start_year: String retrieved from the start year combo box
    :param End_year: String retrieved from the end year combo box
    :return: True if years are good, False if there is a problem
    """
    logger.info(f'Checking if start date {start_year} is lower than end date {end_year}')
    try:
        end_year_int = int(end_year)
        start_year_int = int(start_year)
        if end_year_int - start_year_int >= 0:
            logger.info('Years within acceptable range')
            return True
        else:
            raise InvalidDataException('End Year must be greater then or equal to start year')
    except ValueError:
        logger.warning(f'Start Year: {start_year}, End Year: {end_year} in an invalid format')
        raise InvalidDataException("Invalid date format")


def get_data(start_year, end_year, gender, race, education):
    """
    This function takes the data from the GUI and sends it to the data access layer and then returns it to the
    GUI.
    :param Start_year: String from the start year drop box.
    :param End_year: String from the end year drop box.
    :param Gender: String from the gender radio button.
    :param Race: String from the race drop box.
    :param Education: String from the education drop box.
    :return: Data in format that the plot can use in the GUI.
    """
    try:
        start_year_str = str(start_year)
        end_year_str = str(end_year)
        data = get_api_data(start_year_str, end_year_str, gender, race, education)
        logger.info(f'Retrieved data')
    except NoResponseException:
        raise
    return data
