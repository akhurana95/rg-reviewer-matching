import numpy as np
import pandas as pd
import random
from random import sample
import rg_match_helper_functions as rg
import RothPeranson as rp

# import gspread
# from gspread_dataframe import get_as_dataframe, set_with_dataframe
# from google.colab import auth
# auth.authenticate_user()  # verify your account to read files which you have access to. Make sure you have permission to read the file!
# from oauth2client.client import GoogleCredentials
# gc = gspread.authorize(GoogleCredentials.get_application_default()) 

#A few variables that will need to be inputted into the algorithm to do the work
# article_csv_file
# panelist_csv_file #might be taken from google form instead



#--------------------
#MASTER FUNCTION TO UPLOAD TO STREAMLIT: Inputs will be two CSV files (reviewer and panelist) as wel as number_of_reviews
#--------------------

def master_rg_match(speciality_to_match, article_csv, panelist_csv, number_of_reviews):
  #import csv files into DataFrames
  article_df = pd.read_csv(article_csv)
  panelist_df = pd.read_csv(panelist_csv)

  #post process panelist df
  panelist_df = panelist_df[panelist_df['Which subspeciality are you a panelist for?'] == speciality_to_match].replace('',np.nan)
  panelist_df = panelist_df.dropna(axis='columns')
  panelist_df.columns = ['Timestamp', 'Reviewer', 'Subspeciality','Topic','Institution','coi_dict']
  panelist_df.coi_dict = panelist_df.coi_dict.astype(float)
  panelist_df.Topic = [topic.split(', ') for topic in panelist_df.Topic]
  panelist_df = panelist_df.reset_index()  

  #will need to change code to handle variable column names based on the Streamlit input
  #will need to have a master CSV file that includes all coded topics

  #create dictionaries of articles and reviewers with their topics
  panelist_topic_dict = {panelist_df.Reviewer[i]:panelist_df.Topic[i]for i in range(0, len(panelist_df.Reviewer))}
  #article topic dictionary is already encoded in this example
  article_topic_dict = {article_df.TITLE[i]:article_df.ClassID[i] for i in range(0,len(article_df.TITLE))}

  #encode and shuffle order of preference for panelists
  encode_topics_from_google_form = {
    'Artificial intelligence (AI)': 1,
    'Annual Report': 2,
    'Image segmentation and processing': 3,
    'Operations/Practice improvement': 4,
    'Presentation/Teaching': 5,
    'Reporting/Report analysis/Follow-up': 6,
    'Research': 7,
    'Security': 8,
    'Standards/Coding/Ontologies': 9,
    'UI/UX/Productivity': 10,
    'Visualization/3D Printing/Augmented Reality/Virtual Reality' : 11
  }
  for key,val in panelist_topic_dict.items():
    temp_array = [encode_topics_from_google_form[value] for value in val]
    random.shuffle(temp_array)
    panelist_topic_dict[key] = temp_array

  #create pseudo-rank order lists
  article_rank_order, panelist_rank_order = rg.create_rank_order_lists(article_topic_dict, panelist_topic_dict)

  #assemble conflict of interest dictionaries to remove pairs from same institution
  panelist_coi_dict = {panelist_df.Reviewer[i]:panelist_df.coi_dict[i]for i in range(0, len(panelist_df.Reviewer))}
  article_coi_dict = {article_df.TITLE[i]:article_df.coi_dict[i] for i in range(0,len(article_df.TITLE))}

  #remove any pairs with coi
  rg.remove_same_institution(article_coi_dict, panelist_coi_dict, article_rank_order, panelist_rank_order)

  #set up the match process
  reviewer_article_limit = round(len(article_rank_order)/len(panelist_rank_order))
  #number of 'positions' for each panelist that is acting as the 'institution'
  reviewer_places = pd.DataFrame(len(panelist_rank_order)*[reviewer_article_limit],panelist_rank_order.keys(), columns = ['places'])
  
  #assemble final dataframe with matches
  final_matches = []
  for i in range(0, number_of_reviews):
    results = rg.match_articles_to_reviewers(article_rank_order, panelist_rank_order, reviewer_places, rp.MatchController)
    final_matches.append(results)
    rg.remove_matched_pairs(results, article_rank_order, panelist_rank_order)

  matched_df = pd.DataFrame(final_matches).transpose()
  matched_csv = matched_df.to_csv('final_rg_matches_{}.csv'.format(speciality_to_match))

  return matched_csv




if __name__ == '__main__':
  speciality_to_match = 'Informatics'
  article_csv = 'sample_informatics_articles.csv'
  panelist_csv = 'panelist_google_form_0329.csv'
  number_of_reviews = 3

  master_rg_match(speciality_to_match, article_csv, panelist_csv, number_of_reviews)