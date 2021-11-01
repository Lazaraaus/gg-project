import re

"""
    Single place for resources/utility/constant value import

"""
#############
# Constants #
#############
DEBUG = 1
CHUNKING_PATTERN = 'NP: {<DT>?<JJ>*<NN>}'
CEREMONY_TITLE = "Golden Globes"
############
# Official #
############
# Should probably tokenize each of these entries
OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
###########
# Keywords#
###########
AWARD_KEYWORDS = "best;Best;BEST;award;Award"
WINNER_KEYWORDS = "win;won;wins;gets;receives;accepts;winner"
CATEGORY_KEYWORDS = "director;motion picture;actor;actress;cecil"
HOST_KEYWORDS = "hosting;host;hosts;hostess;funny;joke;comedian;comedienne;joker;hilarious"
NOMINEE_KEYWORDS = "nominee;nominate;nominations;nominated;"
PRESENTER_KEYWORDS = "presents;presented;presentation;presenting;presenter;presenters;announcer;announced;announce"
MOTION_PICTURE_DRAMA_KEYWORDS = ""
# Probably could've scrapped some red carpet reporting on fashion for most frequent positve/negative words with Vader and used those... but time is of the essence. 
WORST_DRESS_KEYWORDS = "worst;bad;ugly;terrible;unfashionable;poor;poor taste;suit"
BEST_DRESS_KEYWORDS = "pretty;favorite;interesting;beautiful;stunning;elegant;nice;outfit;gorgeous;dress;suit;paints;shirt;couture"
##############
# Stop Words #
##############
# Can delete this late, loaded into script directly
# Imported from NLTK stopwords.english
STOP_WORDS = ['than', "isn't", 'weren', 'have', 'what', 'the', 'they', 'more', 'doesn', "mightn't", 'them', 'itself', 'own', 'or', 'you', 'theirs', 'before', 'how', 'were', 'does', 'ma', 'he', 'same', 'each', 'doing', 'at', 'couldn', "needn't", 'but', "weren't", 'only', 'over', 'again', 'any', 'now', 'here', 'no', 'mustn', 're', 'nor', 'so', "she's", 'above', 'against', "didn't", 'myself', 'an', 'ain', 'shouldn', 'where', 'their', 'won', 'yours', 'himself', 'further', 'i', 'this', 'didn', 'these', 'herself', 'both', 'her', 'aren', 'its', 'other', "wouldn't", "shan't", 'all', 'in', 'do', 'with', 'up', 'there', 'our', 'needn', 'such', 'while', 'too', "hasn't", "don't", 'below', 'ourselves', 'to', 've', "couldn't", 'because', 'down', "doesn't", 'is', 'if', 'wouldn', "aren't", 'who', "haven't", 'being', 'then', 'very', "should've", 'should', 'that', 'few', 'hadn', 'under', 'hasn', 'as', 'off', "won't", 'not', 'm', 'hers', 'a', "you've", 'him', 'yourself', 'she', 'on', 't', "hadn't", 'shan', 'of', 'about', 'it', "you're", 'why', 'are', 'through', 'between', 'having', 'whom', 'until', 'and', 'your', 'those', 'me', 'o', 's', 'ours', 'y', 'will', 'my', 'into', 'themselves', 'did', 'be', 'wasn', 'd', 'yourselves', "shouldn't", 'when', 'during', 'isn', "you'd", "wasn't", 'am', "it's", 'by', 'haven', 'been', 'can', "you'll", 'had', 'from', 'most', "that'll", 'don', 'out', 'for', 'after', 'some', 'we', 'his', 'once', 'has', 'was', 'mightn', 'just', 'll', "mustn't", 'which']
