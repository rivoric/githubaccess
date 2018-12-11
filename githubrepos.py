from __future__ import print_function, with_statement
from _utils import githuboptparse, githublogin, get_filtered_repos

if __name__ == "__main__":
    parser = githuboptparse()
    # add additional options here with parser.add_option
    options, additional_args = parser.parse_args()

    ghcon = githublogin(options)
    if ghcon is None:
        print("No login details specified")
        parser.parse_args(['-h'])

    for repo in get_filtered_repos(ghcon, options):
        print(repo.name)
