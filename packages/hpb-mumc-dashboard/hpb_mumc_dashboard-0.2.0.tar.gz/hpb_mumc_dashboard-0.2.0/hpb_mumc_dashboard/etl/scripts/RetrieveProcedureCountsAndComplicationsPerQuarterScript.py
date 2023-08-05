from . import BaseScript


class RetrieveProcedureCountsAndComplicationsPerQuarterScript(BaseScript):

    def __init__(self, runner, params):
        super(RetrieveProcedureCountsAndComplicationsPerQuarterScript, self).__init__(
            'RetrieveProcedureCountsAndComplicationsPerQuarterScript',
            runner, params
        )

    def execute(self):
        print('hello!')
