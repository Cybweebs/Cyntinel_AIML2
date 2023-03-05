import pandas as pd
from datetime import datetime

def filter_main():

# Load the datasets
    users = pd.read_csv('../datasets/users.csv')
    swipes = pd.read_csv('../datasets/swipes.csv')

    # Merge the data
    data = pd.merge(swipes, users, left_on='p2', right_on='_id', how='right')

    # Calculate the number of likes given
    likes_given = data.groupby('p1')['first_type'].apply(lambda x: (x == 'LIKE').sum())

    # Calculate the number of dislikes given
    dislikes_given = data.groupby('p1')['first_type'].apply(lambda x: (x == 'DISLIKE').sum())

    # Calculate the number of likes received
    likes_received = data.groupby('p2')['second_type'].apply(lambda x: (x == 'LIKE').sum())

    # Calculate the number of dislikes received
    dislikes_received = data.groupby('p2')['second_type'].apply(lambda x: (x == 'DISLIKE').sum())

    # Add the calculated columns to the users dataframe
    users['likes_given'] = likes_given
    users['likes_received'] = likes_received
    users['dislikes_given'] = dislikes_given
    users['dislikes_received'] = dislikes_received

    # Add columns for the number of swipes for each user
    swipes_given = data.groupby('p1')['p2'].count()
    swipes_received = data.groupby('p2')['p1'].count()

    users['swipes_total'] = 0
    users['swipes_total'] = swipes_given + swipes_received

    users['matches'] = 0

    # Check for mutual likes and increment matches count if found
    if not data.empty and ((data['first_type'] == 'LIKE') & (data['second_type'] == 'LIKE')).any():
        matches = data[(data['first_type'] == 'LIKE') & (data['second_type'] == 'LIKE')]
        for index, row in matches.iterrows():
            users.loc[users['_id'] == row['p1'], 'matches'] += 1
            users.loc[users['_id'] == row['p2'], 'matches'] += 1

    # Convert timestamp columns to datetime format
    data['first_like_unlike_at'] = pd.to_datetime(data['first_like_unlike_at'])
    data['second_like_unlike_at'] = pd.to_datetime(data['second_like_unlike_at'])
    data['unmatch_on'] = pd.to_datetime(data['unmatch_on'])

    # Define a function to compare timestamps and return the latest one
    def get_latest_timestamp(row):
        timestamps = [row['first_like_unlike_at'], row['second_like_unlike_at'], row['unmatch_on']]
        timestamps = [ts for ts in timestamps if not pd.isnull(ts)]
        if timestamps:
            return max(timestamps)
        else:
            return pd.NaT

    # Apply the function to each row of the data dataframe
    data['latest_timestamp'] = data.apply(get_latest_timestamp, axis=1)

    # Group the data by p1 and p2, and get the max latest_timestamp for each group
    latest_timestamps_p1 = data.groupby('p1')['latest_timestamp'].max()
    latest_timestamps_p2 = data.groupby('p2')['latest_timestamp'].max()

    # Add the latest_timestamp column to the users dataframe
    users['latest_timestamp'] = users['_id'].map(lambda x: latest_timestamps_p1.get(x, latest_timestamps_p2.get(x)))

    # Convert the latest_timestamp column to a timezone-naive Timestamp object
    latest_timestamp_naive = users['latest_timestamp'].dt.tz_localize(None)

    # Calculate the current date
    now = datetime.now()

    # Calculate the time difference between the current date and the latest_timestamp column
    time_diff = now - latest_timestamp_naive

    # Check if the time difference is less than 7 days
    is_active = time_diff < pd.Timedelta(days=7)

    # Add the is_active column to the users dataframe
    users['is_active'] = is_active

    # Save the updated users dataframe to a new csv file
    users.to_csv('../datasets/filter.csv', index=False)

    return True
