import yaml
import random
from kivy.properties import StringProperty
from shlex import shlex
from player import Player
from enemy import Enemy


class Event(Player):
    open_events = file('data/event.yml', 'r')
    event_file = yaml.load(open_events)
    current_text = StringProperty('1234')

    def __init__(self):
        Player.__init__(self)
        self.events = Event.event_file
        self.selection = ''
        self.current_text = '1234'

    def event_name(self):
        eid = random.choice(Event.event_file.keys())
        self.event_selector(eid)
        return self.selection

    def event_selector(self, eid):
        boop = eval(self.events[eid]['condition']['Level'])
        if boop is True:
            self.selection = eid
        elif boop is False:
            self.event_name()
        else:
            self.event_name()

    def parse(self):
        driver = 1
        variables = ('Name', 'Is_Person', 'Level', 'Gold')
        poss_commands = ("[Next Slide]", "[Query]", "[Terminate]", "[Combat]")

        while driver >= 0:
            text = self.events[self.selection][driver]
            lexer = shlex(text)
            lexer.quotes = '/'

            output = ''
            command = ''
            for token in lexer:
                if token in variables:
                    output += str(eval('Player.' + token))
                elif token.replace('/', '') in poss_commands:
                    command += token.replace('/', '')
                else:
                    output += token.replace('/', '')
            self.current_text = output
            driver += self.controller(command)
        self.modifier()

    def modifier(self):
        mods = self.events[self.selection]['modifier']
        if mods is not None:
            for item in mods:
                if item == 'Inventory':
                    for obj in mods[item]:
                        if obj not in self.Inventory:
                            obj_to_add = {obj: mods[item][obj]}
                            self.Inventory.update(obj_to_add)
                        elif obj in self.Inventory:
                            self.Inventory[obj] += mods[item][obj]
                        else:
                            print 'Inventory Error'
                            break
                elif item == 'Event_Confirmation':
                    pass
                else:
                    stat = getattr(Player, item)
                    setattr(Player, item, stat + mods[item])
        else:
            pass

    def controller(self, cmd):
        if cmd == "[Next Slide]":
            return 1
        elif cmd == "[Query]":
            return 0
        elif cmd == "[Terminate]":
            return -99
        elif cmd == '[Combat]':
            enemy = self.events[self.selection]['enemy']
            enemy_stats = Enemy(enemy)
            enemy_stats.load_enemy()
            combat = Combat()
            combat.combat_start()
            return 1
        else:
            print "Event failed to terminate."
            return -99


class Combat:
    damage_types = ('blunt', 'slash', 'pierce', 'projectile', 'shoot')
    special_damage_types = ('burned', 'explosive', 'poisoned')

    def __init__(self):
        pass

    def combat_start(self):
        print 'Your Health: ' + str(Player.hp) + '   Your Location: ' + str(Player.location)
        print Enemy.Name + '\'s Health: ' + str(Enemy.hp) + '   ' + Enemy.Name + '\'s Location: ' + str(Enemy.location)
        print
        print 'Available Actions: 1. Attack, 2. Shoot, 3. Dodge, 4. Defend, 5. Item, 6. Move'
        choice = str.lower(raw_input('Which action will your take?: '))
        self.choice_evaluator(choice, Player, Enemy)

    def combat_bridge(self, defender):
        if defender == Enemy:
            attacker = Enemy
            defender = Player
        else:
            attacker = Player
            defender = Enemy
        while Player.hp > 0 and Enemy.hp > 0:
            print 'Your Health: ' + str(Player.hp) + '   Your Location: ' + str(Player.location)
            print Enemy.Name + '\'s Health: ' + str(Enemy.hp) + '   ' + Enemy.Name + '\'s Location: ' + str(
                Enemy.location)
            print
            print 'Available Actions: 1. Attack, 2. Shoot, 3. Dodge, 4. Defend, 5. Item, 6. Move'
            choice = str.lower(raw_input('Which action will your take?: '))
            self.choice_evaluator(choice, attacker, defender)
        print 'Event Complete!'

    def choice_evaluator(self, choice, attacker, defender):
        if choice == '1' or choice == 'attack':
            print
            # print 'Choose attack type: 1. Cautious, 2. Standard, 3. Heavy'
            # atk_type = str(raw_input('How will you attack: '))
            if self.chance_to_hit(attacker, defender) is True:
                self.calculate_damage(attacker, defender)
            else:
                print
                print 'The attacked missed.'
            self.boost_resets(defender)
            self.combat_bridge(defender)
        elif choice == '2' or choice == 'shoot':
            print
            print 'You have ' + str(attacker.ammo_count) + ' shots left'
            if attacker.ammo_count > 0:
                if self.ranged_to_hit(attacker, defender) is True:
                    self.calculate_damage(attacker, defender)
                else:
                    'The shot missed.'
            else:
                self.reload(attacker)
                print 'You reload.'
            self.boost_resets(defender)
            self.combat_bridge(defender)
        elif choice == '3' or choice == 'dodge':
            #  Double Temporary Player Agility
            attacker.agi *= 2
            attacker.dodged = True
            self.boost_resets(defender)
            self.combat_bridge(defender)
        elif choice == '4' or choice == 'defend':
            #  Double Temporary Player Endurance
            attacker.end *= 2
            attacker.defended = True
            self.boost_resets(defender)
            self.combat_bridge(defender)
        elif choice == '5' or choice == 'item':
            # Load inventory and send to item_handler()
            self.boost_resets(defender)
            self.combat_bridge(defender)
        elif choice == '6' or choice == 'move':
            print
            direction = str.lower(raw_input('Will you move left or right?: '))
            self.move(direction, attacker, defender)
            self.boost_resets(defender)
            self.combat_bridge(defender)
        else:
            print
            choice = str.lower(raw_input('Command not found. Please Retry: '))
            self.boost_resets(defender)
            self.choice_evaluator(choice, attacker, defender)

    def chance_to_hit(self, attacker, defender):
        if abs(defender.location - attacker.location) <= attacker.weapon_range:
            chance = ((attacker.agi - defender.agi) * 0.05 + 0.75) * 100
            if chance >= random.randint(0, 100):
                return True
            else:
                return False
        else:
            print 'You need to get closer to attack.'
            self.combat_bridge(attacker)

    @staticmethod
    def ranged_to_hit(attacker, defender):
        chance = ((attacker.acc - defender.agi) * 0.05 + (.8 * (abs(defender.location - attacker.location))))
        if chance >= random.randint(0, 100):
            return True
        else:
            return False

    @staticmethod
    def reload(attacker):
        attacker.reload_count += 1
        if attacker.reload_count == attacker.reload_time:
            attacker.ammo_count = attacker.max_ammo

    @staticmethod
    def calculate_damage(attacker, defender):
        dmg_type = attacker.damage_type
        if dmg_type == 'blunt':
            damage = attacker.str + attacker.weapon_damage + random.randint(0, attacker.Level) - defender.end
        elif dmg_type == 'slash':
            damage = attacker.str + attacker.weapon_damage + random.randint(0, attacker.Level) - defender.armor - defender.e_end
        elif dmg_type == 'pierce':
            damage = attacker.agi + attacker.weapon_damage + random.randint(0, attacker.Level) - defender.armor / 2 - defender.end
        elif dmg_type == 'projectile':
            damage = attacker.agi + attacker.weapon_damage + random.randint(0, attacker.Level) - defender.armor / 2 - defender.end
        else:  # This is for shooting damage
            damage = attacker.agi + attacker.weapon_damage + random.randint(0, attacker.Level) - defender.armor / 2
        if damage > 0:
            print attacker.Name + ' did ' + str(damage) + ' damage!'
            defender.hp -= damage
        else:
            print attacker.Name + ' attacked, but did no damage'

    @staticmethod
    def move(direction, attacker, defender):
        if direction == 'left':
            for move in range(1 + attacker.spd):
                mod = -1
                if attacker.location + mod != defender.location and attacker.location + mod < 8:
                    attacker.location += mod
                else:
                    print 'You can\'t move that direction.'
                    break
        elif direction == 'right':
            for move in range(1 + attacker.spd):
                mod = 1
                if attacker.location + mod != defender.location and attacker.location + mod > -1:
                    attacker.location += mod
                else:
                    'You can\'t move that direction.'
                    break
        else:
            print 'Error: You didn\'t move.'

    @staticmethod
    def boost_resets(defender):
        if defender.dodged is True:
            defender.agi /= 2
            defender.dodged = False
        if defender.defended is True:
            defender.end /= 2
            defender.defended = False

ct = Event.current_text

player_stats = Player()
player_stats.load_character()
player_stats.add_equipment('weapon', 'Vorpal Cod')
