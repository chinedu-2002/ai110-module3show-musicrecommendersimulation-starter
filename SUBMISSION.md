# Finish and Submit

The code, expanded catalog, evaluation captures, README, and model card are prepared locally. GitHub publication and course submission have not been performed.

1. Run `python -m src.main --all-profiles` and read the reasons. Review the reflection in `model_card.md`; revise it so it describes your own understanding and experience.
2. Fork the [official starter repository](https://github.com/codepath/ai110-module3show-musicrecommendersimulation-starter) into your GitHub account. Keep the fork public, as the assignment requires.
3. From a terminal in this project folder, point `origin` at **your fork**. The original remote points to CodePath. Replace `YOUR_GITHUB_USERNAME` below before running these commands:

   ```console
   git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/ai110-module3show-musicrecommendersimulation-starter.git
   git remote -v
   git log --oneline -5
   git push -u origin main
   ```

4. If you changed the reflection or other files, commit those changes and push again:

   ```console
   git add model_card.md README.md
   git commit -m "Personalize reflection after reviewing recommendation results"
   git push origin main
   ```

5. Open your GitHub repository in a signed-out browser to verify it is public and contains the code, data, README, model card, AI log, tests, and evaluation files.
6. Use the assignment's **Submit** button in CodePath Courses and submit your repository URL. Confirm the course site records your submission.

The assignment PDF lists a deadline of **Sunday, November 1, 2026, at 10:59 PM CST**. Check your live course page for any updates.

The public starter history is retained. Local implementation and documentation commits record the actual work; no commits are backdated. The PDF and temporary PDF-reader dependency are outside this repository and are not part of the project submission.

The accompanying ZIP contains source files and documentation, without Git history. The commands above assume you use the original `music-recommender` working folder. If starting from the ZIP on another computer, first clone your own fork, copy the ZIP's files into that checkout, and create commits for the changes before pushing.
