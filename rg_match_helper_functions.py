import numpy as np
import pandas as pd
import random
from random import sample
from RothPeranson import MatchController


def remove_same_institution(encode_article_coi, encode_panelist_coi, article_rank_order, reviewer_rank_order):
    #current can only handle single COI per article, will need to expand this to handle multiple COI

    for article, reviewers in article_rank_order.items():
        for r in reviewers:
            if encode_article_coi[article] == encode_panelist_coi[r]:
                article_rank_order[article].remove(r)
                reviewer_rank_order[r].remove(article)
    return

def create_rank_order_lists(article_topics, reviewer_dict):
    """
    input arguments:
        article_topics: dict, article name to the article topic
        reviewer_dict: dict, reviewer name to array of welcomed topics

    create_rank_order_lists() outputs two NumPy arrays of x and y values that creates the circle

    output:
        x, y

        article_rank_order is a dict that contains an article (key) with an array of potential viewers (value) 
        reviewer_rank_order is a dict that contains a reviewer (key) with an array of potential articles (value) 
    """

    article_rank_order = {}
    for article, topic in article_topics.items():
        article_rank_order[article] = [reviewer for reviewer, can_review in reviewer_dict.items() if topic in can_review]
        random.shuffle(article_rank_order[article])
    # article_rank_order

    reviewer_rank_order = {}
    for reviewer, can_review in reviewer_dict.items():
        potential_topics = []
        for topic in can_review:
            potential_topics += [article for article, val in article_topics.items() if topic == val]
        reviewer_rank_order[reviewer] = potential_topics
        random.shuffle(reviewer_rank_order[reviewer])

    return article_rank_order, reviewer_rank_order

def match_articles_to_reviewers(article_rank_order, reviewer_rank_order, reviewer_places, MatchController):
    """
    input arguments:
        article_topics: dict, article name to the article topic
        reviewer_dict: dict, reviewer name to array of welcomed topics

    create_rank_order_lists() outputs two NumPy arrays of x and y values that creates the circle

    output:
        x, y

        article_rank_order is a dict that contains an article (key) with an array of potential viewers (value) 
        reviewer_rank_order is a dict that contains a reviewer (key) with an array of potential articles (value) 
    """
    article_rol = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in article_rank_order.items() ]))
    reviewer_rol = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in reviewer_rank_order.items() ]))
    # reviewer_places = pd.DataFrame(len(reviewer_rank_order)*[reviewer_article_limit],reviewer_rank_order.keys(), columns = ['places'])

    match = MatchController(reviewer_rol, article_rol, reviewer_places)
    match.start_match()
    results = match.results_dict()

    return results

def remove_matched_pairs(match_results, article_rank_order, reviewer_rank_order):
    """
    input arguments:
        article_rank_order: dict, article (key) with an array of potential viewers (value)
        reviewer_rank_order: dict, reviewer name to array of welcomed topics

    create_rank_order_lists() outputs two NumPy arrays of x and y values that creates the circle

    output:
        x, y

        article_rank_order is a dict that contains an article (key) with an array of potential viewers (value) 
        reviewer_rank_order is a dict that contains a reviewer (key) with an array of potential articles (value) 
    """
    for article, reviewer in match_results.items():
        try:
            article_rank_order[article].remove(reviewer)
            reviewer_rank_order[reviewer].remove(article)
        except:
            continue

#If we need to update the article limits, but currently this is causing more bugs than benefits
def update_article_limits(reviewer_places, results):
    for i in range(0, len(reviewer_places.index)):
      reviewer_name = reviewer_places.index[i]
      reviewer_places.places[i] = reviewer_places.places[i] - sum(value == reviewer_name for value in results.values())
    return reviewer_places