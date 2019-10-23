from __future__ import print_function, with_statement
from _utils import githuboptparse, githublogin, get_filtered_repos

def has_slack_webhook (hooks):
    """Goes through all the web hooks checking if any URL references slack"""
    found = False

    for temp_hook in hooks:
        if temp_hook.config['url'][:23].lower() == 'https://hooks.slack.com':
            found = True

    return found

if __name__ == "__main__":
    parser = githuboptparse()
    parser.add_option('-w', '--webhook', action="store", dest="webhook",
                      help="Slack webhook")
    options, additional_args = parser.parse_args()

    ghcon = githublogin(options)
    if ghcon is None:
        print("No login details specified")
        parser.parse_args(['-h'])

    if options.webhook:
        hook_config = {
            "url": options.webhook,
            "content_type": "json"
        }
        hook_events = ['pull_request', 'pull_request_review', 'pull_request_review_comment']
    else:
        print("You need to provide Slack webhook")
        parser.parse_args(['-h'])

    for repo in get_filtered_repos(ghcon, options):
        if not has_slack_webhook(repo.get_hooks()):
            print("Adding Slack webhook to {name}".format(name=repo.name))
            repo.create_hook("web", hook_config, hook_events, active=True)
