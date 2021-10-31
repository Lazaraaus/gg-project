import time
import csv
name_dict = {}

def get_names():
    # Start Timer
    timer = time.time()
    # Src Path
    src_path = 'name_data.tsv'
    # get name_dict
    with open(src_path, "r") as f:
        rd = csv.reader(f, delimiter="\t")
        # Get Fields
        name_fields = next(rd)
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

        time_passed = str(time.time() - timer)
        print(f"Time taken: {time_passed}")

get_names()