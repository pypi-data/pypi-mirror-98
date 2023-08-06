from django.core.management.base import BaseCommand, CommandError
import os
from generator_app.app import app

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', type=str, help='Django app path')
        parser.add_argument('-m', '--mode', type=str, help='Mode to read file, choose (model) or (json)')

    def handle(self, *args, **options):
        path = self.default_path(options['path'])
        self.stdout.write('Generate CRUD from path {}'.format(path))
        app(path, self.default_mode(options['mode']))
        # self.stdout.write('Successfully generate crud {} {}'.format(path, options['mode']))


    def default_path(self, path : str) -> str:
        if not path:
            return os.getcwd()
        else:
            return os.getcwd() + '/' + path 

    def default_mode(self, mode : str) -> str:
        return 'model' if mode == 'model' else 'json' 

    