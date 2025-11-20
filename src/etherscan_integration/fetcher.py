import requests
from typing import Any, List, Dict

# Etherscan V2 base URL
ETHERSCAN_API = "https://api.etherscan.io/v2/api"
CHAIN_ID = 1  # Ethereum mainnet


def _check_etherscan_response(data: Dict[str, Any], context: str) -> Any:
    """
    Validate Etherscan API V2 response and handle common cases.
    """
    status = data.get("status")
    message = data.get("message")
    result = data.get("result")

    # Success: status == "1" and result is a list
    if status == "1" and isinstance(result, list):
        return result

    # "No transactions found" or similar → treat as empty list
    if status == "0" and isinstance(result, str) and (
        "No transactions found" in result
        or "Contract source code not verified" in result
    ):
        print(f"[INFO] {context}: {result}")
        return []

    # V1 deprecation message (should not appear once we're on V2, but keep for safety)
    if status == "0" and isinstance(result, str) and "deprecated V1 endpoint" in result:
        raise RuntimeError(
            f"[ERROR] Etherscan still reports V1 deprecation in {context}. "
            f"Double-check URL construction."
        )

    # Free-tier throttling / other errors
    raise RuntimeError(
        f"Etherscan API error during {context}: status={status}, message={message}, result={result}"
    )


def get_contracts_by_deployer(address: str, api_key: str) -> List[Dict[str, Any]]:
    """
    Returns all contracts created by a given deployer address using Etherscan V2.
    We use the txlist action under module=account, same as V1, but with:
    - base URL: https://api.etherscan.io/v2/api
    - chainid parameter for network selection.
    """
    params = {
        "chainid": CHAIN_ID,
        "module": "account",
        "action": "txlist",
        "address": address,
        "sort": "asc",
        "apikey": api_key,
    }

    resp = requests.get(ETHERSCAN_API, params=params)
    resp.raise_for_status()
    data = resp.json()

    result = _check_etherscan_response(data, context="get_contracts_by_deployer")

    contracts: List[Dict[str, Any]] = []
    for tx in result:
        if isinstance(tx, dict) and tx.get("contractAddress"):
            contracts.append(tx)
    return contracts


def get_contract_source(contract_address: str, api_key: str) -> str:
    """
    Fetch contract source code using Etherscan V2.
    """
    params = {
        "chainid": CHAIN_ID,
        "module": "contract",
        "action": "getsourcecode",
        "address": contract_address,
        "apikey": api_key,
    }

    resp = requests.get(ETHERSCAN_API, params=params)
    resp.raise_for_status()
    data = resp.json()

    status = data.get("status")
    result = data.get("result")

    # V2 returns list with one dict on success
    if status == "1" and isinstance(result, list) and result:
        entry = result[0]
        src = entry.get("SourceCode") or ""
        return src if isinstance(src, str) else ""

    # Not verified / no source
    if status == "0":
        msg = result if isinstance(result, str) else ""
        print(f"[INFO] get_contract_source: {msg} for {contract_address}")
    return ""
