#!/usr/bin/python3
import os
import re
import sys
import time
import random
import datetime
import threading

import vlc
import pafy
import argparse
from pypresence import Presence

import tools


Song = tools.Song


class Player():
    '''Main player class

    args:
        songs (list, str):      one or more song titles/urls
        playlists (list, str):  one or more urls to youtube playlists/paths to local playlist files
        shuffle (bool):         whether or not to randomise the song queue
        volume (int >= 0):      volume level (>100 gets distorted and LOUD)
        rich_presence (bool):   whether or not to use discord rich presence to display the current song
        muted (bool):           whether or not to start the player muted
        enable_input (bool):    whether or not to allow users to control the player through commandline input
        vlclogs (bool):         whether or not to print VLC logs
        debuglogs (bool):       whether or not to print pYTerm debug logs
        legacystreams (bool):   whether or not to use legacy streams, enable if some songs dont load
        '''
    # vvv variables that can't be changed in initialisation
    rich_presence_id = '737813623967318077'
    curren_song = None
    songs = []
    song_index = 0
    exiting = False
    muted = False
    pending_action = False
    input_commands = { # all user input commands and their corrosponding action
        'next': lambda self,cmd: self.next(),
        'previous': lambda self,cmd: self.previous(),
        'scrub': lambda self,cmd: self.scrub(int(cmd[0])),
        'pause': lambda self,cmd: self.toggle_pause(),
        'mute': lambda self,cmd: self.toggle_mute(),
        'goto': lambda self,cmd: self.play_at_index(int(cmd[0])),
        'volume': lambda self,cmd: self.set_volume(int(cmd[0])),
        'exit': lambda self,cmd: self.stop(),
    }
    def __init__(self,
                songs           = None,     # list of song titles/urls or single song title/url
                playlists       = None,     # list of urls to youtube playlist/paths of local playlist file or single url to youtube playlist/path of local playlist file
                shuffle         = False,    # whether or not to randomise the song queue
                volume          = 100,      # starting volume
                muted           = False,    # whether or not to start the player muted
                rich_presence   = True,     # whether or not to use discord rich presence to display the current song
                enable_input    = True,     # whether or not to allow users to control the player through commandline input
                vlclogs         = False,    # whether or not to print VLC logs
                debuglogs       = False,    # whether or not to print pYTerm debug logs
                legacystreams   = False,    # whether or not to use legacy streams, disabling might improve sound quality at the cost of some songs not working
                ):
        self.shuffle            = shuffle
        self.volume             = volume
        self.rich_presence      = rich_presence
        self.enable_input        = enable_input
        self.vlclogs            = vlclogs
        self.debuglogs          = debuglogs
        self.legacystreams      = legacystreams
        self.vlc                = vlc.Instance('--no-video', 'vout=none') # vlc instance, really only needed to spawn the player and create media objects, but handy to keep around ig
        self.vlc_player         = self.vlc.media_player_new()
        if songs:               self.add_song(songs)
        if playlists:           self.add_playlist(playlists)
        if not vlclogs:         os.environ['VLC_VERBOSE'] = '-1' # sets the env var for vlc logging to -1, seems to not obey it fully tho :\
        if self.rich_presence:
            try:
                self.rich_presence_client = Presence(self.rich_presence_id)
                self.rich_presence_client.connect()
            except:
                pass
        if self.enable_input:
            threading.Thread(target=self.run_input, daemon=True).start()


    def play(self, song, halting = False):
        '''Play a single song

            args:
                song (str, Song):       keyword or url of a song on YouTube
                halting = False (bool): set to False to not halt the program
        '''
        if type(song) != Song:
            song = tools.get_song_obj(song)
        self.current_song = song
        stream_url = song.get_stream(legacy = self.legacystreams)
        vlc_media = self.vlc.media_new(stream_url, 'vout=none', '--no-video')
        self.vlc_player.set_media(vlc_media)
        self.vlc_player.play()
        if self.muted:
            self.vlc_player.audio_set_volume(0)
        else:
            self.vlc_player.audio_set_volume(self.volume)
        while not self.vlc_player.is_playing():
            time.sleep(0.05)
            # wait for song to load
        if song.length == None:
            song.length = int(self.vlc_player.get_length()/100)
            # if song is missing length attribute, get it from vlc
        self.info(f'Playing {song.title} by {song.artist} [{song.length}]')
        if halting:
            time.sleep(self.vlc_player.get_length()/100)


    def play_all(self, halting = False, **kwargs):
        '''play entire song queue.

        args:
            halting = False (bool):     set to False to not halt the program
            keep_alive = True (bool):   keep loop running even when the queue has ended, useful if you want to add more songs later
            loop = False (bool):        whether or not to restart the song queue once its played the final song
            '''
        def run(self, keep_alive = False, loop = False):
            while True:
                while self.song_index < len(self.songs) or loop:
                    self.play_current_song(halting = False)
                    while self.is_vlc_alive(): # loop while the song is playing to update discord
                        self.update_rich_presence()
                        time.sleep(0.5)
                    if self.exiting: return
                    if self.pending_action:
                        self.pending_action = False
                    else:
                        self.increment_song_index(wrap = loop)
                if not keep_alive:
                    break
        x = threading.Thread(target=run, daemon=True, args=(self,), kwargs=kwargs)
        if halting:
            x.run()
        else:
            x.start()


    def increment_song_index(self, positive=True, wrap=True):
        '''increments or decrements the `song_index` by one, with optional wrapping'''
        number = -1+(2*bool(positive))
        new_index = self.song_index + number
        queue_length = len(self.songs)
        if new_index >= queue_length and wrap:
            new_index = new_index - (queue_length-1)
        elif new_index < 0:
            if wrap:
                new_index = new_index + (queue_length-1)
            else:
                new_index = 0
        self.song_index = new_index


    def run_input(self):
        '''allows user input. halts if called, initialise Player with `enable_input = True` to not halt'''
        def ignore(*args, **kwargs):
            print('ignored')
        while self.enable_input:
            full = input(':').split(' ')
            if len(full) > 1:
                key = full[0]
                cmd = full[1:]
            else:
                key = full[0]
                cmd = ''
            try:
                self.input_commands.get(key,ignore)(self,cmd)
            except Exception as e:
                print(e)

    def stop(self):
        '''Stops player and exits'''
        self.exiting = True
        self.vlc_player.stop()


    def next(self):
        '''play next song in the queue'''
        # self.pending_action = True
        # self.increment_song_index()
        self.vlc_player.stop()


    def previous(self):
        '''play previous song in the queue'''
        self.pending_action = True
        self.increment_song_index(positive = False)
        self.vlc_player.stop()


    def play_at_index(self, index):
        '''plays the song at the given position in the queue'''
        self.pending_action = True
        self.song_index = index
        self.vlc_player.stop()


    def pause(self):
        '''pauses the player'''
        self.set_volume(0, desync_volume=self.volume)
        self.vlc_player.set_pause(1)

    def unpause(self):
        '''unpauses the player'''
        self.set_volume(self.volume, desync_volume=0)
        self.vlc_player.set_pause(0)

    def toggle_pause(self):
        '''toggles between paused and unpaused player'''
        if self.is_vlc_alive():
            if self.vlc_player.is_playing():
                self.pause()
            else:
                self.unpause()


    def toggle_mute(self):
        '''toggles between muted and unmuted player'''
        if self.muted:
            self.unmute()
        else:
            self.mute()

    def mute(self):
        '''mutes player and fades music out'''
        if not self.muted:
            self.set_volume(0, desync_volume=self.volume)
            self.muted = True
            self.debug('muted')

    def unmute(self):
        '''unmutes player and fades music back in'''
        if self.muted:
            self.muted = False
            self.set_volume(self.volume, desync_volume=0)
            self.debug('unmuted')


    def scrub(self,seconds):
        '''scrub the current song left or right in seconds

        args:
            seconds (int): positive or negative int indicating seconds to fast forward/backwards
        '''
        self.vlc_player.set_time(round(self.vlc_player.get_time() + seconds * 1000))


    def set_volume(self, new_volume, fadetime=0.5, desync_volume=None):
        '''change volume smoothly over `fadetime` seconds

        args:
            new_volume (int): volume to transition to
            fadetime (foat): transition time in seconds
            desync_volume (int): don't use this, its for muting
        '''
        current_volume = self.volume
        if desync_volume != None:
            current_volume = desync_volume
        if (new_volume != self.volume or desync_volume != None) and 200 >= new_volume >= 0:
            if fadetime and not self.muted:
                if new_volume > current_volume:
                    step = +1
                else:
                    step = -1
                fadedelay = fadetime / abs(new_volume - current_volume)
                for i in range(current_volume, new_volume, step):
                    self.vlc_player.audio_set_volume(i)
                    time.sleep(fadedelay)

            if not self.muted: self.vlc_player.audio_set_volume(new_volume)
            if desync_volume == None:
                self.volume = new_volume


    def play_current_song(self,*args,**kwargs):
        '''play queue song at the current index'''
        self.play(self.songs[self.song_index],*args,**kwargs)


    def shuffle(self):
        '''shuffle song queue'''
        random.shuffle(self.songs)
        self.song_index = 0


    def add_song(self, songs):
        '''Add one or multiple songs to the queue

        args:
            songs (list, str): one or more songs or youtube urls to add to the queue
        '''
        songs = tools.ensure_list(songs)
        out = []
        for song in songs:
            out.append(tools.get_song_obj(song))
        if self.shuffle: random.shuffle(out)
        self.songs += out


    def add_playlist(self, playlists):
        '''Checks type of playlist and hands it off to the right function,
        which will then add it's songs to the queue

        args:
            playlists (str, list): one or more urls to youtube playlists or paths to local playlist files
        '''
        playlists = tools.ensure_list(playlists)
        for playlist in playlists:
            playlist = str(playlist)
            if tools.is_url(playlist):
                if tools.is_youtube_url(playlist):
                    self.add_youtube_playlist(playlist)
                else:
                    self.add_local_playlist(playlist)
            else:
                self.add_youtube_playlist(tools.url_from_playlist_search(playlist))


    def add_youtube_playlist(self, url):
        '''Adds songs from a youtube playlist to the queue

        args:
            url (str): url to youtube playlist
        '''
        songs = tools.songs_from_yt_playlist(url)
        if self.shuffle:
            random.shuffle(songs)
        self.songs += songs


    def add_local_playlist(self, file):
        '''Adds songs from a local playlist file to the queue.
        playlist files are a list of youtube URLs or search words, with each entry on its own line

        args:
            file (str): path to local playlist file
        '''
        with open(file,'r') as f:
            lines = f.read().split('\n')
        songs = []
        for line in lines:
            if line[0] != '#' and len(line) > 1:
                songs.append(line)
        if self.shuffle:
            random.shuffle(songs)
        self.add_song(songs)


    def is_vlc_alive(self):
        """returns true if vlc is either paused or playing"""
        try:
            if str(self.vlc_player.get_state()) == 'State.Playing' or str(self.vlc_player.get_state()) == 'State.Paused':
                return True
            else:
                return False
        except:
            return False


    def debug(self, *args):
        '''Print debug-level log'''
        if self.debuglogs:
            print('[DBUG] ', *args, sep='')


    def info(self, *args):
        '''Print info-level log'''
        print('[INFO] ', *args, sep='')


    def update_rich_presence(self):
        '''Update discord rich presence if `self.rich_presence == True`'''
        if self.rich_presence:
            try:
                self.rich_presence_client.update(details=self.current_song.title, state=f'by '+self.current_song.artist, large_image="logo-2",
                                            small_image='clock', small_text=f'bro idk yet/{self.current_song.length}', large_text=';)')
            except:
                self.rich_presence = False


def get_args():
    '''Parses argparse arguments from commandline and returns the namespace object mapped to the correct .play_all() and Player() kwargs'''
    parser = argparse.ArgumentParser(
                        description="Play youtube audio from the commandline / écouter l'audio des vidéos youtube sur la ligne de commande")
    parser.add_argument('--version', help='Prints version / version imprimé', action='store_true')
    parser.add_argument('-v', '--volume',
                        help='Starts with <value> volume / le programme démarrer avec un niveau de volume <value>',
                        action='store', type=int, default=100)
    parser.add_argument('-l', '--loop', help='Enable queue looping', action='store_true')
    parser.add_argument('-s', '--shuffle', help='Enable queue shuffling', action='store_true')
    parser.add_argument('-p', '--playlist', help="Add local or youtube playlist / utiliser une playlist à partir d'un fichier",
                        action='append', type=str, dest='playlists')

    parser.add_argument('--nopresence', dest='rich_presence',
                        help='Disable discord rich presence', action='store_false')
    parser.add_argument('--muted', dest='muted',
                        help='Start player muted', action='store_true')
    parser.add_argument('--noinput', help='Disable player controls / désactiver les contrôles',
                        action='store_false', dest='enable_input')
    parser.add_argument('--legacy', dest='legacystreams', action='store_true',
                        help='Forces the use legacy streams, use this if some songs dont load')
    parser.add_argument('--verbose', help='Enable debug logging', action='store_true', dest='debuglogs')
    parser.add_argument('--vlclogs', help='Enable vlc logging', action='store_true')
    parser.add_argument('songs', help='Name or url of the song(s) you want to play / nom de la chanson à jouer tu veux jouer',
                        action='store', type=str, nargs=argparse.REMAINDER)
    # parser.add_argument('--fr', help='enable french output / activer mode français', action='store_true')
    # french isnt a thing in this version yet, need to have a proper translation system
    return parser.parse_args()


def commandline():
    '''Handles arguments if run from the commandline'''
    name_args = get_args()
    dict_args = vars(name_args)

    # version and loop are not kwargs for the player object, so gotta get them out before passing it along
    if dict_args['version']:
        print('rewrite 2, v0.5?')
        return
    else:
        del dict_args['version']
    loop = dict_args['loop']
    del dict_args['loop']
    player = Player(**dict_args)
    player.play_all(halting=True, loop=loop) # halting = True so it runs until the queue ends

if __name__ == '__main__':
    commandline()
