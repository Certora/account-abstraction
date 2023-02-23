
methods {

    validateUserOp(uint256, bytes32, uint256 ) => DISPATCHER(true)

}
rule sanity(method f) {
    env e;
    calldataarg args;
    f(e,args);
    assert false; 
}