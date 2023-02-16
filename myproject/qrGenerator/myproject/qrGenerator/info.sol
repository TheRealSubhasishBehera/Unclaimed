pragma solidity ^0.8.0;

contract LostItem {
    // Define a structure to store information about a lost item
    struct LostItemData {
        string itemName;
        string itemDescription;
        string itemLocation;
        address owner;
    }
    
    // Create a mapping to store lost item data
    mapping (string => LostItemData) public lostItems;
    
    // Function to add a lost item
    function addLostItem(string memory _itemId, string memory _itemName, string memory _itemDescription, string memory _itemLocation) public {
        lostItems[_itemId] = LostItemData(_itemName, _itemDescription, _itemLocation, msg.sender);
    }
    
    // Function to retrieve lost item data
    function getLostItem(string memory _itemId) public view returns (string memory, string memory, string memory, address) {
        LostItemData memory lostItem = lostItems[_itemId];
        return (lostItem.itemName, lostItem.itemDescription, lostItem.itemLocation, lostItem.owner);
    }
}
