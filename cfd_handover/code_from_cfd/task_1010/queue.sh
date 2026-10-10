#!/bin/bash
# worker: takes the next unclaimed line of queue.txt (flock), runs run_geom_mesh.sh; run 2 workers in parallel. 14_T5n_12p5 (D14) is a mesh-only variant handled after 14_T5n.
H=/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010; cd $H
while true; do
  line=$(flock queue.lock bash -c 'n=$(cat claimed 2>/dev/null || echo 0); l=$(sed -n "$((n+1))p" queue.txt); [ -n "$l" ] && echo $((n+1)) > claimed; echo "$l"')
  [ -z "$line" ] && break
  IFS='|' read -r pk lab menv var <<< "$line"
  ./run_geom_mesh.sh "$pk" "$lab" "$menv" "$var"
  if [ "$lab" = 14_T5n ] && [ -f out/14_T5n/case.stl ]; then ln -sfn $H/out/14_T5n $H/out/14_T5n_12p5; ./run_geom_mesh.sh "$pk" 14_T5n_12p5 "M1_THROAT_REQ=0.00002" "--variant=3"; fi
done
echo "$(date +%F_%T) worker $$ done" >> runs.log
