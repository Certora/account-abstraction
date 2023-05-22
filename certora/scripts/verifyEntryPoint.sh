certoraRun.py \
  contracts/core/EntryPoint.sol certora/harness/SymbolicAccount.sol \
  --verify EntryPoint:certora/specs/entryPoint.spec \
 --solc solc8.12 \
 --staging master \
 --optimistic_loop --optimistic_hashing --settings -optimisticFallback=true,-depth=25,-t=400,-dontStopAtFirstSplitTimeout=true \
 --link EntryPoint:constantSender=SymbolicAccount \
 --loop_iter 1 \
 --msg "entrypoint $1"
