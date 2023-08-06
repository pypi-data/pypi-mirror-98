#!/usr/bin/env python3

import os
import sys
import random
from playsound import playsound

def PlaySongs(path, repeat = 0, shuffle = False):

    try:
        # Create the list of files from a directory of songs.
        file_list = os.listdir(path)
        # Filter list to only include MP# files.
        song_list = [i for i in file_list if i.endswith('.mp3')]
    except Exception as e:
        return str(e)

    # Initialize repeat counter.
    counter = 0

    # Play all songs and repeat as necessary.
    while counter <= repeat:

        # Shuffle list if necessary.
        if shuffle is True:
            random.shuffle(song_list)

        try:
            # Play songs.
            for song in song_list:
                print('Playing: {}/{}...'.format(path, song))
                playsound('{}/{}'.format(path, song))
        
        except KeyboardInterrupt:
            print('Stopped')
            sys.exit(1)
        
        except Exception as e:
            return str(e)
        
        # Increment counter.
        counter += 1

    return 'Done'
