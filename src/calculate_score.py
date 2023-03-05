import pandas as pd


def calculate_score(row):
    weights = {
        'verified': 10,
        'likes': 10,
        'matches': 20,
        'subscription': 10,
        'likes_given_received_ratio': 10,
        'likes_dislikes_given_ratio': 10,
        'likes_dislikes_received_ratio': 10,
        'profile_completion': 20,
    }

    score = 0
    if row['is_verified'] == True:
        score += weights['verified']  # 10
    if row['likes_received'] > 30:
        score += weights['likes']  # 20
    if row['is_subscribed'] == True:
        score += weights['subscription']  # 10

    try:
        if (row['likes_given'] / row['likes_received']) > 1.0:
            score += weights['likes_given_received_ratio']  # 20
    except ZeroDivisionError:
        score += 0

    try:
        if (row['likes_given'] / row['dislikes_given']) > 0.5:
            score += weights['likes_dislikes_given_ratio']  # 10
    except ZeroDivisionError:
        score += 0

    try:
        if (row['likes_received'] / row['dislikes_received']) > 0.5:
            score += weights['likes_dislikes_received_ratio']  # 10
    except ZeroDivisionError:
        score += 0

    # New scoring rules based on parameters
    filled_fields = sum([1 for val in [row['bio'], row['college'], row['country'], row['dob'], row['gender'],
                        row['height'], row['interests'], row['name'], row['what_to_find'], row['who_to_date']] if val])

    if filled_fields >= 9:
        # 10, 1 or less fields are missing
        score += weights['profile_completion']
    elif filled_fields >= 7:
        score -= 10  # 4 or less fields are missing
    else:
        score -= 10  # else


    return round(score, 2)


def score_main():

    # Read the CSV file into a Pandas dataframe
    df = pd.read_csv('../datasets/filter.csv')

    # Add a new column to the dataframe with the calculated score for each row
    df['score'] = df.apply(calculate_score, axis=1)

    # Exclude users with empty name or score
    df = df.dropna(subset=['name', 'score'])

    # Convert the score to a scale of 0-100
    df['score'] = df['score']

    # Save the output to a new CSV file
    df[['_id', 'score']].to_csv('scores.csv', index=False)

    return True
