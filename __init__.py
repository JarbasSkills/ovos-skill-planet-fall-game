from ovos_workshop.decorators import conversational_intent, intent_handler
from pyfrotz.ovos import FrotzSkill


class PlanetFallSkill(FrotzSkill):
    def __init__(self, *args, **kwargs):
        # Game specific init
        def intro_parser(game):
            intro = """it's been five years since your planetfall on resida.
            your heroics in saving that doomed world resulted in a big promotion, but your life of dull scrubwork has been replaced by a life of dull paperwork.
            today you find yourself amidst the administrative maze of deck twelve on a typically exciting task: an emergency mission to space station gamma delta gamma 777- g 59/59 sector alpha-mu-79 to pick up a supply of request for stellar patrol issue regulation black form binders request form forms
            """
            game._frotz_read()
            return intro

        # game is english only, apply bidirectional translation
        super().__init__(game_id="planetfall",
                         game_lang="en-us",
                         game_data=f'{self.root_dir}/res/{self.game_id}.z5',
                         intro_parser=intro_parser,
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
