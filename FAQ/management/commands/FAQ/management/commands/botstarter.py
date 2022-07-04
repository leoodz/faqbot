from time import sleep
import psutil
from subprocess import Popen
from django.core.management import BaseCommand
from base_connect import DBConnector

db = DBConnector()


def set_from_tuple(db_tuple):
    """Converting a tuple from a query to a set"""
    return {x[0] for x in db_tuple}


class Command(BaseCommand):
    """Class to run script via manage.py"""
    help = 'Launching the Bot Manager'

    def handle(self, *args, **options):
        bm = BotsManager()
        bm.kill_process(bm.tokens)
        bm.run_process(bm.tokens)
        bm.update_checker()


class BotsManager:
    """A class to control the start and stop of bots"""

    def __init__(self):
        self.tokens = db.get_bot_tokens()

    def update_checker(self):
        """Loop checking token refresh"""
        while True:
            db.__init__()
            if self.tokens == db.get_bot_tokens():
                print('No token updates')
            else:
                self.update(self.tokens, db.get_bot_tokens())
                print('Tokens updated')
            sleep(5)

    def update(self, old_tokens, new_tokens):
        """Ends the process of the token removed from the database, and starts the process for the added one"""
        killer_set = old_tokens - new_tokens
        run_set = new_tokens - old_tokens
        self.kill_process(killer_set)
        self.kill_process(run_set)
        self.run_process(run_set)
        self.__init__()

    def kill_process(self, *args):
        """Stopping processes by bot token"""
        for i in args[0]:
            process_command = ['python3', 'manage.py', 'app', i]
            for process in psutil.process_iter():
                if process.cmdline() == process_command:
                    print('Process found, disable')
                    process.terminate()

    def run_process(self, *args):
        """Launching processes by bot token"""
        for i in args[0]:
            process_command = ['python3', 'manage.py', 'app', i]
            Popen(process_command)
