from pyfrotz.ovos import FrotzSkill
from pyfrotz.parsers import planetfall_intro_parser


class PlanetFallSkill(FrotzSkill):
    def __init__(self, *args, **kwargs):
        # game is english only, apply bidirectional translation
        super().__init__(*args,
                         game_id="planetfall",
                         game_lang="en-us",
                         game_data=f'{self.root_dir}/res/{self.game_id}.z5',
                         intro_parser=planetfall_intro_parser,
                         **kwargs)
