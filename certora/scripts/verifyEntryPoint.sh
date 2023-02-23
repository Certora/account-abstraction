certoraRun.py \
  contracts/core/EntryPoint.sol certora/harness/SymbolicAccount.sol \
  --verify EntryPoint:certora/specs/entryPoint.spec \
 --solc solc8.12 \
 --staging master \
 --optimistic_loop \
 --msg "entrypoint $1"