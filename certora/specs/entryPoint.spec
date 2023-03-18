using SymbolicAccount as account 

methods {

    validateUserOp(account.UserOperation,bytes32,uint256) => DISPATCHER(true)
    account.called() returns (bool) envfree;

    // 
    createSender(bytes initCode) returns (address) => NONDET 

    // Paymaster
   // validatePaymasterUserOp(account.UserOperation  userOp, bytes32 userOpHash, uint256 maxCost)=> NONDET

    validatePaymasterUserOp((address,uint256,bytes,bytes,uint256,uint256,uint256,uint256,uint256,bytes,bytes) userOp, bytes32 userOpHash, uint256 maxCost)=> NONDET

    balanceOf(address user) returns (uint256) envfree
 

    postOp(uint8 mode, bytes context, uint256 actualGasCost) => NONDET 

    account.validatedLength()  returns (uint256) envfree
    account.calledLength()  returns (uint256) envfree
    account.called_data(uint256 index) returns (bytes) envfree
    account.validated_data(uint256 index) returns (bytes) envfree
    account.eq(uint256 index) returns (bool) envfree
}

//// # Verifies that certain function always revert as expected */
rule alwaysRevert(method f) 
    filtered { f->
            f.selector == _validateSenderAndPaymaster(bytes,address,bytes).selector ||
            f.selector == getSenderAddress(bytes).selector ||
            f.selector == simulateValidation((address,uint256,bytes,bytes,uint256,uint256,uint256,uint256,uint256,bytes,bytes)).selector }

    {
        env e;
        calldataarg args;
        f(e,args);
        assert lastReverted; 
}


//// # Check that every op that exec-ed on an account has been checked via the validateUserOp function 
/**
* Verified by keeping track of opcodes that have been verified and executed opcodes
*/

rule onyValidatedCalls(method f, uint index) {
    env e;
    calldataarg args;
    require account.validatedLength() == 0;
    require account.calledLength() == 0;
     
    f(e,args);

    assert account.validatedLength() == account.calledLength();
    assert index < account.validatedLength() => account.eq(index);
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
    assert (after < before => e.msg.sender == user);
}