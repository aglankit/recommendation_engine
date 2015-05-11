#!/bin/bash

echo "==== Users-kNN ==="
for outer in $(seq 3 2 15)
do
  echo "k = $outer"
  for inner in $(seq 5)
  do
    echo
    echo "Iteration $inner"
    python cf_users_knn_jaccard.py u$inner.base u$inner.test $outer
    #python cf_users.py u$inner.base u$inner.test $outer
    #echo u$inner.base u$inner.test $outer
  done
done

echo "==== Items-kNN ==="
for outer in $(seq 1 2 15)
do
  echo "k = $outer"
  for inner in $(seq 5)
  do
    echo
    echo "Iteration $inner"
    python cf_items_knn_jaccard.py u$inner.base u$inner.test $outer
    #python cf_users.py u$inner.base u$inner.test $outer
    #echo u$inner.base u$inner.test $outer
  done
done


#for i in $(seq 5) 
#do
#   echo
#   echo "Iteration $i"
#   python cf_users.py u$i.base u$i.test
#done

#echo "==== Items-kNN ==="
#for i in $(seq 5)
#do
#   echo
#   echo "Iteration $i"
#   python baseline.py u$i.base u$i.test
#done

