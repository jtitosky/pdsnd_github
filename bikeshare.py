import sys
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def query_user(query,options=['y','n'],options_short=None,options_int_offset=0):
    """
    Input:
        (str) query - the prompt displayed to the user
        (list) options - possible options for the user to select.
             Requires options to be not be digits only. 
        (list) options_short - list of options in short (3 char) format
        (int) options_int_offset - offset for user's input in int

    Returns:
        (str) option selected by user, once a valid option is chosen
    """

    while True:
        try:
            answer = input(query).strip().lower()

            # If digit, assume user is using index
            if answer.isdigit() \
                and int(answer) \
                in range(0 + options_int_offset,
                    len(options) + 1 + options_int_offset):
                answer = options[int(answer) - options_int_offset]
            # If 3 alpha characters, assume that using short form
            elif answer.isalpha() and options_short != None:
                if len(answer) == 3 and answer in options_short:
                    answer = options[options_short.index(answer)]
            if answer in options:
                break
            else:
                print("\nERROR: That doesn't seem to be one of the options." 
                    "Please try again.")
        except KeyboardInterrupt:
            print("\nERROR: User requested exit.")
            sys.exit(0)
        except:
            print("\nERROR: Something wasn't quite right. Please try again.")
        
    return str(answer)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
             or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
             or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    
    # Generate properly formatted question for city user input query
    city_query = "\nWhich city would you like data for? ("
    cities_ordered = sorted(CITY_DATA.keys())
    for i in range(0,len(cities_ordered)):
        # Last city in list
        if i + 1 == len(cities_ordered):
            city_query += cities_ordered[i].title() + "): "
        # Second last city in list
        elif i + 2 == len(cities_ordered):
            city_query += cities_ordered[i].title() + " or "
        else:
            city_query += cities_ordered[i].title() + ", "

    while True:
        # Ask user for city
        while True:
            city = query_user(city_query,CITY_DATA)
            confirmation = query_user(
                "\nYou've selected {}. Is that correct? [Y/N]: ".format(
                    city.upper()))
            if confirmation == "y":
                break
        # TO DO: get user input for month (all, january, february, ... , june)
        
        months = ["january","february","march","april","may","june","july",\
        "august","september","october","november","december", "all"]
        months_short = ["jan","feb","mar","apr","may","jun","jul","aug","sep",\
        "oct,","nov","dec"]

        month_query = "\nWhat month would you like data for? "\
            + "[1-12, Jan-Dec, January-December, All]: "
        while True:
            month = query_user(month_query,months,months_short,1)
            confirmation = query_user(
                "\nYou've selected {}. Is that correct? [Y/N]: ".format(
                    month.upper()))
            if confirmation == "y":
                break

        # Get user input for day of week (all, monday, tuesday, ... sunday)
        days = ["sunday","monday","tuesday","wednesday","thursday","friday",\
            "saturday", "all"]
        days_short = ["sun","mon","tue","wed","thu","fri","sat"]

        day_query = "\nWhat day would you like data for? "\
            + "[1-7, Sun-Sat, Sunday-Saturday, All]: "
        while True:
            day = query_user(day_query,days,days_short,1)
            confirmation = query_user(
                "\nYou've selected {}. Is that correct? [Y/N]: ".format(
                    day.upper()))
            if confirmation == "y":
                break

        
        print("\nYour current selection is:")
        print("  City: {}".format(city.title()))
        print("  Month: {}".format(month.title()))
        print("  Day: {}".format(day.title()))

        confirmation = query_user("\nIs that correct? [Y/N]: ")
        if confirmation == "y":
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
            or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
            or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    new_query_needed = False
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # Filter by month if applicable
    month = month.strip().lower()
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june',\
        'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
    
        # Get months in dataset
        months_available = sorted(df.month.unique())
        if month not in months_available:
            print("\nERROR: {} is not available for selected dataset.".format(
                months[month - 1].title()))
            for i in range(len(months_available)):
                months_available[i] = months[months_available[i] - 1]
            print("\nMonths that ARE available are: \n  ")
            print(str(months_available))
            new_query_needed = True
        else:
            # Filter by month to create the new dataframe
            df = df[df['month'] == month]

    # Filter by day of week if applicable
    day = day.strip().title()
    if day != 'All':
        # Filter by day of week to create the new dataframe
        days_available = sorted(df.day_of_week.unique())
        if day not in days_available:
            print("\nERROR: {} is not available for selected dataset.".format(
                day))
            print("\nDays that ARE available are: \n  ")
            print(str(days_available))
            new_query_needed = True
        else:
            df = df[df['day_of_week'] == day]

    if new_query_needed:
        print("\nRequested data not in dataset. We will have to start over.\n")
        print('-'*40)
        df = None
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    months = ['january', 'february', 'march', 'april', 'may', 'june',\
        'july', 'august', 'september', 'october', 'november', 'december']

    # Display the most common month
    print("\nMost common month:")
    print(months[int(df['month'].mode()[0]) - 1].title())

    # Display the most common day of week
    print("\nMost common day of week:")
    print(df['day_of_week'].mode()[0])

    # Display the most common start hour
    print("\nMost common start hour:")
    print(df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # Display most commonly used start station
    col = "Start Station"
    if col in df.columns:
        print("\nMost common start station:")
        print(df[col].mode()[0])
    else:
        print("\n{} not present in dataset. Related stats skipped.".format(col))

    # Display most commonly used end station
    col = "End Station"
    if col in df.columns:
        print("\nMost common {}:".format(col))
        print(df[col].mode()[0])
    else:
        print("\n{} not present in dataset. Related stats skipped.".format(col))

    # Display most frequent combination of start station and end station trip
    col1 = "Start Station"
    col2 = "End Station"
    if col1 in df.columns and col2 in df.columns:
        start_end = df.groupby(
            [col1, col2]).size().reset_index().rename(
                columns={0:'Count'})
        start_end_max = \
        start_end[start_end['Count'] == start_end['Count'].max()]
        print("\nMost common combination of start and end:")
        print("  {}: {}".format(
            col1,start_end_max[col1].values[0]))
        print("  {}: {}".format(col2,start_end_max[col2].values[0]))
        print("  Count: {}".format(start_end_max['Count'].values[0]))
    else:
        print("\n{}/{} not present in dataset. Related stats skipped.".format(
            col1.col2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    col = "Trip Duration"
    if col in df.columns:
        # Display total travel time
        print("\nTotal travel time of all trips:")
        print(str(df[col].sum()))

        # Display mean travel time
        print("\nMean travel time of all trips:")
        print(str(df[col].mean()))
    else:
        print("\n{} not present in dataset. Related stats skipped.".format(col))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    col = "User Type"
    if col in df.columns:
        print("\n" + df.groupby(col).size().to_string())
    else:
        print("\n{} not present in dataset. Related stats skipped.".format(col))

    # Display counts of gender
    col = "Gender"
    if col in df.columns:
        print("\n" + df.groupby(col).size().to_string())
            #.reset_index().rename(columns={0:'Count'}))
    else:
        print("\n{} not present in dataset. Related stats skipped.".format(col))

    # Display earliest, most recent, and most common year of birth
    col = "Birth Year"
    if col in df.columns:
        # Earliest
        print("\nEarliest {}:".format(col))
        print(int(df[col].min()))
        # Recent
        print("\nMost recent {}:".format(col))
        print(int(df[col].max()))
        # Most Common
        print("\nMost common {}:".format(col))
        print(int(df[col].mode()))
    else:
        print("\n{} not present in dataset. Related stats skipped.".format(col))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def disp_raw_data(df,increment=5):
    """
    Displays raw data from the passed dataframe
    
    Args:
        (df) df - dataframe being viewed
        (int) increment - the amount of lines to display at a time
    """

    rows = len(df.index)
    increments = int(rows / increment)

    i = 1
    while i <= increments + 1:
        tail = i * increment
        head = tail - increment
        if i <= increments:
            print (df.iloc[head:tail])
        else:
            print (df.iloc[head:])
        print("\nThere are {} lines remaining".format(rows - i * increment))
        conf = query_user(
            "\nWould you like to see {} more lines? [Y/N]: ".format(increment))
        if conf == "n":
            break
        i+=1

def main():
    while True:

        df = None
        while df is None:
            city, month, day = get_filters()
            df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        conf = query_user("\nWould you like to see the raw data? [Y/N]: ")
        if conf == "y":
            disp_raw_data(df)
        
        conf = query_user("\nWould you like to restart? [Y/N]: ")
        if conf == "n":
            break

if __name__ == "__main__":
	main()
