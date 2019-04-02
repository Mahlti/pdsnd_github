import time
import pandas as pd
import numpy as np
from datetime import datetime as dt


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington).
    print('\nHello! Let\'s explore some US bikeshare data for 2017! Enter yes!')
    city = str(input("\n\t")).lower()

    # get user input for month (all, january, february, ... , june)
    print('\n Please, enter a month from January to June or just type "all"')
    month = str(input("\n\t")).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('\n Please, enter a day or just type "all"')
    day = str(input("\n\t")).lower()

    # verify users inputs
    city_list = ['chicago', 'new york city', 'washington']
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # verify "city" user's input
    while city not in city_list:

        print('\n\tPlease,enter a city name (Chicago, New York city, Washington): ')
        city = str(input("\n\t\t")).lower()

    # verify "month" user's inputs
    while month not in month_list:

        print('\n\tPlease, enter a month name (all, January, February, ... June):')
        month = str(input("\n\t\t")).lower()

    # verify "day" user's inpunt
    while day not in day_list:

        print('\n\tPlease, enter a day (all, Monday, Tuesday, ... Sunday):')
        day = str(input("\n\t\t")).lower()

    print('\033[0;046m-\033[1;m'*80)
    return city, month, day

def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    --------------------------------------
    --------------------------------------"""


    # create a datatime object from Start and End Time columns
    df = pd.read_csv(CITY_DATA[city])

    # create a datatime object from "Start" and "End Time" columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # new column for hours
    hours_list = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
                "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]
    df['Hour'] = pd.to_datetime(df['Start Time']).dt.hour
    df['Hour'] = df['Hour'].apply(lambda x: hours_list[x])

    # new column for days
    df['Day'] = df['Start Time'].dt.weekday_name

    # extract month from Start Time to create new columns
    months_list = ['January', 'February', 'March', 'April', 'May', 'June']
    df['Month'] = df['Start Time'].dt.month - 1
    df['Month'] = df['Month'].apply(lambda x: months_list[x])

    # Add new columns: start station and end station
    df['Start and End'] = '(Start) ' + df['Start Station'] + ' (End) ' + df['End Station'] # returns a deltaTime object

    # filter by month
    if month != 'all':
        # new dataframe - month
        df = df[df['Month'] == month.title()]

    # filter by day
    if day != 'all':
        # new dataframe -day
        df = df[df['Day'] == day.title()]

    return df

    # Add the functionality of displaying the raw data that was missing
def disp_raw_data(df):
    '''
    Displays the data used to compute the stats
    Input:
        the df with all the bikeshare data
    Returns:
       none
    '''
    # Raw data filters; omit irrelevant columns from visualization
    df = df.drop(['Month', 'Day'], axis = 1)
    row_index = 0
    see_data = input("\n Do you like to see rows of raw data used to compute the stats? yes/no \n").lower()
    while True:
        if see_data == 'no':
            return
        if see_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input("\n Would you like to see five more rows of raw data used to compute the stats? yes/no  \n").lower()

print('\033[0;046m-\033[1;m'*80)
def time_stats(df):

    """Displays statistics on the most frequent times of travel."""


    print('\nCalculating the most frequent times of travel...\n')

    # display the most common month
    print('\tMonth:', df['Month'].mode()[0])

    # display the most common day of week
    print('\tDay:', df['Day'].mode()[0])

    # display the most common start hour
    print('\tHour:', df['Hour'].mode()[0])

    print('\033[0;046m-\033[1;m'*80)

def station_stats(df):

    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the Most Popular stations and Trip...\n')

    # display most commonly used start station
    print('\tStart:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\tEnd:', df['End Station'].mode()[0])

    # display most frequent start and end stations
    stations = df['Start and End'].value_counts().index[0]
    times = df['Start and End'].value_counts().iloc[0]
    print('\tTrip: {} times of {}'.format(times,stations))

    print('\033[0;046m-\033[1;m'*80)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    # display total travel time - create a deltatime object from "End Time" and "Start time" dataframes
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #total travel time:sum
    total_time = df['Travel Time'].sum()
    # convert total to sec and to an integer
    sec = int(total_time.total_seconds())
    days = sec // 86400
    hours = (sec % 86400) // 3600
    min = ((sec % 86400) % 3600) // 60
    sec = ((sec % 86400) % 3600) % 60
    print('\n\tTotal: {} days {} hours {} min {} sec'.format(days, hours, min, sec))

    # display mean travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    mean_time = df['Travel Time'].mean()
    sec = int(mean_time.total_seconds())
    days = sec // 86400
    hours = (sec % 86400) // 3600
    min = ((sec % 86400) % 3600) // 60
    sec = ((sec % 86400) % 3600) % 60
    print('\tMean: {} days {} hours {} min {} sec'.format(days, hours, min, sec))

    print('\033[0;046m-\033[1;m'*80)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    # Display counts of user types
    print('\n\tUser Type:\n')
    df_User_Type = df['User Type'].value_counts()

    # convert df to string, remove all '\n' in the string, and insert a tab for display
    print('\t' + df_User_Type.to_string().replace('\n', '\n\t'))

    print('\033[1;34m-\033[1;m'*40)

    # Display counts of gender
    # Take into account that file washington.csv doesn't provide gender data
    try:

        df_Gender_Type = df['Gender'].value_counts()
        # Display counts of gender
        print('\n\tGender:\n')

        # convert df to string, remove all '\n' in the string, and insert a tab for display
        print('\t' + df_Gender_Type.to_string().replace('\n', '\n\t'))

        print('\033[1;34m-\033[1;m'*40)

    # create an exception to avoid errors and to continue wt the code
    except Exception:
        pass

    # Display earliest, most recent, and most common year of birth
    # the file washington.csv doesn't provide "Brith Year" data
    try:

        # Display earliest, most recent, and most common year of birth
        current_year = dt.now().year
        age = current_year - df['Birth Year'].mode()[0]
        print('\n\tMost common age:', int(age))

        age = current_year - df['Birth Year'].min()
        print('\tOldest: ' + str(int(age)))

        age = current_year - df['Birth Year'].max()
        print('\tYoungest: ' + str(int(age)))

        age = current_year - df['Birth Year'].mean()
        print('\tAverage: ' + str(int(age)))

        print('\033[0;046m-\033[1;m'*80)

    #create an exception to avoid errors and to continue wt the code
    except Exception:
        pass

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        print('\n\nWould you like to restart? enter yes/no.')
        restart = input('\n\t')
        if restart.lower() != 'yes':
            print()
            break

if __name__ == "__main__":

    main()
