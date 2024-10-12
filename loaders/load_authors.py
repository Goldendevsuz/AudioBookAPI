import json
import os
import sys
import django

# Set the root folder as the working directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AudioBook.settings.local')  # Replace with your project settings
django.setup()

from apps.author.models import Author  # Replace with your actual app name

# List of authors to be added
with open('loaders/authors.json') as f:
    authors_data = json.load(f)

# Create authors
for author_data in authors_data:
    author_name = author_data.get('name')
    author, created = Author.objects.get_or_create(name=author_name)
    if created:
        print(f'Created author: {author_name}')
    else:
        print(f'Author already exists: {author_name}')
