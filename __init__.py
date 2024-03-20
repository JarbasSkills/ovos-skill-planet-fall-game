from ovos_workshop.decorators import conversational_intent, intent_handler
from pyfrotz.ovos import FrotzSkill
from pyfrotz.parsers import planetfall_intro_parser


class PlanetFallSkill(FrotzSkill):
    def __init__(self, *args, **kwargs):
        # game is english only, apply bidirectional translation
        super().__init__(game_id="planetfall",
                         game_lang="en-us",
                         game_data=f'{self.root_dir}/res/{self.game_id}.z5',
                         intro_parser=planetfall_intro_parser,
                         *args, **kwargs)

    @intent_handler("play.intent")
    def handle_play(self, message=None):
        self.start_game(load_save=True)

    # intents
    @conversational_intent("exit.intent")
    def handle_exit(self, message=None):
        self.exit_game()

    @conversational_intent("restart_game.intent")
    def handle_restart(self, message=None):
        self.start_game(load_save=False)

    @conversational_intent("save.intent")
    def handle_save(self, message=None):
        self.save_game()
