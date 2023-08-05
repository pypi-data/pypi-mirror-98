import json
import argparse
import importlib

from types import SimpleNamespace
from barbell2.utils import Logger, current_time_secs, elapsed_secs


class ScriptRunner:

    def __init__(self):
        self.scripts = []
        self.logger = Logger(prefix='log_etl')

    def execute(self):
        if len(self.scripts) == 0:
            self.logger.print('Nothing to execute')
            return
        start_total = current_time_secs()
        for script in self.scripts:
            self.logger.print('Starting script {}'.format(script.name))
            start = current_time_secs()
            script.execute()
            self.logger.print('Script finished after {} seconds'.format(elapsed_secs(start)))
        self.logger.print('Runner finished after {} seconds'.format(elapsed_secs(start_total)))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('params',
                        help='Path to params.json file')
    args = parser.parse_args()
    with open(args.params, 'r') as f:
        params = json.load(f)
    params = SimpleNamespace(**params)

    runner = ScriptRunner()
    for script in params.scripts:
        script = getattr(importlib.import_module('hpb_mumc_dashboard.etl.scripts'), script)
        runner.scripts.append(script(runner, params))
    runner.execute()


if __name__ == '__main__':
    main()
