#!/bin/sh
# Run exactly the inventoried original files. No reader fixes or transformations.
set -eu
cd /corpus
limit=$1
while IFS= read -r id; do
    printf 'started\n' > "/out/$id.started"
    start=$(date +%s)
    code=0
    timeout --signal=TERM --kill-after=5 "$limit" swipl -q -f "cases/$id.pl" \
        >"/out/$id.stdout" 2>"/out/$id.stderr" || code=$?
    end=$(date +%s)
    printf '%s\t%s\t%s\n' "$code" "$start" "$end" > "/out/$id.status"
done < /out/input_ids.txt
