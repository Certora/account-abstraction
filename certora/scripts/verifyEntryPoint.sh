certoraRun \
  contracts/core/EntryPoint.sol certora/harness/SymbolicAccount.sol \
  --verify EntryPoint:certora/specs/entryPoint.spec \
 --solc solc8.12 \
 --staging master \
 --optimistic_loop --optimistic_hashing --settings -optimisticFallback=true  \
 --link EntryPoint:constantSender=SymbolicAccount \
 --msg "entrypoint $1" \
 --rule verifyMsgData
 