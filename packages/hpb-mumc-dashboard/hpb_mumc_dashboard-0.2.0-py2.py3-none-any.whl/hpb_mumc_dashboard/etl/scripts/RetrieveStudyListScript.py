from barbell2.castorclient import CastorClient
from . import BaseScript


class RetrieveStudyListScript(BaseScript):

    def __init__(self, runner, params):
        super(RetrieveStudyListScript, self).__init__('RetrieveStudyListScript', runner, params)

    def execute(self):
        client = CastorClient()
        study_list = client.get_studies()
        for study in study_list:
            self.runner.logger.print(study)
