'''Version 0.35'''
import json
import os
import nltk
from nltk.corpus import stopwords
from utilities.util import *
from collections import Counter
import re
import spacy
import time
from difflib import SequenceMatcher
nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords')
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Globals
YEAR = ''
STOP_WORDS = ["goldenglobes", "golden globes", "Golden", "Hollywood", "RT", "rt", "film", "best", "actress", "actor", "goldenglobe", "musical", "picture", "motion"]
TWEETS_DICT = {}
TWEETS_LIST = []
TWEETS_CLEAN_LIST = []
TWEETS_FOR_AWARDS = []
NAME_DICT = {}
DEFAULT_YEAR = '2013'
AWARD_TWEETS = {}
PRESENTER_TWEETS = []
PRESENTER_AWARD_TWEETS = {}
HOST_TWEETS = []
NOMINEE_TWEETS = []
PERSON_WORDS = ['actor', 'actress', 'director', 'screenplay', 'cecil']
TOKEN_AWARD_1 = [0, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 1, 1, 2, 2, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 4]
TOKEN_AWARD_2 = [4, 6, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 2, 2, 4, 6, 3, 4, 4, 4, 4, 4, 4, 4, 4, 1]
# Regexpr Patterns
award_pattern_1 = re.compile('Best ([A-z\s-]+)[A-Z][a-z]*[^A-z]')
award_pattern_2 = re.compile(".*^((?!(goes|but|is|in|by an|a)).)*$")
presenter_pattern = re.compile('present[^a][\w]*\s([\w]+\s){1,5}')
presenter_pattern_2 = re.compile(r"^(?=.*\b(present.*)\b).*$")
nominee_pattern = re.compile(r"^(?=.*\b(nomin.*)\b).*$")
award_type_pattern = re.compile(r"^(?=.*\b(drama|comedy|musical|animated|foreign|screenplay|original|song|score)\b)(?=.*\b(motion|picture|movie|tv|television|series|limited)\b).*$")

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 
                        'best motion picture - drama', 
                        'best performance by an actress in a motion picture - drama', 
                        'best performance by an actor in a motion picture - drama', 
                        'best motion picture - comedy or musical', 
                        'best performance by an actress in a motion picture - comedy or musical', 
                        'best performance by an actor in a motion picture - comedy or musical', 
                        'best animated feature film', 
                        'best foreign language film', 
                        'best performance by an actress in a supporting role in a motion picture', 
                        'best performance by an actor in a supporting role in a motion picture', 
                        'best director - motion picture', 
                        'best screenplay - motion picture', 
                        'best original score - motion picture', 
                        'best original song - motion picture', 
                        'best television series - drama', 
                        'best performance by an actress in a television series - drama', 
                        'best performance by an actor in a television series - drama', 
                        'best television series - comedy or musical', 
                        'best performance by an actress in a television series - comedy or musical', 
                        'best performance by an actor in a television series - comedy or musical', 
                        'best mini-series or motion picture made for television', 
                        'best performance by an actress in a mini-series or motion picture made for television', 
                        'best performance by an actor in a mini-series or motion picture made for television', 
                        'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 
                        'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 
                        'best motion picture - musical or comedy', 
                        'best performance by an actress in a motion picture - drama', 
                        'best performance by an actor in a motion picture - drama', 
                        'best performance by an actress in a motion picture - musical or comedy', 
                        'best performance by an actor in a motion picture - musical or comedy', 
                        'best performance by an actress in a supporting role in any motion picture', 
                        'best performance by an actor in a supporting role in any motion picture', 
                        'best director - motion picture', 
                        'best screenplay - motion picture', 
                        'best motion picture - animated', 
                        'best motion picture - foreign language', 
                        'best original score - motion picture', 
                        'best original song - motion picture', 
                        'best television series - drama', 
                        'best television series - musical or comedy', 
                        'best television limited series or motion picture made for television', 
                        'best performance by an actress in a limited series or a motion picture made for television', 
                        'best performance by an actor in a limited series or a motion picture made for television', 
                        'best performance by an actress in a television series - drama', 
                        'best performance by an actor in a television series - drama', 
                        'best performance by an actress in a television series - musical or comedy', 
                        'best performance by an actor in a television series - musical or comedy', 
                        'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 
                        'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 
                        'cecil b. demille award']

VERB_PREFIXES = {
    "wins": 10,
    "win": 5,
    "winning": 3,
    "will win": 1,
    "receives": 5,
    "receive": 5,
    "taking home": 3,
    "take home": 3,
    "takes home": 5,
    "will present": 5,
    "is nominated for": 3,
    "presents": 3,
    "nominated for": 3,
    "to win": 5
}

# Split Award Tweets from TWEETS
def split_award_tweets():
    global AWARD_TWEETS
    award_tweets = [award_pattern_1.search(tweet).group(0)[:-1] for tweet in TWEETS_LIST if award_pattern_1.search(tweet)]
    award_tweets_2 = [award_pattern_2.search(tweet).group(0)[:-1] for tweet in TWEETS_LIST if award_pattern_2.search(tweet)]
    award_tweets_3 = [award_type_pattern.search(tweet).group(0)[:-1] for tweet in TWEETS_LIST if award_type_pattern.search(tweet)]
    tweets = set(award_tweets + award_tweets_2 + award_tweets_3)
    # CECIL AWARD
    cecil_award_tweets = list(filter(lambda x : ('cecil' in x.lower()), tweets))
    AWARD_TWEETS["cecil"] = cecil_award_tweets
    # BEST ACTRESS
    best_actress_tweets = list(filter(lambda x : ('actress' in x.lower()), tweets))
    AWARD_TWEETS["actress"] = best_actress_tweets
    # BEST ACTOR
    best_actor_tweets = list(filter(lambda x : ('actor' in x.lower()), tweets))
    AWARD_TWEETS["actor"] = best_actor_tweets
    # BEST DRAMA | DIRECTOR | SCREENPLAY | ANIMATED | COMEDY, MUSICAL | FOREIGN | SCORE | SONG
    best_drama_tweets = list(filter(lambda x : ('drama' in x.lower()), tweets))
    AWARD_TWEETS["drama"] = best_drama_tweets
    best_director_tweets = list(filter(lambda x : ('director' in x.lower()), tweets))
    AWARD_TWEETS["director"] = best_director_tweets
    best_screenplay_tweets = list(filter(lambda x : ('screenplay' in x.lower()), tweets))
    AWARD_TWEETS["screenplay"] = best_screenplay_tweets
    best_animated_tweets = list(filter(lambda x : ('animated' in x.lower()), tweets))
    AWARD_TWEETS["animated"] = best_animated_tweets
    best_comedy_tweets = list(filter(lambda x : ('comedy' in x or 'musical' in x.lower()), tweets))
    AWARD_TWEETS["comedy"] = best_comedy_tweets
    best_foreign_tweets = list(filter(lambda x : ('foreign' in x.lower()), tweets))
    AWARD_TWEETS["foreign"] = best_foreign_tweets
    best_score_tweets = list(filter(lambda x : ('score' in x.lower()), tweets))
    AWARD_TWEETS["score"] = best_score_tweets
    best_song_tweets = list(filter(lambda x : ('song' in x.lower()), tweets))
    AWARD_TWEETS["song"] = best_song_tweets
    best_miniseries_tweets = list(filter(lambda x : ('mini-series' in x.lower()), tweets))
    AWARD_TWEETS["mini-series"] = best_miniseries_tweets
    AWARD_TWEETS["series"] = best_miniseries_tweets

# Split Presenter Tweets from TWEETS
def split_presenter_tweets():
    global PRESENTER_TWEETS
    global PRESENTER_AWARD_TWEETS
    presenter_tweets = [presenter_pattern.search(tweet).group(0)[:-1] for tweet in TWEETS_LIST if presenter_pattern.search(tweet)]
    presenter_tweets_2 = [presenter_pattern_2.search(tweet).group(0)[:-1] for tweet in TWEETS_LIST if presenter_pattern_2.search(tweet)]
    PRESENTER_TWEETS = set(presenter_tweets + presenter_tweets_2)
    presenter_award_tweets = [award_pattern_1.search(tweet).group(0)[:-1] for tweet in PRESENTER_TWEETS if award_pattern_1.search(tweet)]
    presenter_award_tweets_2 = [award_pattern_1.search(tweet).group(0)[:-1] for tweet in PRESENTER_TWEETS if award_pattern_1.search(tweet)]
    tweets = set(presenter_award_tweets + presenter_award_tweets_2)
    # CECIL AWARD
    cecil_award_tweets = list(filter(lambda x : ('cecil' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["cecil"] = cecil_award_tweets
    # BEST ACTRESS
    best_actress_tweets = list(filter(lambda x : ('actress' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["actress"] = best_actress_tweets
    # BEST ACTOR
    best_actor_tweets = list(filter(lambda x : ('actor' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["actor"] = best_actor_tweets
    # BEST DRAMA | DIRECTOR | SCREENPLAY | ANIMATED | COMEDY, MUSICAL | FOREIGN | SCORE | SONG
    best_drama_tweets = list(filter(lambda x : ('drama' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["drama"] = best_drama_tweets
    best_director_tweets = list(filter(lambda x : ('director' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["director"] = best_director_tweets
    best_screenplay_tweets = list(filter(lambda x : ('screenplay' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["screenplay"] = best_screenplay_tweets
    best_animated_tweets = list(filter(lambda x : ('animated' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["animated"] = best_animated_tweets
    best_comedy_tweets = list(filter(lambda x : ('comedy' in x or 'musical' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["comedy"] = best_comedy_tweets
    best_foreign_tweets = list(filter(lambda x : ('foreign' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["foreign"] = best_foreign_tweets
    best_score_tweets = list(filter(lambda x : ('score' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["score"] = best_score_tweets
    best_song_tweets = list(filter(lambda x : ('song' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["song"] = best_song_tweets
    best_miniseries_tweets = list(filter(lambda x : ('mini-series' in x.lower()), tweets))
    PRESENTER_AWARD_TWEETS["mini-series"] = best_miniseries_tweets
    PRESENTER_AWARD_TWEETS["series"] = best_miniseries_tweets

# Split Nominee Tweeets from TWEETS
def split_nominee_tweets():
    global NOMINEE_TWEETS
    nominee_tweets = [nominee_pattern.search(tweet).group(0)[:-1] for tweet in TWEETS_LIST if nominee_pattern.search(tweet)]
    nominee_tweets_2 = list(filter(lambda x : ('nominee' in x.lower() or 'nominated' in x.lower() or 'nominate' in x.lower() or 'nominations' in x.lower()), TWEETS_LIST))
    NOMINEE_TWEETS = set(nominee_tweets + nominee_tweets_2)

# spaCy entity recognition
def spacy_tag_entity(tweet: str):
    doc = nlp(tweet)
    # returns [(entity, label)] for each entity in the tweet
    # e.g. [("European", "NORP"), ("Google", "ORG"), ("5.1 billion", "MONEY"), ("Wednesday", "DATE")]
    return [(X.text, X.label_) for X in doc.ents]

# spaCy POS tagging
def spacy_tag_speech(tweet: str):
    doc = nlp(tweet)
    # # This return statement is the more detailed one
    # # returns [(word, pos, detailed pos)] for each word in the tweet
    # return [(token.text, token.pos_, token.tag_) for token in doc]
    # returns [(word, part of speech)] for each word in the tweet
    return [(token.text, token.pos_) for token in doc]

# Extract PERSONs from Entity list
def get_people_from_ents(entities):
    people = []
    for ent in entities:
        if ent[1] == 'PERSON' and not any(w in ent[0].split() for w in STOP_WORDS):
            people.append(ent[0].lower())
    return people

# Extract PROPNs from POS list
def get_proper_nouns(tags):
    proper_nouns = []
    for tag in tags:
        if tag[1] == "PROPN" and not any(w in tag[0].lower().split() for w in STOP_WORDS):
            proper_nouns.append(tag[0].lower())
    return proper_nouns

# Extract NOUNs from POS list
def get_nouns(tags):
    nouns = []
    for tag in tags:
        if tag[1] == "NOUN" and not any(w in tag[0].lower().split() for w in STOP_WORDS):
            nouns.append(tag[0].lower())

# Load and Extract Data
def extract_data(year):
    global TWEETS_DICT, TWEETS_LIST, TWEETS_FOR_AWARDS
    # Get path to JSON of specified year
    src_path = 'gg' + str(year) + '.json'
    # Nested Dict for tweets for current year
    TWEETS_DICT[str(year)] = {} 
    # Open file
    with open(src_path, "r") as read_file:
        # Load JSON
        TWEETS = json.load(read_file)
    # Light preprocessing
    for tweet in TWEETS:
        TWEETS_LIST.append(tweet["text"])
        # Dict for individual tweets
        tweet_dict  = {"text" : [], "clean_text" : [], "entities" : []}
        # Get unclean text
        tweet_dict["text"] = tweet["text"]
        # Light processing
        clean_text = re.sub(r'[^\w\s]', '', tweet["text"])
        re.sub(r'http\S+', '', clean_text)
        clean_text.replace('\d+', '')
        tweet_dict["clean_text"] = clean_text 
        # Set entities to None for now
        tweet_dict["entities"] = None
        # Add to TWEETS_DICT
        TWEETS_DICT[str(year)][tweet["text"]] = tweet_dict
        TWEETS_FOR_AWARDS.append(remove_punc_awards(tweet["text"].lower().strip().split()))

# Remove Stopwords
def remove_stopwords_str(words, stop_words = []):
    if stop_words == []:
        stop_words = set(stopwords.words('english'))
        list_words = words.split()
        new_words = list(filter(lambda x: (x not in stop_words), list_words))
        new_words = " ".join(new_words)
    else:
        list_words = words.split()
        new_words = list(filter(lambda x: (x not in stop_words), list_words))
        new_words = " ".join(new_words)
    return new_words

def remove_stopwords_lst(words, stop_words = []):
    if stop_words != []:
        return list(filter(lambda x: (x not in stop_words), words))
    else:
        stop_words = set(stopwords.words('english'))
        return list(filter(lambda x: (x not in stop_words), words))

# Get Best Dressed
def get_best_dressed(year):
    # Get Keywords
    keywords = BEST_DRESS_KEYWORDS.split(";")
    # List of People
    people = []
    # Loop through tweets
    for tweet in TWEETS_LIST:
        # get clean text
        clean_text = TWEETS_DICT[str(year)][tweet]["clean_text"]
        # Check for keywords
        if any(word in clean_text.lower() for word in keywords):
            # If so, get ents
            entities = spacy_tag_entity(clean_text)
            # Get persons
            persons = get_people_from_ents(entities)
            # Add to people
            people = people + persons
    
    people_counter = Counter(people)
    best_dressed = people_counter.most_common(1)[0][0]
    # print(f"Best dressed was {best_dressed}")
    print("Best Dressed:", best_dressed)
    return best_dressed

# Get Worst Dressed
def get_worst_dressed(year):
    # Get keywords
    keywords = WORST_DRESS_KEYWORDS.split(";")
    # List of People
    people = []
    # Loop through tweets
    for tweet in TWEETS_LIST:
        # get clean text
        clean_text = TWEETS_DICT[str(year)][tweet]["clean_text"]
        # Check for keywords
        if any(word in clean_text.lower() for word in keywords):
            # If so, get ents
            entities = spacy_tag_entity(clean_text)
            # Get persons
            persons = get_people_from_ents(entities)
            # Add to people
            people = people + persons
    
    people_counter = Counter(people)
    worst_dressed = people_counter.most_common(1)[0][0]
    print("Worst Dressed:", worst_dressed)
    # print(f"Worst dressed is {worst_dressed}")
    return worst_dressed

# Get Sentiments

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    with open("results" + str(year) + ".json", "r") as f:
        d = json.load(f)
    awards = d["Host"]
    return awards

def prep_hosts(year):
    #global HOST_TWEETS, TWEETS_LIST
    # Get Relevant Keywords
    keywords = HOST_KEYWORDS.split(";")
    badwords = ["should host", "next year", "could host", "next", "should've", "could've", "could have", "should have"]
    # if year == '2013':
    #     stop = 15000
    # else:
    #     stop = -1
    # # List of people
    people = []
    # Loop through tweets
    for tweet in TWEETS_LIST:#[0:stop]:
        # Get text
        clean_text = TWEETS_DICT[str(year)][tweet]["clean_text"]
        # Check for bad words
        if any(word in clean_text.lower() for word in badwords):
            continue
        # Check for keywords
        elif any(word in clean_text.lower() for word in keywords):#'host' in clean_text: #any(word in tweet for word in keywords):
            # If so, 
            entities = spacy_tag_entity(clean_text)
            #print(entities)
            persons = get_people_from_ents(entities)
            #print(persons)
            people = people + persons
            #print(people)

        else:
            # If not, skip
            continue

    people_counter = Counter(people)
    host = [i[0] for i in people_counter.most_common(2)]
    # Your code here
    return host

# Helpers for get_awards

def remove_punc_awards(words):
    new_words = []
    for word in words:
        if word[0] == "#":
            continue
        if len(word) >= 3 and word[:3] == "htt":
            continue
        new_word = re.sub(r'[^\w\s]', '', (word))
        if new_word != '':
            new_words.append(new_word)
    return new_words

def verb_prefix(tweet):
    tweet_lsts = []
    for verbs in VERB_PREFIXES:
        split_verbs = verbs.split()
        n = len(split_verbs)
        indices = [i for (i, w) in enumerate(tweet) if tweet[i:i + n] == split_verbs]
        if indices:
            tweet_lsts.append((tweet[indices[-1] + n:], VERB_PREFIXES[verbs]))
    return tweet_lsts

def tweet_lst_to_candidate(cand, val):
    if cand and (cand[0] == "the" or cand[0] == "a" or cand[0] == "an"):
        cand = cand[1:]
    if len(cand) >= 1 and cand[0] in ("goldenglobe", "goldenglobes"):
        cand = cand[1:]
    if len(cand) >= 2 and cand[0:2] in (["golden", "globe"], ["golden", "globes"]):
        cand = cand[2:]
    if cand and "award" in cand:
        val += 20
    if cand and "category" in cand:
        val += 10
    if cand and cand[0] == "for":
        cand = cand[1:]
        val += 5
    if cand and cand[0] == "best ":
        val += 200
    if cand and cand[0] == "at":
        cand = cand[1:]
    if "as" in cand:
        ind = cand.index("as")
        cand = cand[:ind]
        val += 5
    if "with" in cand:
        ind = cand.index("with")
        cand = cand[:ind]
        val += 5
    if "at" in cand:
        ind = cand.index("at")
        cand = cand[:ind]
        val += 5
    if "for" in cand:
        ind = cand.index("for")
        cand = cand[:ind]
        val += 5
    if "from" in cand:
        ind = cand.index("from")
        cand = cand[:ind]
    if "award" in cand:
        ind = cand.index("award")
        cand = cand[:ind]
    return cand, val

def prep_awards():
    candidates = {}
    for tweet in TWEETS_FOR_AWARDS:
        tweet_sublists = verb_prefix(tweet)
        for tweet_sublist, val in tweet_sublists:
            tweet_sublists2 = verb_prefix(tweet_sublist)
            if tweet_sublists2:
                tweet_sublists.extend(tweet_sublists2)
            else:
                cand, val = tweet_lst_to_candidate(tweet_sublist, val)
                n = len(cand)
                cand = " ".join(cand)
                val += 5 * n
                if cand in candidates:
                    candidates[cand] += val
                else:
                    candidates[cand] = val
    candidates = {x[0]: x[1] for x in list(sorted(candidates.items(), key=lambda i: i[1], reverse=True))}
    candidates_lst = list(candidates.keys())
    max_val = candidates[candidates_lst[0]]
    candidates = {k: v for (k, v) in candidates.items() if v > (max_val / 100)}
    cands_to_del = set()
    for i in range(len(candidates)):
        cand_i = candidates_lst[i]
        for j in range(len(candidates)):
            if i < j:
                cand_j = candidates_lst[j]
                n_i, n_j = len(cand_i.strip().split()), len(cand_j.strip().split())
                if fuzz.token_sort_ratio(cand_i, cand_j) >= 97 or fuzz.token_set_ratio(candidates_lst[i], candidates_lst[j]) >= 95:
                    if cands_to_del and n_i >= 4 and candidates[cand_i] > candidates[cand_j]:
                        candidates[cand_i] += candidates[cand_j]
                        cands_to_del.add(cand_j)
                    elif n_j >= 4 and candidates[cand_j] > candidates[cand_i]:
                        candidates[cand_j] += candidates[cand_i]
                        cands_to_del.add(cand_i)
                    else:
                        if n_i > n_j:
                            candidates[cand_i] += candidates[cand_j] // 2
                            cands_to_del.add(cand_j)
                        else:
                            candidates[cand_j] += candidates[cand_i] // 2
                            cands_to_del.add(cand_i)
        if n_i < 4 or "golden globe" in cand_i or "golden globes" in cand_i or "award" in cand_i or "awards" in cand_i or "gg" in cand_i:
            cands_to_del.add(cand_i)
    for cand in cands_to_del:
        del candidates[cand]
    candidates = {k: candidates[k] for k in candidates if k not in cands_to_del}
    return [x[0] for x in list(sorted(candidates.items(), key=lambda i: i[1], reverse=True))[:20]]

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    with open("results" + str(year) + ".json", "r") as f:
        d = json.load(f)
    awards = d["Awards"]
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    with open("results" + str(year) + ".json", "r") as f:
        d = json.load(f)
    official_awards = OFFICIAL_AWARDS_1315 if int(year) < 2016 else OFFICIAL_AWARDS_1819
    nominees = {k: d[k]["Nominees"] for k in d if k in official_awards}
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    with open("results" + str(year) + ".json", "r") as f:
        d = json.load(f)
    official_awards = OFFICIAL_AWARDS_1315 if int(year) < 2016 else OFFICIAL_AWARDS_1819
    winner = {k: d[k]["Winner"] for k in d if k in official_awards}
    return winner

def prep_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    count = 0
    # Get Keywords
    keywords = WINNER_KEYWORDS.split(";")
    # Get awards
    official_awards = OFFICIAL_AWARDS_1315 if int(year) < 2016 else OFFICIAL_AWARDS_1819
    # Winner Dict from Awards
    # Initialize values as an empty str
    winners = dict.fromkeys(official_awards, "")
    flag = ''
    # Loop through awards
    for award in official_awards:
        # List of people
        people = []
        # List of nouns
        noun_list = []
        # Get award keywords
        award_keywords = award.split() 
        # Super HACKY
        award_tweets_key = award_keywords[TOKEN_AWARD_1[count]] if int(year) < 2016 else award_keywords[TOKEN_AWARD_2[count]]
        award_keywords = remove_stopwords_lst(award_keywords)
        # Check if looking for Noun or Person
        if any(word in award_keywords for word in PERSON_WORDS):
            flag = 'PERSON'
            for tweet in AWARD_TWEETS[award_tweets_key]:
                text = tweet
                # Get text
                text.replace('\d+', '')
                text = re.sub(r'\w*\d+\w*', '',text)
                text = re.sub(r'[^\w\s]', '',text)
                # Check for keywords
                if any(word in text.lower() for word in award_keywords):
                    # If so,
                    entities = spacy_tag_entity(text)
                    persons = get_people_from_ents(entities)
                    persons = remove_stopwords_lst(persons, stop_words = STOP_WORDS)
                    if award_tweets_key in persons:
                        persons.remove(award_tweets_key)
                    people = people + persons
        else:
            flag = 'NOUN'
            # Loop through tweets
            for tweet in AWARD_TWEETS[award_tweets_key]:

                text = tweet
                # Get text
                text.replace('\d+', '')
                text = re.sub(r'\w*\d+\w*', '',text)
                text = re.sub(r'[^\w\s]', '',text)
                # Check for keywords
                if any(word in text.lower() for word in award_keywords):
                    # If so,
                    tags = spacy_tag_speech(text)
                    #proper_nouns = get_proper_nouns(tags)
                    nouns = get_proper_nouns(tags)
                    if (type(nouns) != type(None)):
                        nouns = remove_stopwords_lst(nouns, stop_words=STOP_WORDS)
                        if award_tweets_key in nouns:
                            nouns.remove(award_tweets_key)
                        noun_list = noun_list + nouns
        # Get Counter        
        if flag == "PERSON":
            award_counter = Counter(people) 
        if flag == "NOUN":
             award_counter = Counter(noun_list)
        # Get most common element
        winners[award] = award_counter.most_common(1)[0][0]
        count += 1
    # Your code here
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    with open("results" + str(year) + ".json", "r") as f:
        d = json.load(f)
    official_awards = OFFICIAL_AWARDS_1315 if int(year) < 2016 else OFFICIAL_AWARDS_1819
    presenters = {k: d[k]["Presenters"] for k in d if k in official_awards}
    return presenters

def prep_presenters(year):
    keywords = PRESENTER_KEYWORDS.split(";")
    count = 0
    # Get awards
    official_awards = OFFICIAL_AWARDS_1315 if int(year) < 2016 else OFFICIAL_AWARDS_1819
    # Winner Dict from Awards
    # Initialize values as an empty str
    presenters = dict.fromkeys(official_awards, "")
    flag = ''
    # Loop through awards
    for award in official_awards:
        # List of people
        people = []
        # List of nouns
        noun_list = []
        # Get award keywords
        award_keywords = award.split() 
        #print(award_keywords)
        # Super HACKY
        award_tweets_key = award_keywords[TOKEN_AWARD_1[count]] if int(year) < 2016 else award_keywords[TOKEN_AWARD_2[count]]
        award_keywords = remove_stopwords_lst(award_keywords)
        # Check if looking for Noun or Person
        if any(word in award_keywords for word in PERSON_WORDS):
            flag = 'PERSON'
            for tweet in AWARD_TWEETS[award_tweets_key]:
                text = tweet
                # Get text
                text.replace('\d+', '')
                text = re.sub(r'\w*\d+\w*', '',text)
                text = re.sub(r'[^\w\s]', '',text)
                # Check for keywords
                if any(word in text.lower() for word in award_keywords):
                    # If so,
                    entities = spacy_tag_entity(text)
                    persons = get_people_from_ents(entities)
                    persons = remove_stopwords_lst(persons, stop_words = STOP_WORDS)
                    if award_tweets_key in persons:
                        persons.remove(award_tweets_key)
                    people = people + persons
        else:
            flag = 'NOUN'
            # Loop through tweets
            for tweet in AWARD_TWEETS[award_tweets_key]:
                text = tweet
                # Get text
                text.replace('\d+', '')
                text = re.sub(r'\w*\d+\w*', '',text)
                text = re.sub(r'[^\w\s]', '',text)
                # Check for keywords
                if any(word in text.lower() for word in award_keywords):
                    # If so,
                    tags = spacy_tag_speech(text)
                    #proper_nouns = get_proper_nouns(tags)
                    nouns = get_proper_nouns(tags)
                    if (type(nouns) != type(None)):
                        nouns = remove_stopwords_lst(nouns, stop_words=STOP_WORDS)
                        if award_tweets_key in nouns:
                            nouns.remove(award_tweets_key)
                        noun_list = noun_list + nouns
        # Get Counter        
        if flag == "PERSON":
            award_counter = Counter(people) 
        if flag == "NOUN":
             award_counter = Counter(noun_list)
        # Get most common element
        presenters[award] = [i[0] for i in award_counter.most_common(4)]
        # print(presenters[award])
        count += 1
    #presenters = {}
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Load Name Data tsv, Extract Data into Dict, text processing?
    # Your code here
    global YEAR
    YEAR = input("Please enter a year....")
    YEAR = str(YEAR)
    extract_data(YEAR)
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    # Get Year
    year = YEAR
     # Start Timer
    timer = time.time()
    awards = prep_awards()
    split_award_tweets()
    split_nominee_tweets()
    split_presenter_tweets()
    host = prep_hosts(year)
    get_best_dressed(year)
    get_worst_dressed(year)
    winner = prep_winner(year)
    presenter = prep_presenters(year)
    json_dict = {} 
    json_dict["Host"] = host
    json_dict["Awards"] = awards
    official_awards = OFFICIAL_AWARDS_1315 if int(year) < 2016 else OFFICIAL_AWARDS_1819
    for award in official_awards:
        json_dict[award] = {}
        json_dict[award]["Presenters"] = presenter[award]
        json_dict[award]["Nominees"] = []
        json_dict[award]["Winner"] = winner[award]
    out_file = open("results" + str(year) + ".json", "w")
    json.dump(json_dict, out_file)
    time_passed = str(time.time() - timer)
    print(f"Time taken: {time_passed}")
    return

if __name__ == '__main__':
    pre_ceremony()
    main()
