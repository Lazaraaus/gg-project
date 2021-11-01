import time
import csv


def get_names():
    # dict for names
    name_dict = {}
    # Src Path
    src_path = 'name_data.tsv'
    # get name_dict
    with open(src_path, "r") as f:
        rd = csv.reader(f, delimiter="\t")
        # Get Relevant Years
        for year in range(2012, 2021):
            name_dict[str(year)] = []
        # Loop through info
        for row in rd:
            # Get relevant fields [name, birthyear, deathyear]
            primaryName = row[1]
            birthYear = row[2]
            deathYear = row[3]

            # Check if nonsense data for birth
            if (birthYear == "\\N"):
                # If so, skip
                continue

            # Check if Alive
            if (deathYear == "\\N"):
                # If so, active until 2021
                active = range(int(birthYear), 2021)
            else:
                # If not, active until deathYear
                active = range(int(birthYear), int(deathYear))
        
            # Evidently people can die before they were born, need to check for that BS
            if active.start > active.stop:
                # Reincarnation I think not
                continue

            # Only care about range within our testing suites [2012 - 2020]
            if active.start < 2012 and active.stop < 2012:
                # If outside, don't need
                continue
        
            # Reset start year for actors/actresses still active but start was before target year
            if active.start < 2012:
                # Set to start 2012
                active = range(2012, active[-1])
            # Add actor/actress to dict for each year in which they were active        
            for year in active:
                name_dict[str(year)].append(primaryName)

        return name_dict

def get_movies_and_series():
    # Start Timer
    timer = time.time()
    # dict for movies
    movie_dict = {}
    genre_movie_dict = {}
    # dict for series
    series_dict = {}
    genre_series_dict = {}
    # Src Path
    src_path = 'title_data.tsv'
    src_path_debug = "/home/yjaden/Courses/337/gg-project/utilities/title_data.tsv"
    # get name_dict
    with open(src_path_debug, "r") as f:
        rd = csv.reader(f, delimiter="\t")
        # Get Relevant Years
        for year in range(2012, 2021):
            series_dict[str(year)] = []
            movie_dict[str(year)] = []
            genre_movie_dict[str(year)] = []
            genre_series_dict[str(year)] = []

        # Loop through info
        for row in rd:
            # Skip Adult Films
            if row[4] == 1:
                continue 

            # Check if Movie
            elif row[1] == 'movie':
                # Movies
                # Get relevant fields [title, startyear, endyear]
                primaryTitle = row[2]
                startYear = row[5]
                endYear = row[6]
                genres = row[8]

                # Check if nonsense data for start
                if (startYear == "\\N"):
                    # If so, skip
                    continue
                # Check if before what we care about
                if (int(startYear) < 2012):
                    continue
                # Check if after what we care about
                if (int(startYear) > 2020):
                    continue
                # Append to movie_dict
                movie_dict[str(startYear)].append(primaryTitle)  
            
                # Check for genre
                if genres != "\\N":
                    # Split str into list
                    genres = genres.split()
                    # Append list to dict
                    genre_movie_dict[str(startYear)].append(genres)
                else:
                    # Append None
                    genre_movie_dict[str(year)].append(None)

            # Check if Series
            elif row[1] == 'tvSeries':
                # Series
                # Get relevant fields [title, startyear, endyear]
                primaryTitle = row[2]
                startYear = row[5]
                endYear = row[6]
                genres = row[8]

                # Check if nonsense data for start
                if (startYear == "\\N"):
                    # If so, skip
                    continue

                # Check if after what we care about
                if (int(startYear) > 2020):
                    continue

                # Check if ended
                if (endYear == "\\N"):
                    # If so, airing until 2021
                    active = range(int(startYear), 2021)
                else:
                    # If not, aired until endYear
                    if int(endYear) <= 2020:
                        # Make sure it's within bounds
                        active = range(int(startYear), int(endYear))
                    else:
                        active = range(int(startYear), 2020)
        
                # Evidently people can die before they were born, need to check for that BS
                if active.start > active.stop:
                    # Reincarnation I think not
                    continue

                # Only care about range within our testing suites [2012 - 2020]
                if active.start < 2012 and active.stop < 2012:
                    # If outside, don't need
                    continue
        
                # Reset start year for series still active but start was before target year
                if active.start < 2012:
                    # Set to start 2012
                    active = range(2012, active[-1])

                # Check for genres
                if genres != "\\N":
                    # Split Genres
                    genres = genres.split()
                    # Add the genres for each year show was running
                    for year in active:
                        genre_series_dict[str(year)].append(genres)
                else:
                    # Otherwise append None
                    for year in active:
                        genre_series_dict[str(year)].append(None)
                       
                # Add series to dict for each year in which it ran        
                for year in active:
                    series_dict[str(year)].append(primaryTitle) 

        time_passed = str(time.time() - timer)
        print(f"Time taken: {time_passed}")

        return series_dict, movie_dict, genre_series_dict, genre_movie_dict
