# FightingArena (Work in progress)
A simulation of random generated fighters fighting against each other in turn-based matches with the main goal to be easily extendable.

You can navigate this readme easier by using the button with the 3 dots and lines. It will open a table of contents.

## Command line
This instructions will explain how to set up FightingArena for use via command line.

### Prerequisites
The things you need to have preinstalled:
- Python (3.12 or higher)
- Git

### Clone the project
In the console of your choosing run:
```
git clone https://github.com/Zitronenjoghurt/FightingArena.git
```

### Install dependencies
Install all required dependencies via pip by using this command in the project directory:
```
pip install -r requirements.txt
```

---------------------------------------

# Configuration
There are various options to configurate fighters and skills to behave exactly how you want them to.

# Fighters
To customize fighters edit `/src/data/fighters/fighter_name.json` (fighter_name can be whatever name you want)

Example of the contents in `barbarian.json`:
```json
{
    "name": "barbarian",
    "max_hp": 1000,
    "max_mp": 0,
    "max_stamina": 250,
    "skills": [
        {"name": "sword slash", "level": 1}
    ]
}
```

|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`name`|`no`|str|The name fighters of this class will get by default (if not specified otherwise).|`no_name`|`barbarian`|
|`max_hp`|`no`|int|The maximum HP fighters of this class have.|`0`|`1000`|
|`max_mp`|`no`|int|The maximum MP fighters of this class have.|`0`|`200`|
|`max_stamina`|`no`|int|The maximum amount of Stamina fighters of this class have.|`0`|`200`|
|`initiative`|`no`|int|How fast fighters of this class are. The higher the initiative, the earlier they will attack.|`1`|`40`|
|`skills`|`no`|list|Which skills characters of this class have. (Look in the fighter skills subsection for more info).|`[]`|`[{"name": "sword slash", "level": 1}]`|

### Fighter skills
|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`name`|`yes`|str|The name of the skill (has to be defined in the `skills.json`, look in the skills section for more info).||`sword slash`|
|`level`|`no`|int|The level of this skill. The final skill properties will then be scaled depending on how the level scaling of the skill is defined in `skills.json`|`1`|`1`|

---------------------------------------

# Skills
To customize skills edit `/src/data/skills.json`

All skills are stored each as their own dict in the overall dict of skills.json. The key is the skill name, the value includes various skill data.
Example of the contens in `skills.json`:
```json
{
    "sword slash": {
        "actions": {
            "attack": {"damage": 150, "on_target": true}
        },
        "effects": {},
        "stamina_cost": 20,
        "message": "{user} uses their sword to slash {opponent}.",
        "themes": ["sword", "knight", "physical", "melee"]
    },
    "fireball": {
        "actions": {
            "attack": {"damage": 100, "on_target": true}
        },
        "effects": {
            "burn": {"duration": 3, "damage": 25, "on_target": true}
        },
        "mp_cost": 20,
        "message": "{user} throws fireball at {opponent}.",
        "themes": ["fire", "magic", "ranged"]
    }
}
```

|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`actions`|`yes`|dict|The name of the fighter class. (Look in the actions subsection for more info).||`{"attack": {"damage": 150}}`|
|`effects`|`yes`|dict|The maximum HP fighters of this class have. (Look in the effects subsection for more info).||`{"burn": {"duration": 3, "damage": 25}}`|
|`mp_cost`|`no`|int|The amount of mp it costs to use this action.|`0`|`20`|
|`stamina_cost`|`no`|int|The amount of stamina it costs to use this action.|`0`|`20`|
|`cooldown`|`no`|int|The amount of rounds that have to pass before the fighter can use this skill again.|`0`|`3`|
|`message`|`yes`|str|The message that is output when the skill is used.||`"{user} throws fireball at {opponent}."`|
|`themes`|`yes`|list|Thematic context of this skill. Will be used to allow random generation of skillsets based on themes.||`["fire", "magic", "ranged"]`|

## Actions
Actions are predetermined tasks a skill will fulfill once it is used. There is a predefined set of actions you can add to skills. You can specify different parameters for different actions.

Actions are added as dicts to the actions-dict of a skill, for example:
```json
"actions": {
    "attack": {"damage": 150, "on_target": true},
    "heal": {"amount": 50, "on_self": true}
},
```

### attack
Will deal the specified amount of damage to the target.
|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`damage`|`no`|int|The amount of damage the action is supposed to deal to the target.|`0`|`100`|
|`on_self`|`no`|bool|If action is applied to the user after use.|`False`|`True`|
|`on_target`|`no`|bool|If action is applied to the target after use.|`False`|`True`|

### heal
Will heal the specified amount of HP for the target.
|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`amount`|`no`|int|The amount of hp this action will heal to the user.|`0`|`100`|
|`on_self`|`no`|bool|If action is applied to the user after use.|`False`|`True`|
|`on_target`|`no`|bool|If action is applied to the target after use.|`False`|`True`|

### regen_mp
Will regenerate the specified amount of MP for the user.
|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`amount`|`no`|int|The amount of mp this action will add to the user.|`0`|`100`|
|`on_self`|`no`|bool|If action is applied to the user after use.|`False`|`True`|
|`on_target`|`no`|bool|If action is applied to the target after use.|`False`|`True`|

### regen_stamina
Will regenerate the specified amount of stamina for the user.
|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`amount`|`no`|int|The amount of stamina this action will add to the user.|`0`|`100`|
|`on_self`|`no`|bool|If action is applied to the user after use.|`False`|`True`|
|`on_target`|`no`|bool|If action is applied to the target after use.|`False`|`True`|

### lifesteal
Will deal the specified amount of damage to the target and heal a specified amount of HP for the user.
|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`damage`|`no`|int|The amount of damage the action is supposed to deal to the target.|`0`|`100`|
|`heal`|`no`|int|The amount of hp this action will heal to the user.|`0`|`100`|
|`damage_is_heal`|`no`|bool|If the amount of hp healed is supposed to depend on the dealt damage.|`False`|`True`|
|`heal_multiplier`|`no`|float|If `damage_is_heal` is true, this will multiply the amount of HP healed by the specified factor.|`1`|`1.5`, `2`|

## Effects
Effects are predetermined tasks that take effect on the target every round for a specified amount of rounds. There is a predefined set of effects you can add to skills. You can specify different parameters for different effects.

Effects are added as dicts to the effects-dict of a skill, for example:
```json
"effects": {
    "burn": {"duration": 3, "damage": 25, "on_target": true},
    "freeze": {"duration": 2, "on_target": true}
}
```

### burn
Will deal damage to the target every round for a specified amount of rounds.
|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`duration`|`no`|int|The amount of rounds this effect will last (including the round its applied).|`0`|`3`|
|`damage`|`no`|int|The amount of damage dealt to the target every round.|`0`|`25`|
|`on_self`|`no`|bool|If effect is applied to the user.|`False`|`True`|
|`on_target`|`no`|bool|If effect is applied to the target.|`False`|`True`|

### freeze
Will freeze the target and make them unable to attack for a specified amount of rounds.
|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`duration`|`no`|int|The amount of rounds this effect will last (including the round its applied).|`0`|`3`|
|`on_self`|`no`|bool|If effect is applied to the user.|`False`|`True`|
|`on_target`|`no`|bool|If effect is applied to the target.|`False`|`True`|
