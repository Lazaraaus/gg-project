import json
import pandas as pd
import re

from collections import Counter


def remove_punc(words):
    new_words = []
    for word in words:
        if word[0] == "#":
            continue
        if len(word) >= 4 and word[:4] == "http":
            continue
        new_word = re.sub(r'[^\w\s]', '', (word))
        if new_word != '':
            new_words.append(new_word)
    return new_words, words


def remove_punc2(words):
    new_words = []
    for word in words:
        new_word = word.replace(",", " -")
        for c in new_word:
            if not c.isalnum() and c != "-":
                new_word = new_word.replace(c, "")
        if new_word:
            new_words.append(new_word)
    return new_words


def get_data(year):
    with open("gg" + str(year) + ".json", "r") as read_file:
        tweets_json = json.load(read_file)
    tweets_lst = []
    for tweet in tweets_json:
        tweets_lst.append(remove_punc(tweet["text"].lower().strip().split()))
    return tweets_lst


def verb_prefix(verbs, tweet):
    split_verbs = verbs.split()
    n = len(split_verbs)
    indices = [i for (i, w) in enumerate(tweet) if tweet[i:i + n] == split_verbs]
    return tweet[indices[-1] + n:] if indices else None


def verb_suffix(verbs, tweet):
    split_verbs = verbs.split()
    n = len(split_verbs)
    indices = [i for (i, w) in enumerate(tweet) if tweet[i:i + n] == split_verbs]
    best_index = 0
    if "best" in tweet:
        best_index = tweet.index("best")
    return tweet[best_index:indices[0]] if indices else None


verb_suffix_ratings = {
    "goes to": 10
}

verb_prefix_ratings = {
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
    "nominated for": 3
}


def count_scripts():
    tweets = get_data(2013) + get_data(2015)
    candidates = {}
    for clean_tweet, old_tweet in tweets:
        for verbs in verb_prefix_ratings:
            val = verb_prefix_ratings[verbs]
            cand = verb_prefix(verbs, clean_tweet)
            if cand:
                if cand and cand[0] == "the" or cand[0] == "a":
                    cand = cand[1:]
                if len(cand) >= 2 and cand[0:2] == ["golden", "globes"]:
                    cand = cand[2:]
                if len(cand) >= 2 and cand[0:2] == ["golden", "globe"]:
                    cand = cand[2:]
                if cand and cand[0] == "for":
                    cand = cand[1:]
                    val += 5
                if cand and cand[0] == "best ":
                    val += 100
                if cand and cand[0] == "at":
                    cand = cand[1:]
                if "at" in cand:
                    ind = cand.index("at")
                    cand = cand[:ind]
                    val += 5
                if "for" in cand:
                    ind = cand.index("for")
                    cand = cand[:ind]
                    val += 5
                try:
                    ind_start = old_tweet.index(cand[0])
                    ind_end = old_tweet.index(cand[-1])
                    cand = remove_punc2(old_tweet[ind_start:ind_end + 1])
                except:
                    pass
                if "-" in cand:
                    val += 50
                n = len(cand)
                cand = " ".join(cand)
                if n <= 1:
                    continue
                else:
                    val += 5 * n
                if cand in candidates:
                    candidates[cand] += val
                else:
                    candidates[cand] = val
        for verbs in verb_suffix_ratings:
            val = verb_suffix_ratings[verbs]
            cand = verb_suffix(verbs, clean_tweet)
            if cand:
                if cand and cand[0] == "the" or cand[0] == "a":
                    cand = cand[1:]
                if len(cand) >= 2 and cand[0:2] == ["golden", "globes"]:
                    cand = cand[2:]
                if len(cand) >= 2 and cand[0:2] == ["golden", "globe"]:
                    cand = cand[2:]
                if cand and cand[0] == "for":
                    cand = cand[1:]
                    val += 5
                if cand and cand[0] == "best ":
                    val += 100
                if cand and cand[0] == "at":
                    cand = cand[1:]
                if "at" in cand:
                    ind = cand.index("at")
                    cand = cand[:ind]
                    val += 5
                if "for" in cand:
                    ind = cand.index("for")
                    cand = cand[:ind]
                    val += 5
                try:
                    ind_start = old_tweet.index(cand[0])
                    ind_end = old_tweet.index(cand[-1])
                    cand = remove_punc2(old_tweet[ind_start:ind_end + 1])
                except:
                    pass
                if "-" in cand:
                    val += 50
                n = len(cand)
                cand = " ".join(cand)
                if n <= 1:
                    continue
                else:
                    val += 5 * n
                if cand in candidates:
                    candidates[cand] += val
                else:
                    candidates[cand] = val
    return [x[0] for x in list(sorted(candidates.items(), key=lambda i: i[1], reverse=True)[:50])]


awards = count_scripts()

print(awards)


def comp_to_scripts(tweet):
    pass

    # for A, prefer answers that start with "best"
    # for X, Y, etc., prefer answers that are in the IMDB list (movies or actors)
    # for scripts without an ending ([X] wins [A], e.g.), add each prefix until the end of the tweet
    # favor tweets with the word "category" or "award" in them?
    # bias against golden or golden globe


    # win synonyms: collect, secure, procure, earn, acquire, obtain, attain, gain
   

    # [X] win [A]
    # [X] wins [A]
    # [X] won [A]
    # [X] winning [A]
    # [X] is winning [A]
    # [X] are winning [A]
    # [X] will win [A]
    # [X] should win [A]
    # [X] should have won [A]

    # [X] win [A] for [Y]
    # [X] wins [A] for [Y]
    # [X] won [A] for [Y]
    # [X] winning [A] for [Y]
    # [X] is winning [A] for [Y]
    # [X] are winning [A] for [Y]
    # [X] will win [A] for [Y]
    # [X] should win [A] for [Y]
    # [X] should have won [A] for [Y]



    # [X] get [A]
    # [X] gets [A]
    # [X] got [A]
    # [X] getting [A]
    # [X] is getting [A]
    # [X] are getting [A]
    # [X] will get [A]
    # [X] should get [A]
    # [X] should have got [A]

    # [X] get [A] for [Y]
    # [X] gets [A] for [Y]
    # [X] got [A] for [Y]
    # [X] getting [A] for [Y]
    # [X] is getting [A] for [Y]
    # [X] are getting [A] for [Y]
    # [X] will get [A] for [Y]
    # [X] should get [A] for [Y]
    # [X] should have got [A] for [Y]



    # [A] goes to [X]
    # [A] went to [X]
    # [A] going to [X]
    # [A] is going to [X]
    # [A] will go to [X]
    # [A] should go to [X]
    # [A] should have gone to [X]



    # [X] receive [A]
    # [X] receives [A]
    # [X] received [A]
    # [X] receiving [A]
    # [X] is receiving [A]
    # [X] are receiving [A]
    # [X] will receive [A]
    # [X] should receive [A]
    # [X] should have received [A]

    # [X] receive [A] for [Y]
    # [X] receives [A] for [Y]
    # [X] received [A] for [Y]
    # [X] receiving [A] for [Y]
    # [X] is receiving [A] for [Y]
    # [X] are receiving [A] for [Y]
    # [X] will receive [A] for [Y]
    # [X] should receive [A] for [Y]
    # [X] should have received [A] for [Y]
    
    
    
    # [X] claim [A]
    # [X] claims [A]
    # [X] claimed [A]
    # [X] claiming [A]
    # [X] is claiming [A]
    # [X] are claiming [A]
    # [X] will claim [A]
    # [X] should claim [A]
    # [X] should have claimed [A]

    # [X] claim [A] for [Y]
    # [X] claims [A] for [Y]
    # [X] claimed [A] for [Y]
    # [X] claiming [A] for [Y]
    # [X] is claiming [A] for [Y]
    # [X] are claiming [A] for [Y]
    # [X] will claim [A] for [Y]
    # [X] should claim [A] for [Y]
    # [X] should have claimed [A] for [Y]
    
    
    
    # [X] take home [A]
    # [X] takes home [A]
    # [X] took home [A]
    # [X] taking home [A]
    # [X] is taking home [A]
    # [X] are taking home [A]
    # [X] will take home [A]
    # [X] should take home [A]
    # [X] should have taken home [A]

    # [X] take home [A] for [Y]
    # [X] takes home [A] for [Y]
    # [X] took home [A] for [Y]
    # [X] taking home [A] for [Y]
    # [X] is taking home [A] for [Y]
    # [X] are taking home [A] for [Y]
    # [X] will take home [A] for [Y]
    # [X] should take home [A] for [Y]
    # [X] should have taken home [A] for [Y]



    # [X] bring home [A]
    # [X] brings home [A]
    # [X] brought home [A]
    # [X] bringing home [A]
    # [X] is bringing home [A]
    # [X] are bringing home [A]
    # [X] will bring home [A]
    # [X] should bring home [A]
    # [X] should have brought home [A]

    # [X] bring home [A] for [Y]
    # [X] brings home [A] for [Y]
    # [X] brought home [A] for [Y]
    # [X] bringing home [A] for [Y]
    # [X] is bringing home [A] for [Y]
    # [X] are bringing home [A] for [Y]
    # [X] will bring home [A] for [Y]
    # [X] should bring home [A] for [Y]
    # [X] should have brought home [A] for [Y]



    # [X] present [A]
    # [X] presents [A]
    # [X] presented [A]
    # [X] presenting [A]
    # [X] is presenting [A]
    # [X] are presenting [A]
    # [X] will present [A]
    # [X] should present [A]
    # [X] should have presented [A]

    # [X] present [A] to [Y]
    # [X] presents [A] to [Y]
    # [X] presented [A] to [Y]
    # [X] presenting [A] to [Y]
    # [X] is presenting [A] to [Y]
    # [X] are presenting [A] to [Y]
    # [X] will present [A] to [Y]
    # [X] should present [A] to [Y]
    # [X] should have presented [A] to [Y]

    # [X] present [A] for [Y]
    # [X] presents [A] for [Y]
    # [X] presented [A] for [Y]
    # [X] presenting [A] for [Y]
    # [X] is presenting [A] for [Y]
    # [X] are presenting [A] for [Y]
    # [X] will present [A] for [Y]
    # [X] should present [A] for [Y]
    # [X] should have presented [A] for [Y]

    # [X] present [A] to [Y] for [Z]
    # [X] presents [A] to [Y] for [Z]
    # [X] presented [A] to [Y] for [Z]
    # [X] presenting [A] to [Y] for [Z]
    # [X] is presenting [A] to [Y] for [Z]
    # [X] are presenting [A] to [Y] for [Z]
    # [X] will present [A] to [Y] for [Z]
    # [X] should present [A] to [Y] for [Z]
    # [X] should have presented [A] to [Y] for [Z]



    # nominated for [A]
    # [X] nominated for [A]
    # [X] is nominated for [A]
    # [X] are nominated for [A]
    # [X] was nominated for [A]
    # [X] were nominated for [A]
    # [A] nominee [X]

    # up for [A]
    # [X] up for [A]
    # [X] is up for [A]
    # [X] are up for [A]
    # [X] was up for [A]
    # [X] were up for [A]