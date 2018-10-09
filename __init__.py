from mycroft.skills.core import MycroftSkill, intent_file_handler
from padatious import IntentContainer
from adapt.intent import IntentBuilder
from mycroft.skills.core import intent_handler
from os.path import join, expanduser, exists
from pyfrotz import Frotz
import time

game_name = "planet fall"


class PlanetFall(MycroftSkill):
    save_file = expanduser(join("~", ".planetfall.save"))
    playing = False
    container = None

    def initialize(self):
        self.game = None
        self.current_room = None
        self.last_interaction = time.time()
        self._init_padatious()
        self.disable_intent("Save")
        self.game_data = join(self.root_dir, 'planetfall.z5')
        self.frotz_path = expanduser("~/frotz/dfrotz")

    def _init_padatious(self):
        # i want to check in converse method if some intent by this skill will trigger
        # however there is no mechanism to query the intent parser
        # PR incoming
        intent_cache = expanduser(self.config_core['padatious']['intent_cache'])
        self.container = IntentContainer(intent_cache)
        for intent in ["restore.intent", "play.intent", "credits.intent"]:
            name = str(self.skill_id) + ':' + intent
            filename = self.find_resource(intent, 'vocab')
            if filename is not None:
                with open(filename, "r") as f:
                    self.container.add_intent(name, f.readlines())
        self.container.train()

    def will_trigger(self, utterance):
        # check if self will trigger for given utterance
        # adapt match
        if self.voc_match(utterance, "save"):
            return True
        # padatious match
        intent = self.container.calc_intent(utterance)
        if intent.conf < 0.5:
            return False
        return True

    def get_intro_message(self):
        """ Get a message to speak on first load of the skill.

        Useful for post-install setup instructions.

        Returns:
            str: message that will be spoken to the user
        """
        self.speak_dialog("thank.you", {"name": game_name})
        return None

    def speak_output(self, line):
        # replace type with say because its voice game
        lines = line.lower().replace("type", "say").split(".")
        for line in lines:
            self.speak(line.strip(), expect_response=True, wait=True)
        self.last_interaction = time.time()
        self.maybe_end_game()

    @intent_file_handler("credits.intent")
    def handle_credits(self, message=None):
        self.speak_dialog("credits", {"name": game_name})

    @intent_file_handler("play.intent")
    def handle_play(self, message=None):
        self.playing = True
        self.enable_intent("Save")
        if self.game is None:
            self.game = Frotz(self.game_data, interpreter=self.frotz_path, save_file=self.save_file)
        self.speak_output(self.game.get_intro())
        self.current_room = self.do_command("look")

    @intent_handler(IntentBuilder("Save").require("save")
                    .optionally("planet").optionally("fall"))
    def handle_save(self, message=None):
        if not self.playing:
            self.speak_dialog("save.not.found")
        else:
            self.game.save()
            self.speak_dialog("game.saved", {"name": game_name})

    @intent_file_handler("restore.intent")
    def handle_restore(self, message):
        if exists(self.save_file):
            self.playing = True
            if self.game is None:
                self.game = Frotz(self.game_data, interpreter=self.frotz_path, save_file=self.save_file)
            self.game.restore()
            self.speak_dialog("restore.game", {"name": game_name})
            self.enable_intent("Save")
        else:
            self.speak_dialog("save.not.found")
            new_game = self.ask_yesno("new.game", {"name": game_name})
            if new_game:
                self.handle_play()

    def game_ended(self):
        return self.game.game_ended()

    def maybe_end_game(self):
        # end game if no interaction for 10 mins
        if self.playing:
            timed_out = time.time() - self.last_interaction > 10 * 3600
            if timed_out:
                self.handle_save()
            if timed_out or self.game_ended():
                self.disable_intent("Save")
                self.playing = False
                self.game = None

    def do_command(self, utterance):
        if self.game_ended():
            self.speak_dialog("game.ended")
            return
        # this may return empty string if the game ended
        data = self.game.do_command(utterance)
        if not data:
            self.playing = False
            return None
        else:
            room = data[0]
            description = data[1]
            self.speak_output(room)
            self.speak_output(description)
        return room

    def converse(self, utterances, lang="en-us"):
        """ Handle conversation.

        This method gets a peek at utterances before the normal intent
        handling process after a skill has been invoked once.

        To use, override the converse() method and return True to
        indicate that the utterance has been handled.

        Args:
            utterances (list): The utterances from the user
            lang:       language the utterance is in

        Returns:
            bool: True if an utterance was handled, otherwise False
        """
        # check if game was abandoned mid conversation and we should clean it up
        self.maybe_end_game()
        if self.playing:
            ut = utterances[0]
            # if self will trigger do nothing and let intents handle it
            if self.will_trigger(ut):
                # save / restore will trigger
                return False
            # capture speech and pipe to the game
            self.do_command(ut)
            # check for game end
            if self.game_ended():
                self.playing = False
            return True
        return False


def create_skill():
    return PlanetFall()
