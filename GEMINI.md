# Gemini CLI Mandates

- **GIT Shortcut (`--git`):** When the user provides the input `--git`, I MUST autonomously perform the following workflow without further confirmation:
    1. Run `git status` and `git diff HEAD` to analyze all changes (staged and unstaged).
    2. Stage all relevant changes using `git add`.
    3. Analyze recent commit history (`git log -n 5`) to match the project's commit message style (verbosity, tone, and formatting).
    4. Generate and apply a professional, concise commit message that describes the "why" and "what" of the changes.
    5. Push the commit to the current branch on the remote repository (`git push`).
    6. Report a brief summary of the commit and the push status once completed.