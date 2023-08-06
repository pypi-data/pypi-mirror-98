# Try to follow 'semmantic versioning' scheme, e.g. https://semver.org/
__version__ = '1.2.3'


class BuildToolsTemplate:
    
    def __init__(self, cli_path=[], cli_descriptions={}, summary=None):
        self.cli_path = cli_path
        self.cli_descriptions = cli_descriptions
        self.summary = summary
    
    def run(self, args):
        pass

    def config_parser(self, parser, parents=[]):
        pass
