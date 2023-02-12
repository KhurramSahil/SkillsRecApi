from fastapi import FastAPI
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

app = FastAPI()


@app.get("/")
def get_top_taskers():
    tasker_df = pd.read_csv("tasker_df.csv")
    # Droping unnecossory features
    new_tasker_df = tasker_df[
        ['UserId', 'Email', 'UserName', 'FirstName', 'LastName', 'TotalReviews', 'AvgReviews', 'Skills']]
    # Split the skills column by comma
    Skills = new_tasker_df["Skills"].str.split(",", expand=True)

    # Give the columns meaningful names
    Skills.columns = [f"Skill_{i + 1}" for i in range(Skills.shape[1])]

    # Concatenate the original DataFrame with the new skills DataFrame
    new_tasker_df_exp = pd.concat([new_tasker_df, Skills], axis=1)

    # Drop the original skills column
    new_tasker_df_exp = new_tasker_df_exp.drop("Skills", axis=1)
    new_tasker_df_exp[['Skill_1', 'Skill_2', 'Skill_3', 'Skill_4', 'Skill_5', 'Skill_6', 'Skill_7']] = \
    new_tasker_df_exp[['Skill_1', 'Skill_2', 'Skill_3', 'Skill_4', 'Skill_5', 'Skill_6', 'Skill_7']].fillna('')
    v = new_tasker_df_exp['TotalReviews']
    R = new_tasker_df_exp['AvgReviews']
    C = new_tasker_df_exp['AvgReviews'].mean()
    m = new_tasker_df_exp['TotalReviews'] >= 5
    new_tasker_df_exp['weighted_average'] = ((R * v) + (C * m)) / (v + m)

    weighted_average_result_df = new_tasker_df_exp[new_tasker_df_exp['TotalReviews'] >= 20].sort_values(
        'weighted_average', ascending=False)
    # Create a new column with first and last name concatenated
    weighted_average_result_df['FullName'] = weighted_average_result_df.apply(
        lambda x: x['FirstName'] + ' ' + x['LastName'], axis=1)

    top_taskers = weighted_average_result_df[
        ['UserId', 'FullName', 'TotalReviews', 'AvgReviews', 'Skill_1', 'Skill_2', 'Skill_3', 'Skill_4', 'Skill_5',
         'Skill_6', 'Skill_7']].head(10)

    result = []
    for index, row in top_taskers.iterrows():
        user_details = {}
        user_details['UserId'] = row['UserId']
        user_details['FullName'] = row['FullName']
        user_details['TotalReview'] = row['TotalReviews']
        user_details['AvgReview'] = row['AvgReviews']
        skills = [skill for skill in
                  row[['Skill_1', 'Skill_2', 'Skill_3', 'Skill_4', 'Skill_5', 'Skill_6', 'Skill_7']].tolist() if skill]
        user_details['Skills'] = skills
        result.append(user_details)

    return result

