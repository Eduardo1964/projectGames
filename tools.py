import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

def load_csv(details):

    filepath = f'{details['folder']}/{details['platform']}_game_reviews.csv'
    df = pd.read_csv(filepath)

    return df

def correct_data(df):
    corrected_rows = []

    for _, row in df.iterrows():
        review_text = row["Review"]
        game_title = row.get("game", "Unknown")  # Keep the original game title

        # Updated regex to capture multiple reviews within one cell
        pattern = r"(\d{2,3})\s+([^\n]+)\n\s+([A-Za-z]+ \d{1,2}, \d{4})\n\s+(.+?)(?=\n\s*\d{2,3}\s+[^\n]+\n\s+[A-Za-z]+ \d{1,2}, \d{4}|\Z)"
        matches = re.findall(pattern, review_text, re.DOTALL)

        if matches:
            for match in matches:
                score, publication, date, review = match
                corrected_rows.append({
                    "game": game_title,  # Assign the game title
                    "Score": int(score),
                    "Publication": publication.strip(),
                    "Date": date.strip(),
                    "Review": review.strip(),
                    "Platform": row.get("Platform", "Unknown")  # Keep original platform if available
                })
        else:
            # Keep the original row if no extra reviews found
            corrected_rows.append(row.to_dict())

    return pd.DataFrame(corrected_rows)