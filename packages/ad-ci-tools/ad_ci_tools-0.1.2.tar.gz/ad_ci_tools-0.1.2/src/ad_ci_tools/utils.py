from git import Repo


class JenkinsRepo(Repo):

    def get_git_data(self):
        """
            Return git repo data.
            In case of branch retun {branch: _name_}
            In case of pr return {pull_request: _number_}
        """

        describe = self.git.describe('--all')
        # branch name may be feature/my_branch, so we split only first 2 `/`
        describe_list_branch = describe.split('/', 2)
        # cant use same split for branch and pr case
        describe_list_pr = describe.split('/', 2)
        reponame = self.remotes.origin.url.split('/')[-1].split('.git')[0]
        repoowner = self.remotes.origin.url.split('/')[-2].split('.com:')[-1]

        data = {'reponame': reponame, 'repoowner': repoowner}
        # pull request case
        # it works basically on ci with
        # clean git init and fetch remote with +refs/pull/*:refs/origin/pr/*
        # in onther cases with high chance it wont detect pr
        if describe_list_pr[1] == 'pr' and len(describe_list_pr) > 2:
            data.update({'pull_request': describe_list_pr[2]})
            return data
        # tags case
        if describe_list_branch[0] == 'tags':
            branch = next(filter(
                lambda x: 'origin' in x,
                self.git.branch('-a', '--contains', describe).splitlines())).split('/')[2]
        # all others case
        else:
            try:
                branch = describe_list_branch[2]
            except IndexError:
                branch = self.git.rev_parse('--abbrev-ref', 'HEAD')

        data.update({'branch': branch})
        return data
