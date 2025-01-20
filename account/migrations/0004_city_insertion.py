# account/migrations/xxxx_populate_indian_districts.py

from django.db import migrations
import csv

def populate_indian_districts(apps, schema_editor):
    # Get the City model
    City = apps.get_model('account', 'City')
    
    # Open the CSV file containing districts and pin codes
    with open('./indian_districts.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Iterate through the CSV and insert each row into the City model
        for row in reader:
            district_name = row['district_name']
            
            # Insert each city and pin code into the database
            City.objects.get_or_create(name=district_name)

def reverse(apps, schema_editor):
    # Optionally, you can write a reverse function to remove the added cities if the migration is rolled back
    City = apps.get_model('account', 'City')
    City.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_city_user_city'),  # Replace with your last migration file
    ]

    operations = [
        migrations.RunPython(populate_indian_districts, reverse_code=reverse),
    ]
