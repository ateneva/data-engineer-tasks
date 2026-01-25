
# Setting Up

## Review GIT configuration

```bash
git config user.name          # display the configured user name
git config user.email         # display the configured email
git config core.editor        # display the configured editor
git config core.excludesfile  # review excluded files
```

### Configure GIT

```bash
git config --global user.email ateneva@gmail.com
git config --global user.name angelinateneva
git config --global core.editor atom

# config all new repos to default to main
git config --global init.defaultBranch main

# configure default branch name for all repositories
git config --global init.defaultBranch <name>

# configure default pull strategy
git config --global pull.rebase false  # merge local branches when pulling
git config --global pull.rebase true   # rebase pull strategy
git config --global pull.ff only       # fast-forward only
```

[EXPLANATION](<https://www.atlassian.com/git/tutorials/syncing/git-pull>)

**PRO:**

* <https://sdqweb.ipd.kit.edu/wiki/Git_pull_--rebase_vs._--merge>

* <https://coderwall.com/p/7aymfa/please-oh-please-use-git-pull-rebase>

* <https://spin.atomicobject.com/2020/05/05/git-configurations-default/>

**CON:**

* <https://stackoverflow.com/questions/2472254/when-should-i-use-git-pull-rebase>

### Add `.gitignore` file

```bash
# specify a global exclusion list
git config --global core.excludesfile ~/.gitignore

# adding .DS_Store to that list
echo .DS_Store >> ~/.gitignore

# remove any existing files from the repo, skipping over ones not in repo
find . -name .DS_Store -print0 | xargs -0 git rm --ignore-unmatch
```

### Clone a remote repository

```bash
mkdir prj
cd prj
git clone <url-to-project-name.git>
```

### Create local repository

```bash
mkdir proj
cd proj
git init
```

### Add local repository as a remote

```bash
git remote add origin <url-to-project-name.git>

git add README.md
git commit -m "initial commit"

# setup tracking b/n local and remote
git push -u [<remote>] [<branch>]
git push -u git@gitlab.example.com:namespace/nonexistent-project.git main
git push origin -u <branch_name>

OR

git push --set-upstream <remote> <branch>
git push --set-upstream git@gitlab.example.com:namespace/nonexistent-project.git main
```

### Rename/Remove remote repository

```bash
git remote rename <old> <new>
git remote remove <name>
```

* <https://www.git-tower.com/learn/git/faq/set-upstream/>

### Change local repo default tracking branch

```bash
git branch -m master main       # move from master to main
git fetch origin
git branch -u origin/main main  # set up tracking to main
```

# Daily Usage

## Branches

### review remote repository commit history

```bash
git log
git log --all                           # shows both local and tracking branches
git log --stat                          # shows more details about the commit

git log --oneline                       # shortens the GIT IDs
git log --oneline -2                    # shows the last two commits on current branch
git log --oneline --graph -10           # shows the last 10 commits in a graph

git log origin/master --oneline -5      # shows the last 5 commits on master branch
git log origin --oneline -5             # shows the last 5 commits on default tracking branch

git log -S <keyword>                    # search previously committed files for certain keyword

git reflog                              # review history of all actions that git took
```

### create a new branch

```bash
git branch <branch name>                          # create a new branch
git checkout <branch name>                        # switch to a different branch
git checkout -b <branch name>                     # create a new branch and switch to it

git branch -m <old branch name> <new branch name> # rename a branch without switching to it
git push origin -u <new_name>                     # update the remote tracking reference
git push origin --delete <old_name>               # delete the old remote branch
```

### review existing branches

```bash
git branch
git branch -r         # display only remote branches
git branch -a         # display both remote and local branches

git branch --remote   # display only remote branches
git branch --all      # display both remote and tracking branches
git branch -vv        # display the corresponding tracking branches to your local ones
```

### merge branches

```bash
git merge <branch>
git merge <branch> --ff        # fast-forward merge
git merge <branch> --no-ff     # merge commit
git merge <branch> --ff-only   # abort merge if fast-forward not possible
```

* <https://www.atlassian.com/git/tutorials/using-branches/git-merge>

### squash merge

```bash
# could be a handy strategy to keep commit history clean
# it only works if the original branch is deleted

git checkout master
git merge --squash featureX --ff  
git commit -m "merge featureX into development"
git push origin development
git push -d origin featureX
```

### merge conflicts

```bash
git merge --abort
git checkout --ours [filename]          # keep your changes
git checkout --theirs [filename]        # keep their changes

git fetch origin                        # pull only a specific commit
git checkout [sha]
```

### delete branches

```bash
git branch -d <branch name>             # delete local branch only
git branch -D <branch name>             # delete branch with unmerged commits
git push -d <remote_name> <branch_name> # delete remote branch
git push -d origin <branch_name>        # often remote name is origin
git push origin --delete <branch_name>  # delete the remote branch

git remote prune origin                 # remove local tracking branches that have been deleted on the remote
```

* <https://stackoverflow.com/questions/7726949/remove-tracking-branches-no-longer-on-remote>

## Committing

### check local repository status

```bash
git status
git status -s
git status --short

git status -l
git status --long

git status -v
git status --verbose
```

### show current commit

```bash
git show HEAD -s                 # show current commit on current branch
git show origin/master HEAD -s   # show current commit on master branch
```

### show commits difference between two branches

```bash
# both branches you're comparing must be checked out
git rev-list --left-right --pretty=oneline development...master

# every commit sha is preceded by < or > to indicate which branch it can be found on
```

### stage & commit files

```bash
git add <file>
git add <directory>
git add .

git commit -m "Commit message here"

git push origin feature/login
git push origin master
```

### amend a commit message

```bash
# modify the latest commit
git commit --amend -m "New commit message"
git commit --amend --author="John Doe <john@doe.org>"
git commit --amend --author="ateneva<tenevaa21@gmail.com>" -m "use explicit field names"

# modify commits no matter how long ago they were
git rebase --interactive <parent commit SHA>
git commit --amend
git rebase --continue
```

If the commit has already been pushed then you will need to force push after amending

* <https://stackoverflow.com/questions/179123/how-to-modify-existing-unpushed-commit-messages>

* <https://www.git-tower.com/learn/git/faq/change-author-name-email>
* <https://thoughtbot.com/blog/git-interactive-rebase-squash-amend-rewriting-history>
* <https://stackoverflow.com/questions/30194796/git-rebase-whats-the-difference-between-edit-and-reword>

### push force

* needed to sync your remote branch after rebasing local branch

```bash
git push origin <branch> -f
git push origin <branch> --force
git push <remote> <branch> -f
```

* <https://stackoverflow.com/questions/43567577/what-is-the-different-between-force-push-and-normal-push-in-git>#

* <https://stackoverflow.com/questions/5509543/how-do-i-properly-force-a-git-push>

* <https://stackoverflow.com/questions/34995726/why-when-should-one-ever-force-push>

### discard local changes

```bash
git clean -df               # discard untracked files
git checkout -- <file>      # disard changes to a tracked file
git checkout -- .           # disccard changes to all tracked files
git rm <filename> --cached  # unstage a file from working tree
git rm <filename> -f        # remove a file completely from working tree
```

### unstage files

```bash
git restore --staged <file>
git restore --staged <directory>
git restore --staged .

OR

git reset HEAD -- <file>        # discard changes in modified files
git reset HEAD -- <directory>   # discard changes in modified files
```

### stash local changes

```bash
# keeps a copy of your uncommitted changes in stashes
# and removes them from working tree so you can switch between branches
# only applies to files that are already tracked
git stash

# to stash untracked files
git stash -u

# list all your stashes
git stash list

# restore your stashed changes to working tree and remove them from stashes
# this only applies to the latest stash
git stash pop

# restore your stashed changes to working tree and keep them in your stash
# useful if you want to:
    # apply stashes to multiple branches
    # restore an earlier stash
git stash apply stash@{3}

# clean up a stash
git stash drop stash@{1}

# delete all your stashes
git stash clear
```

# Advanced Tips

<https://www.atlassian.com/git/tutorialsc>

## Merging vs. Rebasing

The major benefit of rebasing is that you get a much cleaner project history.

First, it eliminates the unnecessary merge commits required by git merge
Second, rebasing also results in a perfectly linear project history
    —you can follow the tip of feature all the way to the beginning of the project without any forks.

* It can be harmful to do it in shared branches.
* It can cause complex and hard to resolve merge conflicts.
In these cases, instead of rebasing your branch against the default branch,
consider pulling it instead (git pull origin master).

* It has a similar effect without compromising the work of your contributors.

* So, before you run git rebase, always ask yourself, “Is anyone else looking at this branch?”
  * If the answer is yes, take your hands off the keyboard and start thinking about a non-destructive way to make your changes
    * (e.g., the `git revert` command). Otherwise, you’re safe to re-write history as much as you like.

```bash
git fetch origin main
git checkout my-feature-branch

git pull --rebase origin development
git checkout --ours <file name>       # keep their changes over mine in case of merge conflicts

git add .
git commit -m "sync with development"
git rebase --continue                 # finish rebasing after selecting the changes

# redo your changes and add them with 
git add .
git commit -m <messsage> 
git push origin my-feature-branch -f  # a rebased branch needs force-pushing
```

### note the difference in flags between git merge and git rebase

```bash
git rebase --theirs branch-b          # keep my changes over theirs
git merge --theirs  branch-b          # keep their changes over mine
```

If you try to push the rebased main branch back to a remote repository,
    Git will prevent you from doing so because it conflicts with the remote main branch.
But, you can force the push to go through by passing the --force flag, like so:

* <https://www.atlassian.com/git/tutorials/merging-vs-rebasing>

* <https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase>

* <https://docs.gitlab.com/ee/topics/git/git_rebase.html>

* <https://medium.com/osedea/git-rebase-powerful-command-507bbac4a234>

* <https://stackoverflow.com/questions/52625081/git-pull-another-remote-branch-into-my-local-branch>

* <https://howchoo.com/git/git-merge-conflicts-rebase-ours-theirs#using-ours-theirs-during-a-rebase>

## Resetting & Reverting

You can also think of:

* git revert as a tool for undoing committed changes,
* git reset HEAD is for undoing uncommitted changes.

* `commit level`

```bash
git reset HEAD          # reset local branch to the latest commit
git reset <commit>      # reset local branch to a specific commit


git revert HEAD         # revert the latest pushed commit
git revert <commit SHA> # revert any previously pushed commit

# revert and apply a previous commit on your mocal branch
git revert -n <commit SHA>
git revert --no-commit <commit SHA>
```

* `file level`

```bash
git reset       # unstage a file
git checkout    # discard chnages in the working directory
```

* <https://www.atlassian.com/git/tutorials/resetting-checking-out-and-reverting>

## Cherry picking

`git cherry-pick` is a powerful command that enables arbitrary Git commits to be picked by reference and appended to the current working HEAD

* Bug hotfixes
When a bug is discovered it is important to deliver a fix to end users as quickly as possible.

* Undoing changes and restoring lost commits
Sometimes a feature branch may go stale and not get merged into main.
Sometimes a pull request might get closed without merging.
Git never loses those commits and through commands like git log and git reflog they can be found and cherry picked back to life.

```bash
git checkout main
git cherry-pick <commit SHA>

# apply changes from a different unmerged branch to the current one

git cherry-pick -n <commit SHA>
git cherry-pick --no commit <commit SHA>
```

* <https://www.atlassian.com/git/tutorials/cherry-pick>
