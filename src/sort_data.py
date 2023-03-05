import pandas as pd
import datetime
import json

def sort_main(id_value):
# Load users.csv into DataFrame
    users = pd.read_csv('../datasets/filter.csv')
    scores = pd.read_csv('scores.csv')

    users = pd.merge(users, scores, on='_id')

    # Define mapping of who_to_date and what_to_find
    who_to_date_map = {'F': 'Female', 'M': 'Male', 'A': 'Anyone'}

    # Select the row to sort by
    user = users.loc[users['_id'] == id_value]

    # Extract the who_to_date value from the user row
    who_to_date = user['who_to_date'].values[0]

    # Filter users based on who_to_date value and match with gender
    users_filtered = users.loc[((users['gender'] == who_to_date) & (users['who_to_date'] == user['gender'].values[0]) & (users['is_subscribed'] == True) & (users['is_active'] == True)) | ((users['gender'] == who_to_date) & (users['who_to_date'] == user['gender'].values[0]) & (users['is_subscribed'] == False) & (users['is_active'] == True))]
    
    # Sort and select the latest 100 users based on given criteria
    score = user['score'].values[0]
    if score > 60:
        users_sorted = users_filtered.loc[(users_filtered['score'] >= score - 30) & (users_filtered['score'] <= score + 30)]
    else:
        users_sorted = users_filtered.loc[(users_filtered['score'] >= score - 10) & (users_filtered['score'] <= score + 10)]

    # Split users into new and old based on their createdAt timestamp
    today = datetime.datetime.now(datetime.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    users_sorted['createdAt'] = pd.to_datetime(users_sorted['createdAt']).dt.tz_convert('UTC')

    new_users = users_sorted[users_sorted['createdAt'] >= today - datetime.timedelta(days=14)].iloc[:600]
    old_users = users_sorted[users_sorted['createdAt'] < today - datetime.timedelta(days=14)].iloc[:400]

    # Combine new and old users and sort by createdAt, matches, and score
    users_latest = pd.concat([new_users, old_users]).sort_values(by=['createdAt', 'matches', 'score'], ascending=[False, True, False])

    # Map who_to_date values
    users_latest['who_to_date'] = users_latest['who_to_date'].map(who_to_date_map)

    # Select only the required columns
    users_latest = users_latest[['_id', 'createdAt', 'name', 'gender', 'who_to_date', 'is_subscribed', 'matches', 'score']]
    users_selected = users_latest.sample(n=10)

    # Print the sorted DataFrame
    users_selected_json = users_selected.to_json(orient='records')
    users_selected_json = json.loads(users_selected_json)
    return users_selected_json

