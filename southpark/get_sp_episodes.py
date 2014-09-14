from bs4 import BeautifulSoup
import urllib2
import re
import os
import  shutil


#get all seasons
def south_park_seasons():
  url = "http://southpark.wikia.com/wiki/Portal:Scripts"
  content = urllib2.urlopen(url).read()
  soup = BeautifulSoup(content)
  seasons = []
  seasons_pre = soup.find_all(id="gallery-0")
  links = seasons_pre[0].find_all('a')
  counter = 0
  while counter < len(links):
    if counter == 0:
     counter = counter + 1
    else:
      seasons.append(links[counter].get('href'))
      counter = counter + 2
  return seasons

 #get all info for all seasons
def get_all_episodes(seasons):
  print seasons
  all_seasons = {}
  ##loop through the seasons
  for season in seasons:
  #for season in seasons[0:1]:
    episodes = []
    season_pieces = season.split("/")
    season_name = season_pieces[-1]
    season_url   = 'http://southpark.wikia.com/wiki/' +season_pieces[-1]
    print "*****"
    print season_url
    print "****"
    season_content =  urllib2.urlopen(season_url ).read()
    soup_season = BeautifulSoup(season_content)
    stuff = soup_season.find_all("table")
    tb_rows = stuff[1].find_all("tr")
    tb_rows_len = len(tb_rows)
    counter = 0
    while tb_rows_len > counter+1:
      episode = []
      if counter == 0:
        counter = counter + 1
      else:
        #season name and url
        episode.append(season_name)
        episode.append(season_url)
        tds1 =    tb_rows[counter].find_all("td")
        tds2 =    tb_rows[counter+ 1].find_all("td")
        #episode name
        for link in tds1[1].find_all("a"):
          episode_name = link.get("title")
          episode_name = re.sub("'", "", episode_name)
          episode.append(episode_name)
        #link to script for episode
        for link in tds1[1].find_all("a"):
          script_link =  "http://southpark.wikia.com" + link.get('href') + "/Script"
          episode.append(script_link)
        #link to image for episode
        for link in tds1[0].find_all("a"):
            image_link =  link.get('href')
            episode.append(image_link)
        #get the air_date
        for item in tds1[2]:
          airdate  = item
          episode.append(str(airdate[:-1]))
        description =  tds2[0].find('p')
        description = description.string
        if not (description is None):
          description = description[:-1]
        episode.append(description)
        episodes.append(episode)
        counter =  counter + 2
      #print episodes
      all_seasons[season_name] =  episodes
  return all_seasons
#make the base dir to store all scripts for all seasons
def make_basedir(basedir):
  if os.path.exists(basedir):
    shutil.rmtree(basedir)
  os.makedirs(basedir)

#make an episode guide that you can load into a db
def make_episode_guide(basedir, all_seasons):
  base_file = open(basedir + "southpark_episode_guide_all_seasons.txt", 'w')
  base_file.write("season |||| link_to_season,episode_name ||||  episode link_to_script, image_link |||| air_date |||| description" + "\n")
  for season, episodes in all_seasons.items():
    for episode_row in episodes:
      row =  '||||'.join(episode_row)+ "\n"
      base_file.write(row)
  base_file.close

def make_season_dirs(basedir, season):
  make_basedir(basedir + season.lower())
  make_basedir(basedir + season.lower()+ "/plaintxt")
  make_basedir(basedir + season.lower()+ "/html")

#gets the actual episode script
def get_episode_script(episode_row):
  episode_url = episode_row[3]
  print "******"
  print episode_url
  print "******"
  content = urllib2.urlopen(episode_url).read()
  soup = BeautifulSoup(content)
  script_pre = soup.find_all(id="WikiaArticle")
  all_divs =  script_pre[0].find_all("div")
  script_div = all_divs[2]
  print script_div.find("h2").string

####Main#####
seasons = south_park_seasons()
all_seasons = get_all_episodes(seasons[0:1])
basedir = "southpark_scripts/"
#make a basedir to store all the seasons
make_basedir(basedir)
#make an episode guide for all the seasons
make_episode_guide(basedir, all_seasons)

#iterate through the seasons and grab all the scripts for each season
for season, episodes in all_seasons.items():
  make_season_dirs(basedir, season)
  #for episode_row in episodes:
    #get_episode_script(episode_row)
  get_episode_script(episodes[0])






#for each season, mk a dir
  #for each episode, make a file- put description at top of file


    #  print "****End****"
##csv file

