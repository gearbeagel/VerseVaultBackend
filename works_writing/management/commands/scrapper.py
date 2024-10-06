import json
import os
from django.core.management.base import BaseCommand
from works_writing.models import Tag


class Command(BaseCommand):
    help = 'Import tags from a pre-set JSON file into the database'

    def handle(self, *args, **kwargs):
        # Construct the absolute path to the JSON file
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../tags.json'))

        print(f'Trying to open file at: {file_path}')  # Debug print

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Iterate over each tag and save to the database
            for tag_data in data['tags']:
                tag = Tag()
                for key, value in tag_data.items():
                    setattr(tag, key, value)
                tag.save()

            self.stdout.write(self.style.SUCCESS('Successfully imported tags from JSON'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File {file_path} not found'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Error decoding JSON in file {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
