import yaml


class Enemy:
    enemy_file = file('data/enemies.yml')
    enemy_dat = yaml.load(enemy_file)
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
    max_ammo = 0
    ammo_count = 0
    reload_time = 0
    reload_count = 0
    # Inventory and Statuses
    Inventory = {}
    Condition = {}
    # Combat Status
    location = 7
    defended = False
    dodged = False

    def __init__(self, enemy_id):
        self.id = enemy_id
        self.enemy = Enemy.enemy_dat[self.id]

    def load_enemy(self):
        Enemy.Name = self.enemy['Name']
        Enemy.Level = self.enemy['Level']
        Enemy.armor = self.enemy['stats']['armor']
        Enemy.hp = self.enemy['stats']['hp']
        Enemy.str = self.enemy['stats']['str']
        Enemy.agi = self.enemy['stats']['agi']
        Enemy.acc = self.enemy['stats']['agi']
        Enemy.end = self.enemy['stats']['end']
        Enemy.spd = self.enemy['stats']['spd']
        Enemy.armor = self.enemy['stats']['armor']
        # Enemy.Inventory = self.enemy['Inventory']
        # Enemy.condition = self.enemy['Condition']
        #  Attack Stats
        Enemy.weapon_name = self.enemy['attack']['name']
        Enemy.weapon_alt_name = self.enemy['attack']['alt name']
        Enemy.weapon_damage = self.enemy['attack']['damage']
        Enemy.weapon_range = self.enemy['attack']['range']
        Enemy.damage_type = self.enemy['attack']['type']