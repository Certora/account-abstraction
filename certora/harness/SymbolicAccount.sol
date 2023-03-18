pragma solidity ^0.8.12;


import "../../contracts/interfaces/IAccount.sol";
import "../../contracts/core/Helpers.sol";
/**
 * Symbolic account for verifying that evey executed call has been verified 
 */
contract SymbolicAccount  {
    
    
    bytes[] public called_data;
    bytes[] public validated_data;


    // unconstraint values - can be any value
    mapping(bytes32 => ValidationData) public validationReturnValue;



    constructor() {
    }

    function validatedLength() view external returns (uint256) {
        return validated_data.length ;
    }

    function calledLength() view external returns (uint256) {
        return called_data.length ;
    }

       

    function validateUserOp(UserOperation calldata userOp, bytes32 userOpHash, uint256 missingAccountFunds)
    external  returns (uint256 validationData)
    {
        bytes32 encode = keccak256(abi.encodePacked(userOp.sender, userOp.nonce, userOp.callData));
        validationData = _packValidationData(validationReturnValue[encode]);
        
        validated_data.push(userOp.callData);

    }


    function execCall(
        address to,
        uint256 value,
        bytes memory data,
        uint256 txGas) 
    external returns (bool) 
    {
        called_data.push(msg.data);
        return true;

    }

    function eq(uint256 index) external returns (bool) {
        if ( index >= called_data.length || index >= validated_data.length )
            return false;
        if (called_data[index].length != validated_data[index].length)
            return false;
        for(uint256 i ; i < called_data[index].length ; i++) {
            if ( called_data[index][i] != validated_data[index][i] )
                return false; 
        }
        return true;
    }


    fallback() external payable  {
      called_data.push(msg.data);
      return;
    }

    
}

