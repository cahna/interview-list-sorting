#!/bin/sh

INPUT_FILE=$1

if [ ! -f "$INPUT_FILE" ]; then
  echo "Missing input file argument" > /dev/stderr
  exit 1
fi

for alg in 'iterator' 'generator' 'generator2' 'generator3'; do
  echo "Profiling execution for $alg..."
  python -m cProfile -o "$alg.prof" list_sorting/cli.py --algorithm $alg "$INPUT_FILE" /dev/null
  gprof2dot -f pstats "$alg.prof"|dot -Tpng -o "$alg.png"

  echo "Profiling memory for $alg..."
  bname=$(basename "$INPUT_FILE")
  mprof run \
    --python \
    --timeout 120 \
    --output "mprofile_${alg}_${bname}.dat" \
    list_sorting/cli.py --algorithm $alg "$INPUT_FILE" /dev/null
done
