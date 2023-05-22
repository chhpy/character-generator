#region imports
import json
import random
import os
import csv
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

#endregion imports

#region functions

# images
def generate_images():

    folder_path = 'json' 

    # Font settings
    font_size = 18
    font_color = (255, 255, 255)  # White color
    font_path = 'font/cour.ttf'

    # Image settings
    image_width = 400
    image_height = 210
    background_color = (0, 0, 0)  # Black color

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Iterate over the JSON files in the folder
    for filename in os.listdir(folder_path):

        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)

            # Read and parse the JSON file
            with open(file_path) as file:
                data = json.load(file)

            # Extract the text from the JSON data
            text = json.dumps(data, indent=4)

            # Create a blank image with the specified dimensions and background color
            image = Image.new('RGB', (image_width, image_height), background_color)
            draw = ImageDraw.Draw(image)
            
            # Draw the text on the image
            draw.text((10, 10), text, font=font, fill=font_color)
            output_image = f'images/{os.path.splitext(filename)[0]}.png'
            
            # Save the image
            image.save(output_image)

# statistics
def generate_summary():
    
    folder_path = 'json' 
    # Initialize a dictionary to store the value counts
    value_counts = defaultdict(int)

    # Specify the keys of interest
    keys_of_interest = ['race', 'class', 'armor', 'item', 'weapon']

    # Iterate over the JSON files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            # Read and parse the JSON file
            with open(file_path) as file:
                data = json.load(file)

            # Count the occurrences of the values for the specified keys
            for key in keys_of_interest:
                if key in data:
                    value = data[key]
                    value_counts[value] += 1

    output_file = 'summary.csv'
    
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Value', 'Count'])
        for value, count in value_counts.items():
            writer.writerow([value, count])

# metadata
def generate_metadata():

    # Define folder paths
    json_path = 'json'
    metadata_path = 'metadata'

    for filename in os.listdir(json_path):

        # Define collection attributes
        project_name = 'Text Heroes'
        project_description = 'Text Heroes - a project where unique heroes engage in fierce creature battles and thrilling PvP combat. Collect rare heroes with special abilities, fight menacing creatures, and challenge other players in epic duels. Or just chill. Your choice.'
        external_url = ''
        image = ''

        # Initialize metadata and attributes list
        metadata = {}

        if filename.endswith('.json'):

            file_path = os.path.join(json_path, filename)

            with open(file_path) as file:
                data = json.load(file)
                
            trait_list = [{"trait_type": key, "value": value} for key, value in data.items()]

            # Append the text to the JSON data
            metadata['attributes'] = trait_list
            metadata['description'] = project_description
            metadata['external_url'] = f'{external_url}'
            metadata['image'] = f'{image}'
            metadata['name'] = project_name

            destination_file_path = os.path.join(metadata_path, filename)

            with open(destination_file_path, "w") as file:
                json.dump(metadata, file, indent=4)

# generator
def generate_json_files(num_files: int, races: list, races_weights: list, classes: dict, classes_weights:list, weapons: dict, items:dict):
    for i in range(num_files):

        # Build the character

        # race
        character_race = random.choices(races, races_weights, k=1)[0]
       
        # class
        character_class = random.choices(list(classes), classes_weights, k=1)[0]
        
        # base hp -- not listed
        class_hp = classes[character_class]

        # armor
        if character_class == 'warrior':
            character_armor = random.choice(['heavy', 'medium'])
            character_speed = round(random.uniform(1, 1.4), 2)
        elif character_class == 'paladin':
            character_armor = random.choice(['heavy', 'medium'])
            character_speed = round(random.uniform(1, 1.4), 2)
        elif character_class == 'hunter':
            character_armor = random.choice(['medium', 'light']) 
            character_speed = round(random.uniform(2, 4), 2)     
        elif character_class == 'assassin':
            character_armor = random.choice(['medium', 'light', 'ultralight'])
            character_speed = round(random.uniform(4, 5), 2)  
        elif character_class == 'monk':
            character_armor = random.choice(['medium', 'light', 'ultralight', 'cloth'])
            character_speed = round(random.uniform(1, 1.2), 2)
        elif character_class == 'shaman':        
            character_armor = random.choice(['medium', 'light', 'ultralight', 'cloth'])
            character_speed = round(random.uniform(1, 1.4), 2)
        elif character_class == 'mage':
            character_armor = random.choice(['ultralight', 'cloth'])
            character_speed = round(random.uniform(1, 1.3), 2)

        # item
        character_item = random.choice(list(items))

        # weapon
        character_weapon = random.choice(list(weapons[character_class]))

        # armor hp -- not listed
        armor_hp = armors[character_armor]

        # total hp
        character_hp = round((class_hp + armor_hp) * items[character_item], 2)

        # dmg: 
        weapon_dmg = weapons[character_class][character_weapon]

        # total dmg
        character_dmg = round(weapon_dmg * character_speed * items[character_item], 2)

        # Generate the attribute list
        data = {
            'race': character_race,
            'class': character_class,
            'armor': character_armor,
            'item': character_item,
            'weapon': character_weapon,
            'speed': character_speed,
            'hp': character_hp,
            'dmg': character_dmg
        }

        # Create the json
        folder_path = 'json'
        filename = f'{i+1}.json'
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

#endregion functions

#region variables

# races
races = ['human', 'dwarf', 'elf', 'druid']
races_weights = [0.4, 0.3, 0.2, 0.1]

# classes: hp
classes = {'warrior': 80, 'paladin': 75, 'hunter': 65, 'assassin': 60, 'monk': 55, 'shaman': 50, 'mage': 40}
classes_weights = [0.2, 0.2, 0.2, 0.10, 0.15, 0.05, 0.10]

# armor
armors = {'heavy': 20, 'medium': 10, 'light': 5, 'ultralight': 2, 'cloth': 0}

# weapon: dmg
weapons = {
    'warrior': {'hammer': 60, 'mace': 50, 'axe': 75, 'spear': 50, 'dual swords': 85, 'long sword': 95},
    'paladin': {'hammer': 60, 'mace': 50, 'long sword': 95},
    'hunter': {'crossbow': 35, 'bow': 25, 'slingshot': 20},
    'assassin': {'dagger': 15, 'knife': 10, 'short sword': 20, 'dual knives': 20, 'dual daggers': 30},
    'monk': {'staff': 70},
    'shaman': {'corruption': 85, 'frenzy': 80, 'tourment': 75},
    'mage': {'icebolt': 95, 'icelance': 85, 'firebolt': 95, 'firelance': 85}
}

# # speed -- random -- set in the constructor
# warrior: 1-1.4
# paladin: 1-1.4
# hunter: 2-4
# assassin: 4-5
# monk: 1-1.2
# shaman: 1-1.4
# mage: 1-1.3

# item: hp and dmg multiplier
items = {'lucky charm': 1.05, 'gold ring': 1.1, 'mystery orb': 1.2, 'cursed ring': 0.9, 'heavy old book': 0.95, 'chalice': 1}

#endregion variables
  
