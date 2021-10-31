import pandas as pd

# # Load Data into CSV
# name_data = pd.read_csv("data.tsv", sep = "\t")
# # Convert to numeric, N/A values should be coerced to NaN
# name_data["birthYear"] = pd.to_numeric(name_data["birthYear"], errors="coerce")
# name_data["deathYear"] = pd.to_numeric(name_data["deathYear"], errors="coerce")
# # Fill death year with a dummy value
# name_data["deathYear"] = name_data["deathYear"].fillna(2050)

# # Filter out data that is not useful
# name_data = name_data[name_data["primaryProfession"].notna()]
# name_data = name_data[name_data["birthYear"].notna()]
# name_data = name_data[name_data.deathYear > 2012]

# # Separate into actors, actresses
# actor_names = name_data[name_data.primaryProfession.str.contains('actor')]
# actress_names = name_data[name_data.primaryProfession.str.contains('actress')]
# # Print Lens
# print(len(actor_names))
# print(len(actress_names))
# # Print first 30 values
# print(actor_names.head(30))
# print(actress_names.head(30))
# # Output to CSV
# actor_names.to_csv('actor_names.csv')
# actress_names.to_csv('actress_names.csv')





# JOB_LIST = ["actor", "actress", "director", "writer"]
# # Load Necessary CSVs
# # Load Actors, Actresses Name data
# name_data_actors = pd.read_csv('actor_names.csv')
# name_data_actresses = pd.read_csv('actress_names.csv')
# # Concata actors, actresses
# frames = [name_data_actors, name_data_actresses]
# name_data = pd.concat(frames)
# Load Title Data into CSV
title_data = pd.read_csv('title_data.tsv', sep="\t")
# Load Title Principal Data
#title_principal_data = pd.read_csv('title_principal_data.tsv', sep="\t")


# Adjust to numeric values
title_data["startYear"] = pd.to_numeric(title_data["startYear"], errors="coerce")
title_data["endYear"] = pd.to_numeric(title_data["endYear"], errors="coerce")
title_data["runtimeMinutes"] = pd.to_numeric(title_data["runtimeMinutes"], errors="coerce")
title_data["isAdult"] = pd.to_numeric(title_data["isAdult"], errors="coerce")

# Filter out data that is not useful
#title_data = title_data[title_data.titleType == '']
title_data = title_data[title_data.primaryTitle ==  "30 Rock"]
# title_data = title_data[title_data.startYear < 2015]
# title_data = title_data[title_data.isAdult != 1]
# title_data = title_data[title_data.runtimeMinutes < 40]
# Print for confirmation
print(title_data.head(30))
print(len(title_data))
# # Load titles into list
# title_list = title_data["tconst"].to_list()


# # Filter out useless data
# title_principal_data = title_principal_data[title_principal_data.tconst.isin(title_list)]
# title_principal_data = title_principal_data[title_principal_data.category.isin(JOB_LIST)]
# # Print for confirmation
# print(len(title_principal_data))
# print(title_principal_data.dtypes)
# print(title_principal_data.head(30))

# # Get actor and actress list of names
# #actor_name_list = name_data_actors["nconst"].to_list()
# #actress_name_list = name_data_actresses["nconst"].to_list()
# # Combine into single list
# name_list_all = name_data["nconst"].to_list() #actor_name_list + actress_name_list
# # Filter Title Principal Data with name data
# title_principal_data = title_principal_data[title_principal_data.nconst.isin(name_list_all)]
# # Print for confirmation
# print(len(title_principal_data))
# print(title_principal_data.head(30))