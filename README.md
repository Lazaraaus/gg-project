# gg-project-master
Golden Globe Project Master


PAST YEAR REPOS WE LOOKED AT
https://github.com/kxuan763/gg-project-master/blob/master/gg_api.py
https://github.com/rromo12/EECS-337-Golden-Globes-Team-9
https://github.com/rkm660/GoldenGlobes
https://github.com/feelmyears/goldenglobes
https://github.com/liujjpp/nlp-proj1
https://github.com/kapil1garg/eecs337-team3-project1
https://github.com/Lukas-Justen/NLP-GoldenGlobes
https://github.com/KobraKid/NLP2019Awards


OUR REPOS
We switched our github repo near the end because we wanted to enable large file sharing
Original github repo: https://github.com/Lazaraaus/gg-project-master
LFS github repo: https://github.com/Lazaraaus/gg-project

1.) Install from requirements.txt
2.) In terminal, run: python -m spacy download en_core_web_sm. If using a virtual env remember to run within virtual environ

UPDATE 12/2
Thanks to Victor's help, we realized that we were not integrating our solution with the autograder.

We've edited how we output results. `pre_ceremony()` takes input from the terminal to determine which year it will use to process tweet information. It will load that year into a global variable. `main()` uses the global variable `YEAR` to write out our results for that year to a json file. Our program is now compatible with the autograder, meaning that all of our "get" methods will grab and return information from our output json file.