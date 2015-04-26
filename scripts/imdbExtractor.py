#!/usr/bin/env python

# Import the imdb package.
import imdb
import sys
import time
import random
import logging

cast_list = []
writers_list = []
genre_list = [] 

def fillCastList(cast):
  global cast_list
  count = 0
  for item in cast:
    cast_list.append(item)
    count += 1
  while count < 3:
    cast_list.append("")
    count += 1
  
def fillWritersList(writers):
  global writers_list
  count = 0
  for item in writers:
    writers_list.append(item)
    count += 1
  while count < 2:
    writers_list.append("")
    count += 1
  
def fillGenresList(genres):
  global genre_list
  count = 0
  for item in genres:
    genre_list.append(item)
    count += 1
  while count < 3:
    genre_list.append("")
    count += 1
 
def handleMovie(movie):
  # Search for a movie (get a list of Movie objects).
  s_result = ia.search_movie(movie)

  # Print the long imdb canonical title and movieID of the results.
  #for item in s_result:
  #   print item['long imdb canonical title'], item.movieID

  # Retrieves default information for the first result (a Movie object).
  try:
    the_unt = s_result[0]
    ia.update(the_unt)
  except:
    print >> log, ("Movie: %s not found" % movie)
    return

  # Print some information.
  try:
    title = the_unt['title']
  except KeyError:
    title = ""
    print >> log, "Movie: %s; Key: title" % movie

  try:
    lititle = the_unt['long imdb title']
  except:
    lititle = ""
    print >> log, "Movie: %s; Key: long imdb title" % movie

  try:
    ctitle = the_unt['canonical title']
  except:
    ctitle = ""
    print >> log, "Movie: %s; Key: canonical title" % movie

  try:
    lictitle = the_unt['long imdb canonical title']
  except:
    lictitle = ""
    print >> log, "Movie: %s; Key: long imdb canonical title" % movie

  try:
    year = the_unt['year']
  except:
    year = ""
    print >> log, "Movie: %s; Key: year" % movie

  try:
    kind = the_unt['kind']
  except:
    kind = ""
    print >> log, "Movie: %s; Key: kind" % movie

  try:
    director = the_unt['director'][0]
  except:
    director = ""
    print >> log, "Movie: %s; Key: director" % movie

  try:
    cast = the_unt['cast']
  except:
    cast = []
    print >> log, "Movie: %s; Key: cast" % movie

  try:
    writers = the_unt['writer']
  except:
    writers = []
    print >> log, "Movie: %s; Key: writer" % movie

  try: 
    runtime = the_unt['runtimes'][0]
  except:
    runtime = ""
    print >> log, "Movie: %s; Key: runtimes" % movie

  try:
    rating = the_unt['rating']
  except:
    rating = ""
    print >> log, "Movie: %s; Key: rating" % movie

  try:
    votes = the_unt['votes']
  except:
    votes = ""
    print >> log, "Movie: %s; Key: votes" % movie

  try:
    mpaa = the_unit['mpaa']
  except:
    mpaa = ""
    print >> log, ("Movie: %s; Key: mpaa" % movie)

  try:
    color = the_unt['color info'][0]
  except:
    color = ""
    print >> log, "Movie: %s; Key: color info" % movie

  try:
    countries = the_unt['countries'][0]
  except:
    countries = ""
    print >> log, "Movie: %s; Key: countries" % movie

  try:
    genres = the_unt['genres']
  except:
    genres = []
    print >> log, "Movie: %s; Key: genres" % movie

  try:
    akas = the_unt['akas'][0]
  except:
    akas = ""
    print >> log, "Movie: %s; Key: akas" % movie

  try:
    languages = the_unt['languages'][0]
  except:
    languages = ""
    print >> log, "Movie: %s; Key: languages" % movie

  try:
    certificates = the_unt['certificates'][0]
  except:
    certificates = ""
    print >> log, "Movie: %s; Key: certificates" % movie

  fillCastList(cast)
  fillWritersList(writers)
  fillGenresList(genres)


  try:
    print "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|" % (movie.encode('ascii', 'ignore'), title.encode('ascii', 'ignore'), lititle.encode('ascii', 'ignore'), ctitle.encode('ascii', 'ignore'), lictitle.encode('ascii', 'ignore'), year, kind.encode('ascii', 'ignore'), director, runtime.encode('ascii', 'ignore'), rating, votes, mpaa.encode('ascii', 'ignore'), color.encode('ascii', 'ignore'), countries.encode('ascii', 'ignore'), akas.encode('ascii', 'ignore'), languages.encode('ascii', 'ignore'), certificates.encode('ascii', 'ignore'), "Attribute"), 
    print "%s|%s|%s|%s|%s|%s|%s|%s" % (cast_list.pop(0), cast_list.pop(0), cast_list.pop(0), writers_list.pop(0), writers_list.pop(0), genre_list.pop(0), genre_list.pop(0), genre_list.pop(0))
    #print "%s|%s|%s|%s|%s|%s|%s|%s" % (cast_list.pop(0)['name'].encode('ascii', 'ignore'), cast_list.pop(0)['name'].encode('ascii', 'ignore'), cast_list.pop(0)['name'].encode('ascii', 'ignore'), writers_list.pop(0)['name'].encode('ascii', 'ignore'), writers_list.pop(0)['name'].encode('ascii', 'ignore'), genre_list.pop(0)['name'].encode('ascii', 'ignore'), genre_list.pop(0)['name'].encode('ascii', 'ignore'), genre_list.pop(0)['name'].encode('ascii', 'ignore'))
  except:
    #print logging.exception('')
    print >> log, "Failed to print info for movie %s" % movie
    print 

# Create the object that will be used to access the IMDb's database.
ia = imdb.IMDb() # by default access the web.

log = open ("log", "w+")
with open(sys.argv[1]) as inputFile:
  for line in inputFile:
    movie = line.strip()
    #time.sleep(random.randint(1, 5))
    handleMovie(movie)

log.close()
inputFile.close()
