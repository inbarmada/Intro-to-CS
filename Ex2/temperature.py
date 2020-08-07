############################################################
# FILE : temperature.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex2 2020
# DESCRIPTION: Find if at least two out of three numbers
#              are bigger than some threshold
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
############################################################


def is_it_summer_yet(threshold_temp, temp_one, temp_two, temp_three):
    """Find if at least two out of three numbers are bigger than some threshold"""
    days_over_threshold = 0

    # Check day 1
    if temp_one > threshold_temp:
        days_over_threshold += 1

    # Check day 2
    if temp_two > threshold_temp:
        days_over_threshold += 1

    # Check day 3
    if temp_three > threshold_temp:
        days_over_threshold += 1

    # Return whether at least 2 temperatures were bigger than the threshold
    if days_over_threshold >= 2:
        return True
    else:
        return False
