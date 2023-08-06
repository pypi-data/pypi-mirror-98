import json

# For convenience, import all util/ packages into the 'util' module, e.g. so that we can do 'import buildtools.util.MarkdownComment'
from buildtools.util.markdown_comment_builder import MarkdownComment, BitbucketMarkdownComment, TeamsMarkdownComment
from buildtools.util.teams_card_builder import TeamsCard, TeamsCardSection, TeamsCardTemplate, TeamsCardTemplateError
from buildtools.util.ansible_json_parser import AnsibleJSONParser, AnsibleResults, AnsibleTaskResults

def readfile(path):
    with open(path) as f:
        return f.read()

def is_nonempty_str(obj):
    return isinstance(obj, str) and len(obj) > 0

def hasattr_nonempty_str(obj, attribute):
    return hasattr(obj, attribute) and is_nonempty_str(getattr(obj, attribute))

def parse_ansible_json(json):
    parser = AnsibleJSONParser()
    return parser.parse(json)

