import json
import os
import time
from click import command, argument
from datetime import date
from abc import ABC, abstractmethod
"""
    Needs terminal-notifier installed. 
    Assumes user uses iTerm2.
"""

STORAGE_FILENAME = 'ratings.json'


@command()
@argument('minutes')
def start_timebox(minutes):
    storage = TimeboxStorage()
    terminal = Iterm2()
    timebox = Timebox(minutes=int(minutes), terminal=terminal, storage=storage)
    timebox.start()


class Storage(ABC):
    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def write(self, item):
        pass


class JsonStorage(Storage):
    def __init__(self, filename):
        self.filename = filename

    def get_items(self):
        try:
            with open(self.filename, 'r') as json_file:
                data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            data = {}
        return data

    def write(self, item):
        with open(self.filename, 'w') as target:
            json.dump(item, target)


class TimeboxStorage(JsonStorage):
    def __init__(self):
        super().__init__(filename=STORAGE_FILENAME)

    def add(self, timebox):
        today = str(date.today())
        ratings = self.get_items()
        try:
            ratings[today].append(timebox)
            print(ratings)
        except KeyError:
            ratings[today] = [timebox]
            print(ratings)
        self.write(ratings)


class Timebox:
    def __init__(self, minutes, terminal, storage):
        self.minutes = minutes
        self.seconds = minutes * 60
        self.terminal = terminal
        self.storage = storage
        self.rating = None

    def start(self):
        self.terminal.countdown(self.seconds, self.end)

    def end(self):
        self.terminal.notify_done()
        self.terminal.focus()
        self.rate()
        self.save()

    def save(self):
        timebox_item = self.itemize()
        self.storage.add(timebox_item)

    def rate(self):
        self.rating = input('Did it go well? (1-5): ')

    def itemize(self):
        return {
            "rating": self.rating,
            "duration": self.minutes,
            "timestamp": time.time()
        }


class Terminal(ABC):
    @abstractmethod
    def focus(selfs):
        pass

    @abstractmethod
    def notify_done(selfs):
        pass


class Iterm2(Terminal):
    def focus(self):
        os.system("""osascript -e 'tell application "iTerm 2" to activate'""")

    def notify_done(self):
        os.system(
            "terminal-notifier -title Timebox -message Finished -sound default"
        )

    def countdown(self, seconds, callback):
        os.system(f'termdown {seconds}')
        callback()


if __name__ == '__main__':
    start_timebox('25')
