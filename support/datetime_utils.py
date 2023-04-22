'''
A collection of helper methods related to date, time, and datetime functions.
'''

def convert_seconds_to_d_h_m_s(seconds: float):
    '''Converts a given seconds value to days, hours, minutes, and seconds.

    Args:
        seconds (float): milliseconds to convert

    Returns:
        list: An integer list of the days, hours, minutes, and seconds converted from the input
        value.
    '''
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return int(days), int(hours), int(minutes), int(seconds)
