pragma solidity ^0.8.0;

contract AccessLog {
    struct LogEntry {
        uint256 timestamp;
        string user;
        bool granted;
    }

    LogEntry[] public logs;

    function logAccess(string memory user, bool granted) public {
        logs.push(LogEntry(block.timestamp, user, granted));
    }
}
