pragma solidity ^0.8.12;


import "../../contracts/interfaces/IAccount.sol";
import "../../contracts/core/Helpers.sol";
/**
 * Symbolic account for verifying that evey executed call has been verified 
 */
contract SymbolicAccount  {
    bytes[] public message_data;
    bool public called; 

    // unconstraint values - can be any value
    mapping(bytes32 => ValidationData) public validationReturnValue;
    
    uint count;
    mapping(uint => bytes) public calldatas;


    constructor() {
        count = 0;
    }

    function validateUserOp(UserOperation calldata userOp, bytes32 userOpHash, uint256 missingAccountFunds)
    external  returns (uint256 validationData)
    {
        bytes32 encode = keccak256(abi.encodePacked(userOp.sender, userOp.nonce, userOp.callData));
        validationData = _packValidationData(validationReturnValue[encode]);

    }

    fallback() external payable  {
        called = true;
        message_data.push(msg.data);
    }
}

