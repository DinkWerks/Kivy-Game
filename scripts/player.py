import yaml

class Player:
    pc_file = file('data/player.yml')
    pc_dat = yaml.load(pc_file)
    item_file = file('data/items.yml')
    item_dat = yaml.load(item_file)
    # Player Profile
    Name = ''
    Is_Person = ''
    Level = 0
    # Player Stats
    hp = 0
    str = 0
    agi = 0
    acc = 0
    end = 0
    per = 0
    spd = 0
    armor = 0
    # Equipped Melee
    weapon_name = ''
    weapon_alt_name = ''
    weapon_damage = 0
    weapon_range = 1
    damage_type = ''
    # Equipped Ranged
    ranged_name = ''
    ranged_alt_name = ''
    ranged_damage = 0
    ranged_ranged = 8
    ammo_count = 0
    reload_time = 0
    # Inventory and Statuses
    Gold = 0
    Inventory = {}
    Condition = {}
    # Combat Status
    location = 0
    defended = False
    dodged = False

    def __init__(self):
        self.char = Player.pc_dat
        self.item = Player.item_dat

    def load_character(self):
        Player.Name = self.char['character']['Name']
        Player.Level = self.char['character']['Level']
        Player.Is_Person = self.char['character']['Is_Person']
        Player.armor = self.char['character']['stats']['armor']
        Player.hp = self.char['character']['stats']['hp']
        Player.str = self.char['character']['stats']['str']
        Player.agi = self.char['character']['stats']['agi']
        Player.acc = self.char['character']['stats']['agi']
        Player.end = self.char['character']['stats']['end']
        Player.per = self.char['character']['stats']['per']
        Player.spd = self.char['character']['stats']['spd']
        Player.Gold = self.char['character']['Gold']
        Player.Inventory = self.char['character']['Inventory']
        Player.condition = self.char['character']['Condition']

    def add_equipment(self, item_class, item):
        Player.weapon_name = self.item_dat[item_class][item]['name']
        Player.weapon_alt_name = self.item_dat[item_class][item]['alt name']
        Player.weapon_damage = self.item_dat[item_class][item]['damage']
        Player.damage_type = self.item_dat[item_class][item]['type']
        for stat in self.item_dat[item_class][item]['stats']:
            setattr(Player, stat, self.item_dat[item_class][item]['stats'][stat] + getattr(Player, stat))
