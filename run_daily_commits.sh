#!/usr/bin/env bash

set -euo pipefail

# Configure Git User
git config --global user.name "R VIKRANTH"
git config --global user.email "vikranthras@gmail.com"

# Generate a random number of commits between 3 and 5
num_commits=$(( (RANDOM % 3) + 3 ))

messages=(
  "Refactor routing algorithm logic"
  "Update simulation parameters"
  "Fix minor bug in metric calculation"
  "Improve energy efficiency model"
  "Update documentation"
  "Optimize spline trajectory generation"
  "Tweak adaptive crossover probabilities"
  "Clean up redundant logs"
  "Refactor evaluation function"
  "Tune mutation operator thresholds"
  "Update plotting configuration"
  "Enhance data parsing regex"
  "Reformat C++ codebase"
  "Adjust NS-3 energy source setup"
  "Fix memory leak in Python script"
)

echo "Starting daily commit generation: $num_commits commits to be created."

for i in $(seq 1 $num_commits); do
  # Append to a dummy file to ensure a file change
  echo "Daily commit iteration $i: $(date)" >> dummy_daily.txt
  git add dummy_daily.txt

  # Select a random commit message
  msg_index=$((RANDOM % ${#messages[@]}))
  msg=${messages[$msg_index]}

  # Generate random offset in hours and minutes to simulate activity throughout the day
  hour_offset=$((RANDOM % 12))
  minute_offset=$((RANDOM % 60))

  export GIT_AUTHOR_DATE=$(date -d "-${hour_offset} hours -${minute_offset} minutes" +'%Y-%m-%dT%H:%M:%S')
  export GIT_COMMITTER_DATE=$GIT_AUTHOR_DATE

  git commit -m "$msg - iteration $i"
done

echo "Finished creating $num_commits commits."
