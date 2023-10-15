from api import HeadHunterAPI, SuperJobAPI
import copy


class UserRequest:

    params_default = {}

    def __init__(self):
        self.hh_api = HeadHunterAPI()
        self.sj_api = SuperJobAPI()
        self.params = copy.deepcopy(self.params_default)

    def __call__(self, *args, **kwargs):
        pass
