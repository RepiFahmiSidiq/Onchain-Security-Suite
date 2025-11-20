// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title DeployerReputationRegistry
/// @notice Stores off-chain reputation scores for deployer addresses.
contract DeployerReputationRegistry {
    enum RiskClass { Unknown, Low, Medium, High }

    struct Reputation {
        uint256 score;       // 0-100
        RiskClass riskClass;
        string label;        // trusted, watchlist, high_risk
        uint256 numContracts;
        uint256 lastUpdated;
        address updater;
    }

    mapping(address => Reputation) public reputations;

    event ReputationUpdated(
        address indexed deployer,
        uint256 score,
        RiskClass riskClass,
        string label,
        uint256 numContracts,
        address indexed updater
    );

    function updateReputation(
        address deployer,
        uint256 score,
        RiskClass riskClass,
        string calldata label,
        uint256 numContracts
    ) external {
        require(score <= 100, "score out of range");

        reputations[deployer] = Reputation({
            score: score,
            riskClass: riskClass,
            label: label,
            numContracts: numContracts,
            lastUpdated: block.timestamp,
            updater: msg.sender
        });

        emit ReputationUpdated(deployer, score, riskClass, label, numContracts, msg.sender);
    }

    function getReputation(address deployer)
        external
        view
        returns (Reputation memory)
    {
        return reputations[deployer];
    }
}
