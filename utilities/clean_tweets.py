import json
import os
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.tag import pos_tag
from util import *
import re
import numpy as np
import pandas as pd
import preprocessor as p
import spacy
from spacy.tokenizer import Tokenizer
from pprint import pprint

nlp = spacy.load("en_core_web_sm")

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent ne chunker')
nltk.download('words')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
"""

    Script to clean tweets using the NLTK, Regular Expressions, and some basic cleaning techniques. Nothing fancy.

    Will need to pull a lot of this functionality out, generalize, so we can set up cmd line args

    Just testing for now, only first 10,000 or so Tweets because my laptop has never worked harder in its life

    NLTK Named Entity Recognition is fairly poor out of the box in comparison to SPACY's, will probably make a swap but unfamiliar with the SPACY library

"""
# Max constant for testing
TWEET_MAX = 174643
# Year constant for testing
YEAR = 2013
# Get current directory
path = os.getcwd()
# Get parent directory
path = os.path.abspath(os.path.join(path, os.pardir))

# Mappings -- I don't think we're supposed to use dicts anymore, something about named tuples idk. 
tweet_to_tags = {}
tweet_to_netree = {}
name_dict = {}

# Load and Extract Data
def extract_data(year):
    print("Extracting Data\n") if DEBUG == 1 else 0
    # Get path to JSON of specified year
    src_path = '../gg' + str(year) + '.json'
    # Open
    with open(src_path, "r") as read_file:
        # Load JSON
        tweets = json.load(read_file)
    # Load into DataFrame
    tweets = pd.json_normalize(tweets)
    # Carve out hashtags
    tweets['hashtag'] = tweets['text'].apply(lambda x: re.findall(r"#(\w+)", x))
    # TESTING PRINT
    print(len(tweets))
    # Return DataFrame 
    return tweets

# Tokenization 
lemmatizer = nltk.stem.WordNetLemmatizer()
tokenizer = TweetTokenizer()
def lemmatize_text(text):
    #print("Tokenization + Lemmatization\n") if DEBUG == 1 else 0
    return [(lemmatizer.lemmatize(w)) for w in tokenizer.tokenize((text))]

# Remove Punctuation
def remove_punc(words):
    #print("Removing Punctuation\n") if DEBUG == 1 else 0
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', (word))
        if new_word != '':
            new_words.append(new_word)
    return new_words

# Remove Stopwords
def remove_stopwords_str(words):
    #print("Removing Stopwords\n") if DEBUG == 1 else 0
    list_words = words.split()
    stop_words = set(stopwords.words('english'))
    new_words = list(filter(lambda x: (x not in stop_words), list_words))
    new_words = " ".join(new_words)
    return new_words

def remove_stopwords_lst(words):
    #print("Removing Stopwords\n") if DEBUG == 1 else 0
    stop_words = set(stopwords.words('english'))
    return list(filter(lambda x: (x not in stop_words), words))

# Clean Text
def clean_text(df):
    print("Cleaning Text\n") if DEBUG == 1 else 0
    global name_dict
    for i, v in enumerate(df['text']):
        # Get text
        uncleaned_text = v
        # Clean 
        clean_text = v #p.clean(v)
        # Replace digits
        clean_text.replace('\d+', '')
        # Remove extraneous spaces
        clean_text = re.sub(r'\w*\d+\w*', '', clean_text)
        ## Remove Punctuation
        clean_text = re.sub(r'[^\w\s]', '', clean_text)
        # Lemmatize & Tokenize
        # Part of Speech Tagging
        #tagged_text = remove_stopwords_lst(lemmatize_text(clean_text))
        #tagged_text = tag_speech(tagged_text)
        # Remove Stop Words, convert back to str
        clean_text = remove_stopwords_str(clean_text)
        # Assign to new column
        df.loc[i, 'clean_text'] = clean_text

        # Spacy Entity Recognition
        # ent_list = spacy_tag_entity(uncleaned_text)
        # new_ent_list = []
        # if len(ent_list) != 0:
        #     words = []
        #     for ent in ent_list:
        #         if ent[1] == 'PERSON':
        #             new_ent_list.append(ent)

        # # Assign to column
        # count = 1
        # for ent in new_ent_list:
        #     column_name = 'Ent_list_' + str(count)
        #     entity_name = ent[0]
        #     entity_tag = ent[1]
        #     entity = entity_name + ' : ' + entity_tag
        #     df.loc[i, column_name] = entity
        #     count += 1
        
        # Assign to mapping, Pandas hates lists
        #name_dict[clean_text] = new_ent_list

        # # Assign to mapping
        # tweet_to_tags[i] = tagged_text
        # # Get Named Entities
        # # Should be spaCy NER w/ uncleaned_text
        # named_entity_tree = nltk.ne_chunk(tagged_text)
        # # Assign to mapping
        # tweet_to_netree[i] = named_entity_tree
        # Sanity Checks
        if i == TWEET_MAX:
            break
        elif i % 1000 == 0:
            print(f"# Tweets processed: {i} \n")
            print(f"Uncleaned text is: {uncleaned_text}\n")
            print(f"Cleaned text is: {clean_text}\n")
            #print(f"Ent list is: {new_ent_list}\n")


# Part of Speech Tagging
def tag_speech(words):
    new_words = nltk.pos_tag(words)
    return new_words


# Spacy tokenizes in its nlp function. It takes phrases as strings

# Spacy Part of Speech Tagging
def spacy_tag_speech(tweet: str):
    doc = nlp(tweet)
    # # This return statement is the more detailed one
    # # returns [(word, pos, detailed pos)] for each word in the tweet
    # return [(token.text, token.pos_, token.tag_) for token in doc]
    # returns [(word, part of speech)] for each word in the tweet
    return [(token.text, token.pos_) for token in doc]
# Spacy Entity Tagging
def spacy_tag_entity(tweet: str):
    doc = nlp(tweet)
    # returns [(entity, label)] for each entity in the tweet
    # e.g. [("European", "NORP"), ("Google", "ORG"), ("5.1 billion", "MONEY"), ("Wednesday", "DATE")]
    return [(X.text, X.label_) for X in doc.ents]

# Get keywords
def get_keywords(tweets):
    pass
# Integrate Named Entity Tree
def integrate_netree(tweets,netree):
    pass
# Integrate Part of Speech Tags
def integrate_pos_tag(tweets,pos_tags):
    pass
# Write Data to path
def write_data(tweets, path):
    tweets.to_csv(path)
# Create Entity Tree CSV
def create_entity_tree_csv(dict, orient, year):
    tweet_netree_df = pd.DataFrame.from_dict(dict, orient=orient)
    path = 'tweet_netree_df_' + str(year) + '.csv'
    tweet_netree_df.to_csv(path)
# Create Part of Speech Tags CSV
def create_pos_tag_csv(dict, orient, year):
    tweet_pos_tag_csv = pd.DataFrame.from_dict(dict, orient=orient)
    path = 'tweet_tag_df_' + str(year) + '.csv'
    tweet_pos_tag_csv.to_csv(path)

###### TESTING ######
# Call Extract data w/ Year to get DataFrame of Tweets w/ hashtags broken into 'hashtags' column
tweets = extract_data(YEAR)
# Clean the tweets
clean_text(tweets)
# Get to MAX_TWEET 
tweets.head(TWEET_MAX).to_csv('cleaned_tweets_13.csv')

# Regexpr Patterns
award_pattern_pre = re.compile('Best ([A-z\s-]+)[A-Z][a-z]*[^A-z]')
award_pattern_post = re.compile(".*^((?!(goes|but|is|in|by an|a)).)*$")
presenter_pattern = re.compile('present[^a][\w]*\s([\w]+\s){1,5}')
presenter_pattern_2 = re.compile(r"^(?=.*\b(present.*)\b).*$")
nominee_pattern = re.compile(r"^(?=.*\b(nomin.*)\b).*$")
award_type_pattern = re.compile(r"^(?=.*\b(drama|comedy|musical|animated|foreign|screenplay|original|song|score)\b)(?=.*\b(motion|picture|movie|tv|television|series|limited)\b).*$")
job_type_pattern = re.compile(r"^(?=.*\b(actor|actress|director)\b).*$")
role_type_pattern = re.compile(r"^(?=.*\b(supporting|support)\b)(?=.*\b(actor|actress)\b).*$")

# Get Tweets
tweets_list = tweets["clean_text"].head(TWEET_MAX).to_list()
tweets_list_uncleaned = tweets["text"].head(TWEET_MAX).to_list()

# Filter using regexp
# Awards
award_tweets = [award_pattern_pre.search(tweet).group(0)[:-1] for tweet in tweets_list if award_pattern_pre.search(tweet)]
award_tweets_2 = [award_pattern_post.search(tweet).group(0)[:-1] for tweet in tweets_list if award_pattern_post.search(tweet)]
award_tweets_3 = [award_type_pattern.search(tweet).group(0)[:-1] for tweet in tweets_list if award_type_pattern.search(tweet)]
# Presenters
presenter_tweets = [presenter_pattern.search(tweet).group(0)[:-1] for tweet in tweets_list if presenter_pattern.search(tweet)]
presenter_tweets_2 = [presenter_pattern_2.search(tweet).group(0)[:-1] for tweet in tweets_list if presenter_pattern_2.search(tweet)]
presenter_award_tweets = [award_pattern_pre.search(tweet).group(0)[:-1] for tweet in presenter_tweets if award_pattern_pre.search(tweet)]
presenter_award_tweets_2 = [award_pattern_pre.search(tweet).group(0)[:-1] for tweet in presenter_tweets_2 if award_pattern_pre.search(tweet)]
# Hosts, no Regexpr needed
host_tweets = list(filter(lambda x: ('host' in x), tweets_list))
# Nominees
nominee_tweets = [nominee_pattern.search(tweet).group(0)[:-1] for tweet in tweets_list if nominee_pattern.search(tweet)]
nominee_tweets_2 = list(filter(lambda x : ('nominee' in x.lower() or 'nominated' in x.lower() or 'nominate' in x.lower() or 'nominations' in x.lower()), tweets_list))
best_comedy_nominee_tweets = list(filter(lambda x : ('comedy' in x.lower() or 'musical' in x.lower()), nominee_tweets))
best_comedy_nominee_tweets_2 = list(filter(lambda x : ('comedy' in x.lower() or 'musical' in x.lower()), nominee_tweets_2))
best_drama_nominee_tweets = list(filter(lambda x : ('drama' in x.lower()), nominee_tweets))
best_drama_nominee_tweets_2 = list(filter(lambda x : ('drama' in x.lower()), nominee_tweets_2))
best_screenplay_nominee_tweets = list(filter(lambda x : ('screenplay' in x.lower()), nominee_tweets))
best_screenplay_nominee_tweets_2 = list(filter(lambda x : ('screenplay' in x.lower()), nominee_tweets_2))
best_animated_nominee_tweets = list(filter(lambda x : ('animated' in x.lower()), nominee_tweets))
best_animated_nominee_tweets_2 = list(filter(lambda x : ('animated' in x.lower()), nominee_tweets_2))
best_director_nominee_tweets = list(filter(lambda x : ('director' in x.lower()), nominee_tweets))
best_director_nominee_tweets_2 = list(filter(lambda x : ('director' in x.lower()), nominee_tweets_2))

# Awards
best_comedy_tweets = list(filter(lambda x : ('comedy' in x or 'musical' in x.lower()), award_tweets))
best_comedy_tweets_2 = list(filter(lambda x : ('comedy' in x or 'musical' in x.lower()), award_tweets_2))
# Gonna try for best actress
best_actress_tweets = list(filter(lambda x : ('actress' in x.lower()), award_tweets))
best_actress_tweets_2 = list(filter(lambda x : ('won' in x.lower()), award_tweets_2))
# Supporting actress
best_supporting_actress_tweets = list(filter(lambda x : ('supporting' in x.lower()), best_actress_tweets))
best_supporting_actress_tweets_2 = list(filter(lambda x : ('supporting' in x.lower()), best_actress_tweets_2))
# Best actor
best_actor_tweets = list(filter(lambda x : ('actor' in x.lower()), award_tweets))
best_actor_tweets_2 = list(filter(lambda x : ('won' in x.lower()), award_tweets_2))
# Supporting actor
best_supporting_actor_tweets = list(filter(lambda x : ('supporting' in x.lower()), best_actor_tweets))
best_supporting_actor_tweets_2 = list(filter(lambda x : ('supporting' in x.lower()), best_actor_tweets_2))
# Drama | Director | Screenplay
best_drama_tweets = list(filter(lambda x : ('drama' in x.lower()), award_tweets))
best_director_tweets = list(filter(lambda x : ('director' in x.lower()), award_tweets))
best_screenplay_tweets = list(filter(lambda x : ('screenplay' in x.lower()), award_tweets))
best_drama_tweets_2 = list(filter(lambda x : ('drama' in x.lower()), award_tweets_3))
best_director_tweets_2 = list(filter(lambda x : ('director' in x.lower()), award_tweets_3))
best_screenplay_tweets_2 = list(filter(lambda x : ('screenplay' in x.lower()), award_tweets_3))
# Animated | Foreign | Score | Song
best_animated_tweets = list(filter(lambda x : ('animated' in x.lower()), award_tweets_3))
best_animated_tweets_2 = list(filter(lambda x : ('animated' in x.lower()), award_tweets_2))
best_foreign_tweets = list(filter(lambda x : ('foreign' in x.lower()), award_tweets_3))
best_foreign_tweets_2 = list(filter(lambda x : ('foreign' in x.lower()), award_tweets_2))
best_score_tweets = list(filter(lambda x : ('score' in x.lower()), award_tweets_3))
best_song_tweets = list(filter(lambda x : ('song' in x.lower()), award_tweets_3))


print("\t\t\tThe length of the tweet lists: \n\n")
print("\t\t\tAwards: \n")
print(f"The length of award tweets is {len(award_tweets)}")
print(f"The length of award tweets 2 is {len(award_tweets_2)}")
print(f"The length of award tweets 3 is {len(award_tweets_3)}\n")

print(f"The length of presenter_tweets is {len(presenter_tweets)}")
print(f"The length of presenter_tweets 2 is {len(presenter_tweets_2)}")
print(f"The length of presenter_award_tweets is {len(presenter_award_tweets)}")
print(f"The length of presenter_award_tweets 2 is {len(presenter_award_tweets_2)}\n")

print(f"The length of best actress tweets is {len(best_actress_tweets)}")
print(f"The length of best actress tweets 2 is {len(best_actress_tweets_2)}\n")

print(f"The length of best supporting actress tweets is {len(best_supporting_actress_tweets)}")
print(f"The length of best supporting actress tweets 2 is {len(best_supporting_actress_tweets_2)}\n")


print(f"The length of best actor tweets is {len(best_actor_tweets)}")
print(f"The length of best actor tweets 2 is {len(best_actor_tweets_2)}\n")

print(f"The length of best supporting actor tweets is {len(best_supporting_actor_tweets)}")
print(f"The length of best supporting actor tweets 2 is {len(best_supporting_actor_tweets_2)}\n")

print(f"The length of best director tweets is {len(best_director_tweets)}")
print(f"The length of best director tweets 2 is {len(best_director_tweets_2)}\n")

print(f"The length of best comedy tweets is {len(best_comedy_tweets)}")
print(f"The length of best comedy tweets 2 is {len(best_comedy_tweets_2)}\n")

print(f"The length of best drama tweets is {len(best_drama_tweets)}")
print(f"The length of best drama tweets 2 is {len(best_drama_tweets_2)}\n")

print(f"The length of best screenplay tweets is {len(best_screenplay_tweets)}")
print(f"The length of best screenplay tweets 2 is {len(best_screenplay_tweets_2)}\n")

print(f"The length of best animated tweets is {len(best_animated_tweets)}")
print(f"The length of best animated tweets 2 is {len(best_animated_tweets_2)}")
print(f"The length of best foreign tweets is {len(best_foreign_tweets)}")
print(f"The length of best foreign tweets 2 is {len(best_foreign_tweets_2)}")
print(f"The length of best score tweets is {len(best_score_tweets)}")
print(f"The length of best song tweets is {len(best_song_tweets)}")



print("\n\n\n")
print("\t\t\tNominees\n\n")
print(f"The length of nominee tweets is {len(nominee_tweets)}") 
print(f"The length of nominee tweets 2 is {len(nominee_tweets_2)}\n") 

print(f"The length of animated motion film tweets is {len(best_animated_nominee_tweets)}")
print(f"The length of animated motion film tweets 2 is {len(best_animated_nominee_tweets_2)}\n")

print(f"The length of nominee best comedy tweets is {len(best_comedy_nominee_tweets)}")
print(f"The length of nominee best comedy tweets 2 is {len(best_comedy_nominee_tweets_2)}\n")

print(f"The length of nominee best drama tweets is {len(best_drama_nominee_tweets)}")
print(f"The length of nominee best drama tweets 2 is {len(best_drama_nominee_tweets_2)}\n")

print(f"The length of nominee best director tweets is {len(best_director_nominee_tweets)}")
print(f"The length of nominee best director tweets 2 is {len(best_director_nominee_tweets_2)}\n")

print(f"The length of nominee best screenplay tweets is {len(best_screenplay_nominee_tweets)}")
print(f"The length of nominee best screenplay tweets 2 is {len(best_screenplay_nominee_tweets_2)}\n")

print("\t\t\tHosts\n\n")
print(f"The length of host tweets is {len(host_tweets)}\n")

print("Hit key to continue")
continue_msg = input(" ")
print("Awards\n\n")
pprint(award_tweets_3[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Actress\n\n")
pprint(best_actress_tweets[0:150])
pprint(best_actress_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Actor\n\n")
pprint(best_actor_tweets[0:150])
pprint(best_actor_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Nominees\n\n")
pprint(nominee_tweets[0:150])
pprint(nominee_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Supporting Actor\n\n")
pprint(best_supporting_actor_tweets[0:50])
pprint(best_supporting_actor_tweets_2[0:50])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Supporting Actress\n\n")
pprint(best_supporting_actress_tweets[0:50])
pprint(best_supporting_actress_tweets_2[0:50])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Comedy Nominee\n\n")
pprint(best_comedy_nominee_tweets[0:150])
pprint(best_comedy_nominee_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Comedy\n\n")
pprint(best_comedy_tweets[0:150])
pprint(best_comedy_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Drama\n\n")
pprint(best_drama_tweets[0:150])
pprint(best_drama_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Drama Nominee\n\n")
pprint(best_drama_nominee_tweets[0:150])
pprint(best_drama_nominee_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Director\n\n")
pprint(best_director_tweets[0:150])
pprint(best_director_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Director Nominee\n\n")
pprint(best_director_nominee_tweets[0:150])
pprint(best_director_nominee_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Screenplay Nominee\n\n")
pprint(best_screenplay_nominee_tweets[0:150])
pprint(best_screenplay_nominee_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Screenplay\n\n")
pprint(best_screenplay_tweets[0:150])
pprint(best_screenplay_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Presenters\n\n")
pprint(presenter_tweets[0:150])
pprint(presenter_tweets_2[0:150])
print("Hit key to continue")
continue_msg = input(" ")
print("\n\n\n")
print("Best Animated | Foreign | Score | Song\n\n")
pprint(best_animated_tweets)
print("\n\n\n")
pprint(best_foreign_tweets)
print("\n\n\n")
pprint(best_score_tweets)
print("\n\n\nj")
pprint(best_song_tweets)