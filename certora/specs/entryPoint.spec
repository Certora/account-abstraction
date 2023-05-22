using SymbolicAccount as account;

methods {

    function _.validateUserOp(EntryPoint.UserOperation,bytes32,uint256) external => DISPATCHER(true);
    //function SymbolicAccount.called() external returns (bool) envfree;

    // 
    function _.createSender(bytes initCode) external => NONDET;

    // Paymaster
   // validatePaymasterUserOp(EntryPoint.UserOperation  userOp, bytes32 userOpHash, uint256 maxCost)=> NONDET

    function _.validatePaymasterUserOp(EntryPoint.UserOperation userOp, bytes32 userOpHash, uint256 maxCost) external => NONDET;

    function balanceOf(address) external returns (uint256) envfree;
    function _compensate(address beneficiary, uint256 amount) internal  => NONDET;

    function _.postOp(uint8 mode, bytes context, uint256 actualGasCost) external => NONDET;

    function SymbolicAccount.validatedLength()  external returns (uint256) envfree;
    function SymbolicAccount.calledLength()  external returns (uint256) envfree;
    function SymbolicAccount.called_data(uint256 index) external returns (bytes) envfree;
    function SymbolicAccount.validated_data(uint256 index) external returns (bytes) envfree;
    function SymbolicAccount.eq(uint256 index) external returns (bool) envfree;
}

//// # Verifies that certain function always revert as expected */
rule alwaysRevert(method f) 
    filtered { f->
            f.selector == sig:_validateSenderAndPaymaster(bytes,address,bytes).selector ||
            f.selector == sig:getSenderAddress(bytes).selector ||
            f.selector == sig:simulateValidation(EntryPoint.UserOperation).selector }

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
    //  filtered { f->
    //         //f.selector == sig:handleAggregatedOps(EntryPoint.UserOpsPerAggregator(EntryPoint.UserOperation(address,uint256,bytes,bytes,uint256,uint256,uint256,uint256,uint256,bytes,bytes)[],address,bytes)[],address).selector
    //         //f.selector == sig:handleAggregatedOps(EntryPoint.UserOpsPerAggregator[],address).selector
    //         //f.selector == sig:handleOps(EntryPoint.UserOperation[],address).selector
    //          }
{
    env e;
    calldataarg args;
    require account.validatedLength() == 0;
    require account.calledLength() == 0;
     
    f(e,args);

    assert account.calledLength() > 0  => account.validatedLength() > 0;
    //assert index < account.validatedLength() => account.eq(index);
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
    assert false;
}