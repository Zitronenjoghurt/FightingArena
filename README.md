# FightingArena (Work in progress)
A simulation of random generated fighters fighting against each other in turn-based matches with the main goal to be easily extendable.

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
|`name`|`no`|str|The name of the fighter class.|`no_name`|`barbarian`|
|`max_hp`|`no`|int|The maximum HP fighters of this class have.|`0`|`1000`|
|`max_mp`|`no`|int|The maximum MP fighters of this class have.|`0`|`200`|
|`max_stamina`|`no`|int|The maximum amount of Stamina fighters of this class have.|`0`|`200`|
|`skills`|`yes`|dict|Which skills characters of this class have. (Look in the fighter skills subsection for more info).||`{"name": "sword slash", "level": 1}`|

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
            "attack": {"damage": 150, "stamina_cost": 20}
        },
        "effects": {},
        "message": "{user} uses their sword to slash {opponent}.",
        "themes": ["sword", "knight", "physical", "melee"]
    },
    "fireball": {
        "actions": {
            "attack": {"damage": 100, "mp_cost": 20}
        },
        "effects": {
            "burn": {"duration": 3, "damage": 25}
        },
        "message": "{user} throws fireball at {opponent}.",
        "themes": ["fire", "magic", "ranged"]
    }
}
```

|Property|Required|Type|Description|Default|Example|
|---|---|---|---|---|---|
|`actions`|`yes`|dict|The name of the fighter class.||`{"attack": {"damage": 150, "stamina_cost": 20}}`|
|`effects`|`yes`|dict|The maximum HP fighters of this class have.||`{"burn": {"duration": 3, "damage": 25}}`|
|`cooldown`|`no`|int|The amount of rounds that have to pass before the fighter can use this skill again.|`0`|`3`|
|`message`|`yes`|str|The message that is output when the skill is used.||`"{user} throws fireball at {opponent}."`|
|`themes`|`yes`|list|Thematic context of this skill. Will be used to allow random generation of skillsets based on themes.||`["fire", "magic", "ranged"]`|
