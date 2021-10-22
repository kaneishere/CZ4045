from collections import namedtuple
from enum import Enum
import pickle
import random
from typing import DefaultDict, List, Set
import warnings


class OPTION(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    STOP = -1

BusinessDetails = namedtuple('BusinessDetails', ['id', 'top_attributes', 'sentiment'])

def get_options(business_reviews: DefaultDict):
    options = set()
    for _, attributes in business_reviews.items():
        options.update(noun for noun, _ in attributes['nouns'][:10])
    return options


def validate(chosen, k):
    if chosen is None:
        return False
    if not chosen.isnumeric():
        print("Wrong input. Please enter a number.\n")
        return False

    chosen = int(chosen)
    if chosen < 1 or chosen > k + 1:
        print(
            f"Wrong input. Input range should be a number between 1 and {k}\n")
        return False
    return True


def show_options_and_get_input(options: Set[str], k: int = 5):
    options_to_show = random.sample(options, k)
    chosen=None
    while validate(chosen, k) is False:
        print("Please select an option\n")
        for option_number, attribute in enumerate(options_to_show, 1):
            print(f"{option_number}: {attribute}\n")
        print(f"{k+1}: Quit\n")
        chosen = input()

    chosen = int(chosen)    

    if chosen == k + 1:
        return (None, OPTION.STOP)
    return (options_to_show, chosen)

def get_businesses(attr_chosen: str, business_reviews: DefaultDict, cut_off:int = 10, top_n_nouns:int = 10) -> List[BusinessDetails]:
    business_reviews_list = list(business_reviews.items())
    business_reviews_list.sort(key=lambda review: review[1]['sentiment']['very_good'] * 5 \
                                       + review[1]['sentiment']['good'] * 1 \
                                       - review[1]['sentiment']['bad'] * 1 \
                                       - review[1]['sentiment']['very_bad'] * 5, reverse=True)

    ret = []
    for business_id, attr in business_reviews_list:
        if attr_chosen in set(noun for noun, _ in attr['nouns'][:top_n_nouns]):
            ret.append(BusinessDetails(business_id, attr['nouns'][:top_n_nouns], attr['sentiment']))
        if len(ret) == cut_off:
            break
    return ret

def main():
    warnings.filterwarnings("ignore")
    print("Initializing App...")
    with open('businesses.pickle', 'rb') as f:
        business_reviews = pickle.load(f)
    print("Loading options...")

    print("Initializing complete")
    random.seed(2021)
    options = get_options(business_reviews)

    cut_off = 10
    top_n_nouns = 10
    while (options_chosen := show_options_and_get_input(options))[1] is not OPTION.STOP: 
        chosen_option_number = options_chosen[1]
        attr_chosen = ""
        for idx, attr in enumerate(options_chosen[0], 1):
            if chosen_option_number == idx:
                attr_chosen = attr
            
        businesses = get_businesses(attr_chosen, business_reviews, cut_off=cut_off, top_n_nouns=top_n_nouns) 
        print(f"You chose {attr}\nHere are the top businesses that best match your chosen option."
              f"(Cut-off={cut_off})\n")
        print(f"Top businesses matching your search:\n")
        for business in businesses:
            print(f"Business ID: {business.id}\n")
            print(f"Top {top_n_nouns} words:\n")
            for idx, (noun, count) in enumerate(business.top_attributes):
                print(f"{idx}: {noun} ({count})\n")
            print(f"Reviews:\n")
            for sentiment, sentiment_score in business.sentiment.items():
                print(f"{sentiment} reviews: {sentiment_score}\n")

            print(f"\n\n\n")

    print("ok bye")

if __name__ == "__main__":
    main()
