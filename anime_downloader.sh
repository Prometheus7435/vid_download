#!/bin/bash

# echo "What's your name?"
# read user_name
echo "Enter site where series is"
read var
# info=$(python test.py $thing)
info=$(python anime_download.py $var)
# echo $info
# echo $info | read $genre $series $save_loc
# echo $genre
# echo $series
# echo $save_loc

# IFS=' '
#Read the split words into an array based on comma delimiter
IFS=" " read genre series save_loc <<< "$info"
# echo $genre
# echo $series
# # echo $synop
# echo $save_loc


echo $genre $series $save_loc
# while ! [find $save_loc -maxdepth 1 -type f -exec ".part$" {}]
# while ! [grep -i ".part" $save_loc]
# do
#     echo grep -i ".part" $save_loc
#     # find $save_loc -maxdepth 1 -type f -exec ffmpeg -i {} -metadata genre=$genre .{} \; 
#     # find $save_loc -maxdepth 1 -type f -exec rm {} \;
# done



find $save_loc -maxdepth 1 -type f -exec ffmpeg -i {} -metadata genre=$genre .{} \; 
# find $save_loc -maxdepth 1 -type f -exec rm {} \;


# echo $info
# echo $(python anime_download.py $thing)
# echo "Greetings $info. It's nice to meet you"
# ffmpeg -i inputfile -metadata title="Movie Title" -metadata year="2010" outputfile

# from ffmpeg wiki 
# Key 	iTunes field 	Low-level identifier
# "title" 	Name 	'\251nam'
# "author" 	Artist 	'\251ART'
# "album_artist" 	Album Artist 	'aART'
# "album" 	Album 	'\251alb'
# "grouping" 	Grouping 	'\251grp'
# "composer" 	Composer 	'\251wrt'
# "year" 	Year 	'\251day'
# "track" 	Track Number 	'trkn'
# "comment" 	Comments 	'\251cmt'
# "genre" 	Genre 	'\251gen'
# "copyright" 	?? 	'\251cpy'
# "description" 	Description 	'desc'
# "synopsis" 	Information dialog when selecting "Show Description" in context menu 	'ldes'
# "show" 	Show 	'tvsh'
# "episode_id" 	Episode ID 	'tven'
# "network" 	?? 	'tvnn'
# "lyrics" 	Lyrics 	'\251lyr'
