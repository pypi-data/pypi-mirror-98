# Constants for the wrapper
"""
Specifies a timeout in seconds for http request.
Default: 10
"""
DEFAULT_TIMEOUT = 10

"""
If the data in cache is older than CACHE_TIME seconds, then a new request will be made.
Default: 300
"""
CACHE_TIME = 300


# Constants for communicating Wynncraft API (DO NOT CHANGE!)
URL_V1 = "https://api.wynncraft.com/public_api.php?action="

URL_V2 = "https://api.wynncraft.com/v2/"

URL_CODES = {
    " ": "+",
    "^": "%5E",
    "<": "%3C",
    ">": "%3E"
}

INGREDIENT_QUERIES =[
    "name",
    "tier",
    "level",
    "skills",
    "sprite",
    "identifications",
    "itemOnlyIDs",
    "consumableOnlyIDs"
]

SKILLS = [
    "alchemism",
    "armouring",
    "cooking",
    "jeweling",
    "scribing",
    "tailoring",
    "weaponsmithing",
    "woodworking"
]

SPRITES = [
    "id",
    "damage"
]

IDENTIFICATIONS = [
    "agilitypoints",
    "airdamagebonus",
    "airdefense",
    "attackspeed",
    "damagebonus",
    "damagebonusraw",
    "defensepoints",
    "dexteritypoints",
    "earthdamagebonus",
    "earthdefense",
    "emeraldstealing",
    "exploding",
    "firedamagebonus",
    "firedefense",
    "healthbonus",
    "healthregen",
    "healthregenraw",
    "intelligencepoints",
    "lifesteal",
    "lootbonus",
    "loot_quality",
    "manaregen",
    "manasteal",
    "poison",
    "reflection",
    "soulpoints",
    "speed",
    "spelldamage",
    "spelldamageraw",
    "stamina_regen",
    "strengthpoints",
    "thorns",
    "thunderdamagebonus",
    "thunderdefense",
    "waterdamagebonus",
    "waterdefense",
    "xpbonus"
]

ITEM_ONLY_IDS = [
    "durability",
    "strength",
    "dexterity",
    "intelligence",
    "defence",
    "agility"
]

CONSUMABLE_ONLY_IDS = [
    "duration",
    "charges"
]

CATEGORIES = [
    "all",
    "boots",
    "bow",
    "bracelet",
    "chestplate",
    "dagger",
    "helmet",
    "leggings",
    "necklace",
    "ring",
    "spear", 
    "wand"
]

RECIPE_CATEGORIES = [
    "boots",
    "bow",
    "bracelet",
    "chestplate",
    "dagger",
    "food",
    "helmet",
    "leggings",
    "necklace",
    "potion",
    "relik",
    "ring",
    "scroll",
    "spear", 
    "wand"
]

RECIPE_QUERIES = [
    "type",
    "skill",
    "level",
    "durability",
    "healthOrDamage",
    "duration",
    "basicDuration"
]

RECIPE_MIN_MAX = [
    "min",
    "max"
]
