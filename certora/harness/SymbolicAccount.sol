pragma solidity ^0.8.12;


import "../../contracts/interfaces/IAccount.sol";
import "../../contracts/core/Helpers.sol";
/**
 * Symbolic account for verifying that evey executed call has been verified 
 */
contract SymbolicAccount  {

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
        validationData = _packValidationData(validationReturnValue[encode].aggregator, 
                                                    validationReturnValue[encode].validAfter,
                                                    validationReturnValue[encode].validUntil);

    }


    // writing as a fallback function requires assembly, which will take some time for
    // me to learn writing. 
    // let's start with a simple implementation as `execute`

    function execute(address target, uint256 value, bytes calldata data) external {
        // _requireFromEntryPointOrOwner();
        calldatas[count] = data;
        count++;
    }

    //todo - in fallback mark which userOp has been called
    /*
    execute(userOp) {
            called[i] = userOp 
            i++
    }
    */
}

