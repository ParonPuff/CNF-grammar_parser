#!/usr/bin/env bash
# fast_generate.sh
# Usage: ./fast_generate.sh <start> <step> <stop>

set -euo pipefail

if [ $# -ne 3 ]; then
  echo "Usage: $0 <start> <step> <stop>"
  exit 1
fi

START=$1
STEP=$2
STOP=$3

# For each target length n:
#  • n=1 → "b"
#  • odd n>=3 → a^((n-1)/2) b c^((n-1)/2)
#  • even n>=2 → a^((n-2)/2) b b c^((n-2)/2)

repeat_char() {
  # usage: repeat_char char count
  # prints char repeated count times
  local ch=$1 count=$2
  # POSIX-safe repeat
  printf "%${count}s" | tr ' ' "$ch"
}

for ((n = START; n <= STOP; n += STEP)); do
  if (( n == 1 )); then
    echo "b"
  elif (( n % 2 == 1 )); then
    # odd lengths: m = (n-1)/2
    m=$(( (n - 1) / 2 ))
    printf "%s" "$(repeat_char a "$m")"
    printf "b"
    printf "%s\n" "$(repeat_char c "$m")"
  else
    # even lengths: m = (n-2)/2
    m=$(( (n - 2) / 2 ))
    printf "%s" "$(repeat_char a "$m")"
    printf "bb"
    printf "%s\n" "$(repeat_char c "$m")"
  fi
done
