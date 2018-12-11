from github import Github
import optparse
import re

def githuboptparse():
    """Returns an optparse.OptionParser object with the standard github options"""
    parser = optparse.OptionParser()
    parser.add_option('-u', '--username', action="store", dest="user",
                      help="Github username to log in with (requires password as well)")
    parser.add_option('-p', '--password', action="store", dest="pwd",
                      help="Github password to log in with (requires username as well)")
    parser.add_option('-t', '--pat', action="store", dest="pat",
                      help="Github Personal Access Token, PAT, to connect with (instead of username/password)")
    parser.add_option('-o', '--organization', action="store", dest="org",
                      help="Report access to repos owned by organisation")
    parser.add_option('-i', '--include', action="store", dest="inc",
                      help="Regular expression of repos to include, will include all by default")
    parser.add_option('-e', '--exclude', action="store", dest="exc",
                      help="Regular expression of repos to exclude, will not exclude any by default")
    return parser


def githublogin(options):
    """Returns the Github login given the optparse options (see githuboptparse)"""
    if options.user and options.pwd:
        return Github(options.user, options.pwd)
    elif options.pat:
        return Github(options.pat)
    else:
        print("No login details specified")
        parser.parse_args(['-h'])


def get_filtered_repos (githublogin, options):
    """Retuns the repos filtered by the optparse options (see githuboptparse)"""
    if options.org:
        # reports on just the organizations repos
        _elements = githublogin.get_organization(options.org)
    else:
        # report on all repos the user has access to
        _elements = githublogin.get_user()

    if options.inc:
        # create a regular expressions to match includes against
        _inc = re.compile(options.inc)
    else:
        _inc = None

    if options.exc:
        # create a regular expressions to match includes against
        _exc = re.compile(options.exc)
    else:
        _exc = None

    for element in _elements.get_repos():
        if _inc and _exc:
            if _inc.search(element.name) and not _exc.search(element.name):
                yield element 
        elif _inc:
            if _inc.search(element.name):
                yield element 
        elif _exc:
            if not _exc.search(element.name):
                yield element 
        else:
            yield element
