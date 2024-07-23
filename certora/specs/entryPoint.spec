//using SymbolicAccount as account;

methods {

    function Exec.call(
        address to,
        uint256 value,
        bytes memory data,
        uint256 txGas
    ) internal returns (bool) => execCallSummary(to, value, data, txGas);
    //function SymbolicAccount.called() external returns (bool) envfree;

    //
    function _.createSender(bytes initCode) external => NONDET;

    // Paymaster
   // validatePaymasterUserOp(EntryPoint.UserOperation  userOp, bytes32 userOpHash, uint256 maxCost)=> NONDET

    function _.validateUserOp(EntryPoint.PackedUserOperation userOp,bytes32 hash,uint256 missingFunds) external => validateUserOpSummary(userOp, hash, missingFunds) expect uint256;
    function _.validatePaymasterUserOp(EntryPoint.PackedUserOperation userOp, bytes32 userOpHash, uint256 maxCost) external => NONDET;

    function SymbolicAccount.validateUserOp(EntryPoint.PackedUserOperation calldata userOp,bytes32 hash,uint256 missingFunds) internal returns (uint256) => validateUserOpSummary(userOp, hash, missingFunds);
    //function SymbolicAccount.validatePaymasterUserOp(EntryPoint.PackedUserOperation calldata userOp, bytes32 userOpHash, uint256 maxCost) internal returns (bytes memory, uint256) => NONDET;


    function balanceOf(address) external returns (uint256) envfree;
    function _compensate(address beneficiary, uint256 amount) internal  => NONDET;
    function _createSenderIfNeeded(uint256 opIndex, EntryPoint.UserOpInfo memory opInfo, bytes calldata initCode) internal => NONDET;

    function _.postOp(IPaymaster.PostOpMode mode, bytes context, uint256 actualGasCost, uint256 actualUserOpFeePerGas) external => NONDET;


    //function SymbolicAccount.validatedLength()  external returns (uint256) envfree;
    //function SymbolicAccount.calledLength()  external returns (uint256) envfree;
    //function SymbolicAccount.called_data(uint256 index) external returns (bytes) envfree;
    //function SymbolicAccount.validated_data(uint256 index) external returns (bytes) envfree;
    //function SymbolicAccount.eq(uint256 index) external returns (bool) envfree;

    function _._ external => DISPATCH [
// //        _.validateUserOp(EntryPoint.PackedUserOperation,bytes32,uint256),
// //        _.validatePaymasterUserOp(EntryPoint.PackedUserOperation, bytes32, uint256),
        EntryPoint.innerHandleOp(bytes,EntryPoint.UserOpInfo,bytes),
//        EntryPointSimulations.innerHandleOp(bytes,EntryPoint.UserOpInfo,bytes)
    ] default HAVOC_ALL;
}

persistent ghost mathint numValidated;
persistent ghost mathint numExecuted;
persistent ghost bool executionValidated;
persistent ghost mapping(mathint => bytes32) validatedUserOpHash;

function validateUserOpSummary(EntryPoint.PackedUserOperation userOp,bytes32 hash,uint256 missingFunds) returns uint256 {
    require userOp.callData.length != 0;
    validatedUserOpHash[numValidated] = keccak256(userOp.callData);
    numValidated = numValidated + 1;
    uint256 validationData;
    return validationData;
}

function execCallSummary(address to, uint256 value, bytes data, uint256 txGas) returns bool {
    if (numExecuted >= numValidated ||
        validatedUserOpHash[numExecuted] != keccak256(data)) {
            executionValidated = false;
    }
    numExecuted = numExecuted + 1;
    bool result;
    return result;
}

//// # Verifies that certain function always revert as expected */
rule alwaysRevert(method f)
filtered { f->
//        f.selector == sig:EntryPointSimulations._validateSenderAndPaymaster(bytes,address,bytes).selector ||
        f.selector == sig:getSenderAddress(bytes).selector
}
{
    env e;
    calldataarg args;
    f@withrevert(e,args);
    assert lastReverted;
}

//// # Check that every op that exec-ed on an account has been checked via the validateUserOp function
/**
* Verified by keeping track of opcodes that have been verified and executed opcodes
*/

rule onlyValidatedCalls(method f, uint index)
filtered { f->
    f.selector != sig:EntryPoint.innerHandleOp(bytes,EntryPoint.UserOpInfo,bytes).selector
}
{
    env e;
    calldataarg args;
    numValidated = 0;
    numExecuted = 0;
    executionValidated = true;

    f(e,args);

    assert numValidated == numExecuted;
    assert executionValidated;
    satisfy numExecuted > 0;
}

rule innerHandleOpProtected()
{
    env e;
    bytes callData;
    EntryPoint.UserOpInfo opInfo;
    bytes context;
    require e.msg.sender != currentContract;

    innerHandleOp@withrevert(e, callData, opInfo, context);
    assert lastReverted;
}


//// # Validity of balance decrease
/**
 *  Who can decrease balance of (in StakeManager) ?
 */
rule onlySelfReduces(method f, address user) {
    env e;
    calldataarg args;
    uint256 before =  balanceOf(user);
    f(e, args);
    uint256 after =  balanceOf(user);
    assert after < before => e.msg.sender == user;
}

rule sanity(method f) {
    env e;
    calldataarg arg;
    f(e, arg);
    satisfy true;
}
