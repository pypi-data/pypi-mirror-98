import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import json
import time

import utils.constants
import wynncraft


def get_data(id, function, *args):
    if InternalCacheManager.call_request(id):
        exec(f"x = {function}{args}", globals(), globals())
        res = x
    else:
        res = None

    return InternalCacheManager.search_cache(id, res)


class CacheManager:
    # User-facing cache manager

    try:
        os.mkdir(os.path.join(os.path.dirname(__file__), "../../.cache"))
    except FileExistsError:
        pass

    os.chdir(os.path.join(os.path.dirname(__file__), "../../.cache"))
    
    @staticmethod
    def delete_cache():
        for f in [".cache.json", ".cache-table.json"]:
            try:
                os.remove(f)
            except FileNotFoundError:
                continue


class InternalCacheManager(CacheManager):
    @staticmethod
    def read_json(file):
        try:
            with open(file) as f:
                pass
        except FileNotFoundError:
            with open(file, "w") as f:
                json.dump({}, f)
        
        with open(file, "r") as f:
            try:
                return json.loads(f.read())
            except json.decoder.JSONDecodeError:
                return json.loads("{}")

    @staticmethod
    def read_cache():
        return InternalCacheManager.read_json(".cache.json")

    @staticmethod
    def read_cache_table():
        return InternalCacheManager.read_json(".cache-table.json")
    
    @staticmethod
    def write_json(file, data, new_data):
        with open(file, "w") as f:
            data.update(new_data)
            json.dump(data, f)

    @staticmethod
    def write_cache_and_table(new_cache, new_table):
        cache = InternalCacheManager.read_cache()
        InternalCacheManager.write_json(".cache.json", cache, new_cache)

        cache_table = InternalCacheManager.read_cache_table()
        InternalCacheManager.write_json(".cache-table.json", cache_table, new_table)

    @staticmethod
    def search_cache(id, res):
        if res:
            InternalCacheManager.write_cache_and_table({id: res}, {id: int(time.time())})
            return res
        else:
            return InternalCacheManager.read_cache()[id]
    
    @staticmethod
    def call_request(id):
        cache_table = InternalCacheManager.read_cache_table()
        return ((not cache_table) or (id not in cache_table) or (cache_table[id] + utils.constants.CACHE_TIME < int(time.time())))

    
class Guild:
    @staticmethod
    def list():
        return get_data("guild_list", "wynncraft.Guild.list")

    @staticmethod
    def stats(name):
        return get_data("guild_stats", "wynncraft.Guild.stats", name)


class Ingredient:
    @staticmethod
    def get(name):
        return get_data(f"ingredient_get_{name}", "wynncraft.Ingredient.get", name)

    @staticmethod
    def list():
        return get_data(f"ingredient_list", "wynncraft.Ingredient.list")

    @staticmethod
    def search(query, arg):
        return get_data(f"ingredient_search_{query}_{arg}", "wynncraft.Ingredient.search", query, arg)

    @staticmethod
    def search_name(arg):
        return Ingredient.search("name", arg)
    
    @staticmethod
    def search_tier(arg):
        return Ingredient.search("tier", arg)

    @staticmethod
    def search_level(arg):
        return Ingredient.search("level", arg)

    @staticmethod
    def search_skills(arg):
        return Ingredient.search("skills", arg)

    @staticmethod
    def search_sprite(arg):
        return Ingredient.search("sprite", arg)
    
    @staticmethod
    def search_identifications(arg):
        return Ingredient.search("identifications", arg)

    @staticmethod
    def search_item_only_ids(arg):
        return Ingredient.search("itemOnlyIDs", arg)

    @staticmethod
    def search_consumable_only_ids(arg):
        return Ingredient.search("consumableOnlyIDs", arg)


class Item:
    @staticmethod
    def database_category(category):
        return get_data(f"item_db_category_{category}", "wynncraft.Item.database_category", category)

    @staticmethod
    def database_search(name):
        return get_data(f"item_db_search_{name}", "wynncraft.Item.database_search", name)


class Leaderboard:
    @staticmethod
    def guild(timeframe):
        return get_data(f"leaderboard_guild_{timeframe}", "wynncraft.Leaderboard.guild", timeframe)

    @staticmethod
    def player(timeframe):
        return get_data(f"leaderboard_player_{timeframe}", "wynncraft.Leaderboard.player", timeframe)

    @staticmethod
    def pvp(timeframe):
        return get_data(f"leaderboard_pvp_{timeframe}", "wynncraft.Leaderboard.pvp", timeframe)


class Network:
    @staticmethod
    def server_list():
        return get_data("server_list", "wynncraft.Network.server_list")

    @staticmethod
    def player_sum():
        return get_data("player_sum", "wynncraft.Network.player_sum")


class Player:
    @staticmethod
    def stats(player):
        return get_data("player_stats", "wynncraft.Player.stats", player)

    @staticmethod
    def uuid(username):
        return get_data("player_uuid", "wynncraft.Player.uuid", username)


class Recipe:
    @staticmethod
    def get(name):
        return get_data(f"recipe_get_{name}", "wynncraft.Recipe.get", name)

    @staticmethod
    def list():
        return get_data("recipe_list", "wynncraft.Recipe.list")

    @staticmethod
    def search(query, arg):
        return get_data(f"recipe_search_{query}_{arg}", "wynncraft.Recipe.search", query, arg)

    @staticmethod
    def search_type(arg):
        return Recipe.search("type", arg)
    
    @staticmethod
    def search_skill(arg):
        return Recipe.search("skill", arg)

    @staticmethod
    def search_level(arg):
        return Recipe.search("level", arg)
    
    @staticmethod
    def search_durability(arg):
        return Recipe.search("durability", arg)

    @staticmethod
    def search_health_or_damage(arg):
        return Recipe.search("healthOrDamage", arg)

    @staticmethod
    def search_duration(arg):
        return Recipe.search("duration", arg)

    @staticmethod
    def search_basic_duration(arg):
        return Recipe.search("basicDuration", arg)


class Search:
    @staticmethod
    def name(name):
        return get_data(f"search_{name}", "wynncraft.Search.name", name)


class Territory:
    @staticmethod
    def list():
        return get_data("territory_list", "wynncraft.Territory.list")
