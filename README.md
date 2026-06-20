# PacMan
Pacman project 42 school

NNESSEEENEENNNENNN






Entities -> classe astratta che rappresenta le entita' in gioco: player, enemies, pacgums (normal and super), vari ed eventuali powerups e idee di sorta
	Objects (Entities) -> sottoclasse astratta che rappresenta gli oggetti in campo (pacgums e powerups)
	Entitys (Entities) -> sottoclasse astratta che rappresenta i personaggi (player e enemies)
		Enemies (Entitys) -> sottoclasse astratta che rappresenta i nemici, ognuno con la sua strategy personalizzata



src/
│
├── core/
│   ├── game.py
│   ├── gamestate.py
│   ├── scene_manager.py
│   └── event_bus.py
│
├── entities/
│   ├── entity.py
│   ├── player.py
│   ├── enemy.py
│   ├── pacgum.py
│   └── super_pacgum.py
│
├── ai/
│   ├── strategies/
│   └── states/
│
├── systems/
│   ├── movement_system.py
│   ├── collision_system.py
│   ├── scoring_system.py
│   ├── cheat_system.py
│   ├── timer_system.py
│   └── highscore_system.py
│
├── level/
│   ├── maze_adapter.py
│   ├── level.py
│   └── level_builder.py
│
├── config/
│   ├── config_loader.py
│   └── game_config.py
│
├── scenes/
│
├── ui/
│
└── pacman.py