from pyfrotz.ovos import FrotzSkill
from pyfrotz.parsers import planetfall_intro_parser


class PlanetFallSkill(FrotzSkill):
    def __init__(self, *args, **kwargs):
        # game is english only, apply bidirectional translation
        # TODO - dedicated icon, use pyfrotz icon for now
        skill_icon = "https://raw.githubusercontent.com/TigreGotico/pyFrotz/refs/heads/dev/pyfrotz/gui/all/pyfrotz.png"
        bg = "http://infocom.elsewhere.org/gallery/planetfall/planetfall1.jpg"
        super().__init__(*args,
                         game_id="planetfall",
                         game_lang="en-us",
                         game_data=f'{self.root_dir}/res/{self.game_id}.z5',
                         intro_parser=planetfall_intro_parser,
                         skill_icon=skill_icon,
                         game_image=bg,
                         **kwargs)
