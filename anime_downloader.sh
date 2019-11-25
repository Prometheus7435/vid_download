#!/bin/bash

# echo "What's your name?"
# read user_name
echo "Enter site where series is"
read thing
# info=$(python test.py $thing)
info=$(python anime_download.py $thing)
echo $info
echo $info | read $var1 $var2
echo $var1
echo $var2
# echo $info
# echo $(python anime_download.py $thing)
# echo "Greetings $info. It's nice to meet you"
