"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Kimora James 

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # Dictionary of enemy types and stats
    enemy_types = {
        "goblin": {
            "health": 50, "strength": 8, "magic": 2,
            "xp_reward": 25, "gold_reward": 10
        },
        "orc": {
            "health": 80, "strength": 12, "magic": 5,
            "xp_reward": 50, "gold_reward": 25
        },
        "dragon": {
            "health": 200, "strength": 25, "magic": 15,
            "xp_reward": 200, "gold_reward": 100
        }
    }

    # Validate enemy type
    if enemy_type not in enemy_types:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")

    stats = enemy_types[enemy_type]

    # Build enemy dictionary
    return {
        "name": enemy_type,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "xp_reward": stats["xp_reward"],
        "gold_reward": stats["gold_reward"]
    }



def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
         self.character = character
         self.enemy = enemy
         self.combat_active = True   # Prevent actions when battle is finished
         self.turn_counter = 1       # Useful for logs and debugging
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # Prevent fighting while dead
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character cannot fight; they are dead.")

        display_battle_log("Battle begins!")
        display_combat_stats(self.character, self.enemy)

        # Main combat loop
        while self.combat_active:
            display_battle_log(f"--- Turn {self.turn_counter} ---")
            
            # PLAYER ACTION
            self.player_turn()
            result = self.check_battle_end()
            if result:  # If someone died, stop the loop
                break

            # ENEMY ACTION
            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                break
            self.turn_counter += 1

        # Determine winner and return results
        winner = result
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            display_battle_log("You defeated the enemy!")
            display_battle_log(f"XP gained: {rewards['xp']}, Gold gained: {rewards['gold']}")
            return {"winner": "player", "xp_gained": rewards["xp"], "gold_gained": rewards["gold"]}

        else:
            display_battle_log("You were defeated...")
            return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}    
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
                if not self.combat_active:
            raise CombatNotActiveError()

        display_battle_log("Your turn!")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")

        choice = input("Choose an action: ").strip()

        if choice == "1":
            # Basic damage calculation
            dmg = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, dmg)
            display_battle_log(f"You deal {dmg} damage!")
            display_combat_stats(self.character, self.enemy)

        elif choice == "2":
            # Use class-specific special ability
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
            display_combat_stats(self.character, self.enemy)

        elif choice == "3":
            # 50/50 escape chance
            if self.attempt_escape():
                display_battle_log("You escaped successfully!")
                return
            else:
                display_battle_log("Escape failed!")

        else:
            display_battle_log("Invalid input; you lose your turn.")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError()

        display_battle_log(f"{self.enemy['name'].capitalize()} attacks!")
        dmg = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, dmg)
        display_battle_log(f"The {self.enemy['name']} deals {dmg} damage!")
        display_combat_stats(self.character, self.enemy)
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        dmg = attacker["strength"] - (defender["strength"] // 4)
        return max(1, dmg)  # Ensures damage never drops below 1
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        target["health"] = max(0, target["health"] - damage)
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    cls = character["class"]

    if cls == "Warrior":
        return warrior_power_strike(character, enemy)
    elif cls == "Mage":
        return mage_fireball(character, enemy)
    elif cls == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif cls == "Cleric":
        return cleric_heal(character)
    else:
        return "Your class has no special ability."
def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    dmg = character["strength"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"Power Strike! You deal {dmg} huge damage!"

def mage_fireball(character, enemy):
    """Mage special ability"""
    dmg = character["magic"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"Fireball! You burn the enemy for {dmg} magic damage!"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    if random.random() < 0.5:
        dmg = character["strength"] * 3
        enemy["health"] = max(0, enemy["health"] - dmg)
        return f"CRITICAL STRIKE! Massive hit for {dmg}!"
    else:
        dmg = character["strength"]
        enemy["health"] = max(0, enemy["health"] - dmg)
        return f"Critical fail... normal damage: {dmg}."

def cleric_heal(character):
    """Cleric special ability"""
   
    old_hp = character["health"]
    character["health"] = min(character["max_health"], old_hp + 30)
    healed = character["health"] - old_hp
    return f"Cleric Heal restores {healed} HP!"
# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    return character["health"] > 0

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {
        "xp": enemy["xp_reward"],
        "gold": enemy["gold_reward"]
    }


def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
   

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
   

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

