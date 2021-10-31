import json
import re
import time

from collections import Counter
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


STOP_WORDS = ['than', "isn't", 'weren', 'have', 'what', 'the', 'they', 'more', 'doesn', "mightn't", 'them', 'itself', 'own', 'or', 'you', 'theirs', 'before', 'how', 'were', 'does', 'ma', 'he', 'same', 'each', 'doing', 'at', 'couldn', "needn't", 'but', "weren't", 'only', 'over', 'again', 'any', 'now', 'here', 'no', 'mustn', 're', 'nor', 'so', "she's", 'above', 'against', "didn't", 'myself', 'an', 'ain', 'shouldn', 'where', 'their', 'won', 'yours', 'himself', 'further', 'i', 'this', 'didn', 'these', 'herself', 'both', 'her', 'aren', 'its', 'other', "wouldn't", "shan't", 'all', 'in', 'do', 'with', 'up', 'there', 'our', 'needn', 'such', 'while', 'too', "hasn't", "don't", 'below', 'ourselves', 'to', 've', "couldn't", 'because', 'down', "doesn't", 'is', 'if', 'wouldn', "aren't", 'who', "haven't", 'being', 'then', 'very', "should've", 'should', 'that', 'few', 'hadn', 'under', 'hasn', 'as', 'off', "won't", 'not', 'm', 'hers', 'a', "you've", 'him', 'yourself', 'she', 'on', 't', "hadn't", 'shan', 'of', 'about', 'it', "you're", 'why', 'are', 'through', 'between', 'having', 'whom', 'until', 'and', 'your', 'those', 'me', 'o', 's', 'ours', 'y', 'will', 'my', 'into', 'themselves', 'did', 'be', 'wasn', 'd', 'yourselves', "shouldn't", 'when', 'during', 'isn', "you'd", "wasn't", 'am', "it's", 'by', 'haven', 'been', 'can', "you'll", 'had', 'from', 'most', "that'll", 'don', 'out', 'for', 'after', 'some', 'we', 'his', 'once', 'has', 'was', 'mightn', 'just', 'll', "mustn't", 'which']

def remove_punc(words):
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


def get_data(year):
    with open("gg" + str(year) + ".json", "r") as read_file:
        tweets_json = json.load(read_file)
    tweets_lst = []
    for tweet in tweets_json:
        tweets_lst.append(remove_punc(tweet["text"].lower().strip().split()))
    return tweets_lst


def verb_prefix(tweet):
    tweet_lsts = []
    for verbs in verb_prefixes:
        split_verbs = verbs.split()
        n = len(split_verbs)
        indices = [i for (i, w) in enumerate(tweet) if tweet[i:i + n] == split_verbs]
        if indices:
            tweet_lsts.append((tweet[indices[-1] + n:], verb_prefixes[verbs]))
    return tweet_lsts


verb_prefixes = {
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


def tweet_lst_to_candidate(cand, val):
    og_cand = cand
    if cand and (cand[0] == "the" or cand[0] == "a" or cand[0] == "an"):
        cand = cand[1:]
    if len(cand) >= 1 and cand[0] in ("goldenglobe", "goldenglobes"):
        cand = cand[1:]
    if len(cand) >= 2 and cand[0:2] in (["golden", "globe"], ["golden", "globes"]):
        cand = cand[2:]
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

def count_scripts():
    tweets = get_data(2015)
    candidates = {}
    for tweet in tweets:
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
    return {x[0]: x[1] for x in list(sorted(candidates.items(), key=lambda i: i[1], reverse=True))[:20]}

start = time.time()
awards_dict = count_scripts()
print(time.time() - start)
awards = list(awards_dict.keys())

for award in awards_dict:
    print(award + ": " + str(awards_dict[award]))


award_answers = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


import sys
import json
import difflib
from pprint import pprint
from collections import Counter

from nltk.metrics import edit_distance


global toMovie
toMovie = {'johann johannsson': 'the theory of everything', 'alexandre desplat': 'the imitation game', 'trent reznor and atticus ross': 'gone girl', 'antonio sanchez': 'birdman', 'hans zimmer': 'interstellar', 'glory': 'selma', 'big eyes': 'big eyes', 'mercy is': 'noah', 'opportunity': 'annie', 'yellow flicker beat': 'the hunger games mockingjay part 1', 'alejandro gonzalez inarritu': 'birdman', 'wes anderson': 'the grand budapest hotel', 'gillian flynn': 'gone girl', 'richard linklater': 'boyhood', 'graham moore': 'the imitation game'}


def norm_text(textstring):
    return "".join([c.lower() for c in textstring if c.isalnum() or c.isspace()])


def text(resultstr, answerstr):

    result = resultstr.split()
    answer = answerstr.split()

    len_result = len(result)
    len_answer = len(answer)

    if (resultstr in answerstr) or (answerstr in resultstr):
        textscore = min(len_result, len_answer)/float(max(len_result, len_answer))
    else:
        s = difflib.SequenceMatcher(None, result, answer)

        longest = s.find_longest_match(0, len_result, 0, len_answer)
        longest = longest.size/float(max(len_result, len_answer))

        if longest > 0.3:
            matchlen = sum([m[2] for m in s.get_matching_blocks() if m[2] > 1])
            textscore = float(matchlen)/max(len_result, len_answer)
        else:
            textscore = longest

    return textscore


def spell_check(r, a, s, scores, weight=1):
    change = weight*(1-(edit_distance(r, a)/float(max(len(r), len(a)))))
    if s in scores:
        # penalty for returning multiple of the same result when
        # one instance is incorrectly spelled
        return (scores[s] + change)/2.0
    else:
        return change


def calc_translation(result, answer):

    resultmap = {norm_text(r): r for r in result}
    answermap = {norm_text(a): a for a in answer}
    result = set(resultmap.keys())
    answer = set(answermap.keys())

    intersection = result.intersection(answer)
    translation = {resultmap[i]: answermap[i] for i in intersection}
    scores = dict(list(zip(list(translation.values()), [1]*len(intersection))))
    score_by_results = {}
    score_by_answers = {}

    # loop through results that didn't have a perfect match
    # and get a score for each of them.
    comp = list(result - intersection)

    for r in comp:
        score_by_results[r] = Counter()
        for a in answer:
            if a not in score_by_answers:
                score_by_answers[a] = Counter()

            score_by_results[r][a] = text(r, a)
            score_by_answers[a][r] = score_by_results[r][a]

    for r in score_by_results:
        cnt = 0
        ranking = score_by_results[r].most_common()
        flag = True
        while flag:
            # The answer that best matches the result
            answer_match = ranking[cnt][0]
            # The top result matching that answer
            max_result = score_by_answers[answer_match].most_common(1)[0]

            if score_by_results[r][answer_match] < 0.45:
                bestAnswer = False
                score = 0

                # Unacceptably low score.
                # Check if we have a case of returning the movie instead
                # of the person, or vice versa.
                for ha in toMovie:
                    tempScore = text(r, ha)
                    if tempScore > score:
                        score = tempScore
                        bestAnswer = ha

                if bestAnswer and score > 0.45:
                    translation[resultmap[r]] = toMovie[ha]
                    scores[toMovie[ha]] = spell_check(r, ha, toMovie[ha], scores, 0.5)

                flag = False
            elif (max_result[0] == r) or (score_by_results[r][answer_match] > score_by_answers[answer_match][max_result[0]]):
                # if the top result matching that answer is our current result or
                # if the current result's score is greater than the previous top result
                translation[resultmap[r]] = answermap[answer_match]
                scores[answermap[answer_match]] = spell_check(r, answer_match, answer_match, scores)

                flag = False

            cnt += 1
            if cnt == len(ranking):
                flag = False

    if scores:
        return sum(scores.values())/float(len(scores)), translation
    else:
        return 0, translation


def calc_score(result, answer):
    result = set(result)
    intersection = result.intersection(answer)
    len_intersection = len(intersection)
    len_union = len(result.union(answer))
    len_result = len(result)
    len_answer = len(answer)

    if len_union == 0:
        return 0
    elif len_result == len_answer and len_intersection == len_answer:
        m = 1.0
    elif len_intersection == len_result:
        # all results correspond to a correct answer, but some 
        # answers are missing
        m = 0.95
    elif len_intersection == len_answer:
        # all answers correspond to a result, but there are
        # some extra results as well
        m = 0.9
    elif len_intersection > 0:
        # there is some post-translation intersection between
        # results and answers.
        m = 0.85
    else:
        return 0

    return (len_intersection / float(len_union)) * m


i = 20
# maxx = (0, 0, 0, {})
# for i in range(18, 53):
spelling_score, translation = calc_translation(awards[:i], award_answers)
c_score = calc_score([translation[res] if res in translation else res for res in awards[:i]], award_answers)
# if c_score > maxx[1]:
# maxx = (i, c_score, spelling_score, translation)

print(spelling_score)
print(c_score)
# print()
# print(maxx[0])
# print(maxx[1])
# print(maxx[2])
# for t in maxx[3]:
#     print(t + "  :  " + maxx[3][t])
    


# for A, prefer answers that start with "best"
# for X, Y, etc., prefer answers that are in the IMDB list (movies or actors)
# for scripts without an ending ([X] wins [A], e.g.), add each prefix until the end of the tweet
# favor tweets with the word "category" or "award" in them?
# bias against golden or golden globe