using SymbolicAccount as account 

methods {

    validateUserOp(account.UserOperation,bytes32,uint256) => DISPATCHER(true)
    account.called() returns (bool) envfree;

    // 
    createSender(bytes initCode) returns (address) => NONDET 

    // Paymaster
     validatePaymasterUserOp(account.UserOperation  userOp, bytes32 userOpHash, uint256 maxCost)=> NONDET

    postOp(uint8 mode, bytes  context, uint256 actualGasCost) => NONDET 

    testMsgData(uint x) returns (uint8)
}
rule sanity(method f) {
    env e;
    calldataarg args;
    f(e,args);
    assert false; 
}

rule fallbackCalled(method f) {
    env e;
    calldataarg args;
    require !account.called();
    f(e,args);
    assert !account.called();
}



rule verifyMsgData(uint8 x) {
    env e;
    
    uint8 res = testMsgData(e, 200);
    assert res == 200;

}