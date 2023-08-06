def strfseconds(seconds, formatstring='%h2:%m2:%s2', ndecimal=3):
    """Convert seconds to units of time.


    :param float or int seconds: The seconds to format
    :param str formatstring: The formatstring containing the format specifiers.
     Time units are:
        %w for weeks
        %d for days
        %h for hours
        %m for minutes
        %s for seconds
        %l for milliseconds (0.001 second)
        %f for microseconds (0.000001 second)
        %o for the unchanged seconds value
    :param int ndecimal: The number of decimals applied to the smallest unit
    :return: str: The formatted formatstring with all format specifiers replaced
    :rtype: str
    :raises TypeError: If seconds is not int, float or long
    :raises ValueError: If seconds is less than zero
    :raises TypeError: If formatstring is not a string
    :raises TypeError: If ndecimal is not an integer
    :raises ValueError: If ndecimal is smaller than 0
    """
   
    # Add al available time units
    units =[
        { # Weeks - secs = 60 * 60 * 24 * 7
        'name': 'w',
        'secs': 604800
        },
        { # Days - secs = 60 * 60 * 24 
        'name': 'd',
        'secs': 86400
        },
        { # Hours - secs = 60 * 60
        'name': 'h',
        'secs': 3600
        },
        { # Minutes
        'name': 'm',
        'secs': 60
        },
        { # Seconds
        'name': 's',
        'secs': 1
        },    
        { # Milliseconds
        'name': 'l',
        'secs': .001
        },
        { # Microseconds
        'name': 'f',
        'secs': .000001
        }]
    
    # Input validation plus initialization

    # seconds must be an integer or a float. If not raise type error.
    # (same behaviour as datetime.datetime.fromtimestamp).
    if type(seconds) not in (int, float):
        raise TypeError( 
            "a float is required (got type %s)" % type(seconds).__name__)
    if seconds < 0:
        raise ValueError( 
            "seconds must be greater than or equal to zero")

    # Add max value for seconds like datetime.timedelta does;
    # 86399999999999 is 2739726 years 
    # timedelta.max = timedelta(days=999999999, hours=23, minutes=59,
    #  seconds=59, microseconds=999999)
    if seconds > 86399999999999.999999:
        raise OverflowError(
            "seconds=%d; must be less than or equal to 86399999999999.999999" % (seconds))

    # formatstring must be of type string.
    if type(formatstring) != str:
        raise TypeError(
            "formatstring must be of type string (got type %s)" % type(formatstring).__name__)
    
    # ndecimal must be an integer greater than or equal to 0.
    if type(ndecimal) != int:
        raise TypeError(
            "ndecimal must be of type integer (got type %s)" % type(ndecimal).__name__)
    if ndecimal < 0:
        raise ValueError( 
            "ndecimal must be greater than or equal to 0 (got %s)" % ndecimal)
    
    
    # Initializtion is done

    # print(seconds)

    # Initialize seconds will be populated by `divmod` calculations.
    # Performace upgrade; removed seconds_remaining
    # seconds = seconds

    # Replace %o by the value passed for seconds
    formatstring = formatstring.replace('%o', str(seconds))

    # Determine the smallest timeunit in the formatstring;
    # when no smallest (any) timeunit found return the formatstring.
    # (same behaviour as 'datetime.strftime').
    smallest_unit_in_formatstring = None
    for unit in units:
        if formatstring.find( '%' + unit['name'] ) != -1:
            smallest_unit_in_formatstring = unit['name']
    if smallest_unit_in_formatstring is None:
        return formatstring

    # For every available time unit ...
    for unit in units:

        # ... check if unit is defined in the formatstring, if not 
        # continue to the next unit.
        if formatstring.find('%' + unit['name']) == -1:
            continue

        # Execute divmod on seconds for this units size: divide the 
        # number of seconds by this unit's number of seconds. 
        # The unit_size is assigned the quotient, seconds is assigned 
        # the remainder.
        unit_size, seconds = divmod(seconds, unit['secs'])

        # If this unit is the smallest unit add the remaining seconds 
        # as a decimal of this unit seconds size.
        if smallest_unit_in_formatstring == unit['name']:
            unit_size += 1 / unit['secs'] * seconds

            # Disable rounding completely; it is bad design to round 
            # when possible (not incrementing unit size) and not round
            # when not possible. 
            # Decimals will be precessed by format call with high value
            # for '.f' after which they will be truncated.

            # # Determine if unit_size can be formatted safely with format() and 
            # # that it will not roundup base unit size.
            # prevent_rounding = False
            # if round( 1 / unit['secs'] * seconds, ndecimal) == 1:
            # 	prevent_rounding = True
            # #else:
            # #    unit_size = round(unit_size, ndecimal)


        # Calculations are done. Convert unit_size to string and format 
        # appearance.

        
        # Determine leading zeroes ( '0%s' ).
        #
        # (Do not use None for unit_rjust_length as it's value is 
        # concatenated to this units name in the replace call.)
        unit_rjust_length = ''
        i = formatstring.find('%' + unit['name'] )
        if len(formatstring) > (i + 2) and formatstring[i+2] in ( '1', '2', '3', '4', '5', '6', '7', '8', '9'): 
            unit_rjust_length = formatstring[i+2]  


        if smallest_unit_in_formatstring != unit['name'] :
            # Apply format() for all non-smallest units. These units 
            # do not have decimals.

            # format string '0{unit_rjust_length}.0f'.
            # - Leading zeroes: Set '0%s.' to '0{unit_rjust_length}.' 
            # - Decimals: Set '.%sf' to '.0f'
            unit_size = format(unit_size, '0%s.0f' % 
                str(unit_rjust_length or 0))
            
        else:
            # Apply format() for smallest unit.

            # Prevent rounding, use format() with a value for '.%f' 
            # being 12 times larger than {ndecimal} after that chop 
            # off the decimals using substring.
            # 
            # Leading zeroes: Set '0%s.' to {ndecimal} + 12 +
            # {unit_rjust_length} + 1 (the decimal sign)
            # Decimals: Set '%sf' to a value relative to {ndecimal}; 
            # add 12 decimals.
            unit_size = format(unit_size, '0%s.%sf' % (
                str((ndecimal + 12) + int(unit_rjust_length or 0) + 1),
                str(ndecimal + 12)
                ))

            if ndecimal == 0:
                # No decimals; chop off string including and after the 
                # decimal sign 
                unit_size = unit_size[0:unit_size.find('.')]
            else:
               # Decimals; chop off string after decimal sign plus 
               # {ndecimal} plus 1 for the decimal sign itself.
               unit_size = unit_size[0:unit_size.find('.') + ndecimal + 1]

            # Truncate decimals manually
            # Convert unit_size to string ...
            # unit_size = str(unit_size)
            #if ndecimal == 0:
            #    # No decimals; chop off values including and after the 
            #    # decimal sign 
            #    unit_size = unit_size[0:unit_size.find('.')]
            #else:
            #   # Decimals; chop off values {ndecimal} after decimal sign 
            #   # (plus 1 for the decimal sign itself).
            #   unit_size = unit_size[0:unit_size.find('.') + ndecimal + 1]
            #   # ljust zeroes; when ndecimal=3 '0.5' should display 
            #   # as '0.500'
            #   unit_size = unit_size.ljust( unit_size.find('.') + ndecimal + 1, '0')
            ## rjust zeroes (leading zeroes)
            #unit_size = unit_size.rjust( len(unit_size) - unit_size.find('.') + int(unit_rjust_length), '0')

        # This is the last step for this unit's loop iteration; replace 
        # of the formatstring.
        formatstring = formatstring.replace('%' + unit['name'] + str(unit_rjust_length), unit_size)


    return formatstring
