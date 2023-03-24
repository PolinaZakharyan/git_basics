# Git intro task

```bash
mkdir cursor && cd cursor   # Create a new directory and navigate to it
git init                    # Initialize a new repository in the created directory
mkdir task_01 && cd task_01 # Create a project directory and navigate to it
touch README.md             # Add readme
git add --all && git commit # Commit all changes
git branch first_branch     # Create a new branch 'first_branch'
echo " ..." >> README.md    # Modify README.md
git status                  # Display the status of the working directory
git add --all && git commit # Commit all changes
git checkout master         # Switch back to the master branch
echo " ..." >> README.md    # Modify README.md
git add --all && git commit # Commit all changes
git log                     # Display the project history
```


