"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Kimora James 

AI Usage: I used Chatgpt to help me structure my functions 

This module handles loading and validating game data from text files.
"""

import os #provides file path checking and file operations 
from custom_exceptions import (
    InvalidDataFormatError, #raised when file data has wrong formatb 
    MissingDataFileError, #raised when file is missing 
    CorruptedDataError #raised when file cannpt be read or empty 
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    if not os.path.exists(filename): #checks if file exists 
        raise MissingDataFileError(f"Quest file not found: {filename}")

    try: #tries to read the file 
        with open(filename, "r", encoding="utf8") as f:
            raw_lines = f.read().strip()
    except Exception:
        raise CorruptedDataError("Could not read quest file")

    if not raw_lines: #check if file is empty 
        raise CorruptedDataError("Quest file is empty")

    # Split quests by blank lines
    blocks = [block.strip().split("\n") for block in raw_lines.split("\n\n")] #split files into blocks for each quest seperated by blank lines 

    quests = {} #dictionary to store parsed quests 

    for block in blocks: # parse each quest block 
        quest = parse_quest_block(block)  # may raise InvalidDataFormatError convert into dictionary
        validate_quest_data(quest) #validate required fields and types 

        quests[quest["quest_id"]] = quest #store quests in dictionary by quest_id

    return quests #return all loaded quests 


def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    if not os.path.exists(filename): #checks if file exists again 
        raise MissingDataFileError(f"Item file not found: {filename}")

    try: #tries to read files 
        with open(filename, "r", encoding="utf8") as f:
            raw_lines = f.read().strip()
    except Exception:
        raise CorruptedDataError("Could not read item file")

    if not raw_lines:
        raise CorruptedDataError("Item file is empty")

    # Split items by blank lines into blocks 
    blocks = [block.strip().split("\n") for block in raw_lines.split("\n\n")]

    items = {} #dictionary to store parsed items 

    for block in blocks:
        item = parse_item_block(block) #convert block to dictionary 
        validate_item_data(item) #validaye required fiels and types 

        items[item["item_id"]] = item #store item in dictionary by item_id

    return items #return all loaded items 

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required = [
        "quest_id", "title", "description", "reward_xp",
        "reward_gold", "required_level", "prerequisite"
    ]

    # Check all required fields exist
    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing quest field: {key}")

    # Validate numbers as integers 
    if not isinstance(quest_dict["reward_xp"], int):
        raise InvalidDataFormatError("reward_xp must be an integer")

    if not isinstance(quest_dict["reward_gold"], int):
        raise InvalidDataFormatError("reward_gold must be an integer")

    if not isinstance(quest_dict["required_level"], int):
        raise InvalidDataFormatError("required_level must be an integer")

    return True #validation passes 
def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for key in required: #check if exists 
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {key}")

    valid_types = {"weapon", "armor", "consumable"} #validate type field 
    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    if not isinstance(item_dict["cost"], int): #validate numeric cost
        raise InvalidDataFormatError("cost must be integer")

    # EFFECT must be formatted like: stat:value
    if ":" not in item_dict["effect"]:
        raise InvalidDataFormatError("effect must be in form 'stat:value'")

    return True #validation passed 

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    
   
    if not os.path.exists("data/quests.txt"): #creates this if missing 
        with open("data/quests.txt", "w", encoding="utf8") as f:
            f.write(
                "QUEST_ID: quest_intro\n"
                "TITLE: The Beginning\n"
                "DESCRIPTION: Your adventure begins!\n"
                "REWARD_XP: 50\n"
                "REWARD_GOLD: 20\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )

    # Create default items #create if missing 
    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", "w", encoding="utf8") as f:
            f.write(
                "ITEM_ID: potion_small\n"
                "NAME: Small Health Potion\n"
                "TYPE: consumable\n"
                "EFFECT: health:20\n"
                "COST: 15\n"
                "DESCRIPTION: Restores 20 health.\n"
            )
            # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest = {} #dictionary to store parsed quest 

    for line in lines:
        if ": " not in line: #validate format 
            raise InvalidDataFormatError(f"Invalid quest line: {line}")

        key, value = line.split(": ", 1) #split key/value 
        key = key.strip().lower() #normalize key to lowercase 

        # Normalize key names into dictionary-friendly versions
        if key == "quest_id":
            quest["quest_id"] = value.strip()
        elif key == "title":
            quest["title"] = value.strip()
        elif key == "description":
            quest["description"] = value.strip()
        elif key == "reward_xp":
            quest["reward_xp"] = int(value)
        elif key == "reward_gold":
            quest["reward_gold"] = int(value)
        elif key == "required_level":
            quest["required_level"] = int(value)
        elif key == "prerequisite":
            quest["prerequisite"] = value.strip()
        else:
            raise InvalidDataFormatError(f"Unknown quest field: {key}")

    return quest
def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item = {} #dictionary to store parsed items 

    for line in lines: #process each line 
        if ": " not in line: #validate format 
            raise InvalidDataFormatError(f"Invalid item line: {line}")

        key, value = line.split(": ", 1) #split key/value 
        key = key.strip().lower() #normalize key 

        if key == "item_id": #map keys to dictionary fields 
            item["item_id"] = value.strip()
        elif key == "name":
            item["name"] = value.strip()
        elif key == "type":
            item["type"] = value.strip()
        elif key == "effect":
            item["effect"] = value.strip()
        elif key == "cost":
            item["cost"] = int(value)
        elif key == "description":
            item["description"] = value.strip()
        else:
            raise InvalidDataFormatError(f"Unknown item field: {key}")

    return item



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

