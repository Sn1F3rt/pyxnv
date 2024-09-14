from typing import Optional

import aiohttp


__all__ = ["Wallet"]


class Wallet:
    """
    A class to interact with the Nerva wallet's JSON-RPC interface.

    Parameters
    ----------
    port : int
        The port of the wallet's JSON-RPC interface.
    host : str, optional
        The host of the wallet's JSON-RPC interface. Default is "localhost".
    ssl : bool, optional
        Whether to use SSL. Default is False.
    timeout : float, optional
        The timeout for the request. Default is 10.0.
    username : str, optional
        The username for the wallet's JSON-RPC interface. Default is "".
    password : str, optional
        The password for the wallet's JSON-RPC interface. Default is "".

    Attributes
    ----------
    url : str
        The URL of the wallet's JSON-RPC interface.
    auth : aiohttp.BasicAuth
        The authentication for the wallet's JSON-RPC interface.
    timeout : float
        The timeout for the request.
    endpoint : str
        The endpoint for the JSON-RPC interface.
    headers : dict
        The headers for the request

    """

    __slots__ = [
        "url",
        "auth",
        "timeout",
        "endpoint",
        "headers",
    ]

    def __init__(
        self,
        port: int,
        host: str = "localhost",
        ssl: bool = False,
        timeout: float = 10.0,
        username: str = "",
        password: str = "",
    ):
        self.url = f"http{'s' if ssl else ''}://{host}:{port}"
        self.auth = (
            aiohttp.BasicAuth(username, password) if username and password else None
        )
        self.timeout = timeout

        self.endpoint = "/json_rpc"
        self.headers = {"Content-Type": "application/json"}

    async def _request(self, method: str, params: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}/{self.endpoint}",
                json={"jsonrpc": "2.0", "id": 0, "method": method, "params": params},
                headers=self.headers,
                auth=self.auth,
                timeout=self.timeout,
            ) as response:
                return await response.json(content_type=None)

    async def get_balance(
        self, account_index: int, address_indices: Optional[list[int]] = None
    ) -> dict:
        """
        Return the wallet's balance.

        Parameters
        ----------
        account_index : int
            Return balance for this account.
        address_indices : list[int], optional
            Return balance detail for those subaddresses.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "get_balance",
            {
                "account_index": account_index,
                "address_indices": address_indices or [],
            },
        )

    async def get_address(
        self, account_index: int, address_indices: Optional[list[int]] = None
    ) -> dict:
        """
        Return the wallet's addresses for an account. Optionally filter for specific set of subaddresses.

        Parameters
        ----------
        account_index : int
            Get addresses for this account.
        address_indices : list[int], optional
            Return specific set of subaddresses.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "get_address",
            {
                "account_index": account_index,
                "address_indices": address_indices or [],
            },
        )

    async def get_address_index(self, address: str) -> dict:
        """
        Get account and address indexes from a specific (sub)address.

        Parameters
        ----------
        address : str
            The (sub)address to look for.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_address_index", {"address": address})

    async def create_address(
        self, account_index: int, label: Optional[str] = None
    ) -> dict:
        """
        Create a new address for an account.

        Parameters
        ----------
        account_index : int
            Create a new address for this account.
        label : str, optional
            Label for the new address.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "create_address", {"account_index": account_index, "label": label}
        )

    async def label_address(self, index: dict, label: str) -> dict:
        """
        Label an address.

        Parameters
        ----------
        index : dict
            Subaddress index in the form {"major": 0, "minor": 0}.
        label : str
            The label of the address.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("label_address", {"index": index, "label": label})

    async def get_accounts(self, tag: Optional[str] = None) -> dict:
        """
        Return the wallet's accounts.

        Parameters
        ----------
        tag : str, optional
            Tag for filtering accounts.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_accounts", {"tag": tag})

    async def create_account(self, label: Optional[str] = None) -> dict:
        """
        Create a new account.

        Parameters
        ----------
        label : str, optional
            The label of the account.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("create_account", {"label": label})

    async def label_account(self, account_index: int, label: str) -> dict:
        """
        Label an account.

        Parameters
        ----------
        account_index : int
            The index of the account.
        label : str
            The label of the account.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "label_account", {"account_index": account_index, "label": label}
        )

    async def get_account_tags(self) -> dict:
        """
        Return the wallet's account tags.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_account_tags", {})

    async def tag_accounts(self, tag: str, accounts: list) -> dict:
        """
        Apply a filtering tag to a list of accounts.

        Parameters
        ----------
        tag : str
            The tag to apply.
        accounts : list
            The accounts to tag.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "tag_accounts", {"tag": tag, "accounts": accounts}
        )

    async def untag_accounts(self, accounts: list) -> dict:
        """
        Remove filtering tag from a list of accounts.

        Parameters
        ----------
        accounts : list
            The accounts to untag.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("untag_accounts", {"accounts": accounts})

    async def set_account_tag_description(self, tag: str, description: str) -> dict:
        return await self._request(
            "set_account_tag_description", {"tag": tag, "description": description}
        )

    async def get_height(self) -> dict:
        """
        Return the wallet's current block height.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_height", {})

    async def transfer(
        self,
        destinations: list,
        account_index: int,
        subaddr_indices: list,
        priority: int,
        mixin: int,
        ring_size: int,
        unlock_time: int,
        get_tx_key: bool,
        get_tx_hex: bool,
        get_tx_metadata: bool,
        do_not_relay: bool,
        payment_id: Optional[str] = None,
    ) -> dict:
        """
        Send a transfer from the wallet to a single recipient.

        Parameters
        ----------
        destinations : list
            The destinations to send the transfer to.
        account_index : int
            The account to send the transfer from.
        subaddr_indices : list
            Array of subaddress indices to send from.
        priority : int
            Set a priority for the transfer.
        mixin : int
            Number of outputs from the blockchain to mix with (0 means no mixing).
        ring_size : int
            Sets ringsize for each transaction.
        unlock_time : int
            Number of blocks before the Nerva can be spent (0 to not add a lock).
        get_tx_key : bool
            Return the transaction key after sending.
        get_tx_hex : bool
            Return the transaction as hex string after sending.
        get_tx_metadata : bool
            Return the transaction metadata.
        do_not_relay : bool
            If true, the transfer won't be relayed to the Nerva network.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "transfer",
            {
                "destinations": destinations,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices,
                "priority": priority,
                "mixin": mixin,
                "ring_size": ring_size,
                "unlock_time": unlock_time,
                "get_tx_key": get_tx_key,
                "get_tx_hex": get_tx_hex,
                "get_tx_metadata": get_tx_metadata,
                "do_not_relay": do_not_relay,
                "payment_id": payment_id,
            },
        )

    async def transfer_split(
        self,
        destinations: list,
        account_index: int,
        subaddr_indices: list,
        priority: int,
        mixin: int,
        ring_size: int,
        unlock_time: int,
        get_tx_keys: bool,
        get_tx_hex: bool,
        get_tx_metadata: bool,
        do_not_relay: bool,
        payment_id: Optional[str] = None,
    ) -> dict:
        """
        Send a transfer from the wallet to multiple recipients.

        Parameters
        ----------
        destinations : list
            The destinations to send the transfer to.
        account_index : int
            The account to send the transfer from.
        subaddr_indices : list
            Array of subaddress indices to send from.
        priority : int
            Set a priority for the transfer.
        mixin : int
            Number of outputs from the blockchain to mix with (0 means no mixing).
        ring_size : int
            Sets ringsize for each transaction.
        unlock_time : int
            Number of blocks before the Nerva can be spent (0 to not add a lock).
        get_tx_keys : bool
            Return the transaction keys after sending.
        get_tx_hex : bool
            Return the transaction as hex string after sending.
        get_tx_metadata : bool
            Return the transaction metadata.
        do_not_relay : bool
            If true, the transfer won't be relayed to the Nerva network.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "transfer_split",
            {
                "destinations": destinations,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices,
                "priority": priority,
                "mixin": mixin,
                "ring_size": ring_size,
                "unlock_time": unlock_time,
                "get_tx_keys": get_tx_keys,
                "get_tx_hex": get_tx_hex,
                "get_tx_metadata": get_tx_metadata,
                "do_not_relay": do_not_relay,
                "payment_id": payment_id,
            },
        )

    async def sign_transfer(
        self, unsigned_txset: str, export_raw: Optional[bool] = False
    ) -> dict:
        """
        Sign a transaction created on a read-only wallet (in cold-signing process).

        Parameters
        ----------
        unsigned_txset : str
            Set of unsigned tx returned by "transfer" method.
        export_raw : bool, optional
            If true, return the raw transaction data. Default is False.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "sign_transfer",
            {"unsigned_txset": unsigned_txset, "export_raw": export_raw},
        )

    async def describe_transfer(self, unsigned_txset: str) -> dict:
        """
        Return a list of unsigned transfers in the set, their count, and total amount.

        Parameters
        ----------
        unsigned_txset : str
            Set of unsigned tx returned by "transfer" method.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "describe_transfer", {"unsigned_txset": unsigned_txset}
        )

    async def submit_transfer(self, tx_data_hex: str) -> dict:
        """
        Submit a previously signed transaction.

        Parameters
        ----------
        tx_data_hex : str
            Transaction in hex format.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("submit_transfer", {"tx_data_hex": tx_data_hex})

    async def sweep_dust(
        self,
        get_tx_keys: Optional[bool] = False,
        do_not_relay: Optional[str] = False,
        get_tx_hex: Optional[bool] = False,
        get_tx_metadata: Optional[bool] = False,
    ) -> dict:
        """
        Sweep the dust from the wallet.

        Parameters
        ----------
        get_tx_keys : bool, optional
            Return the transaction keys after sending.
        do_not_relay : bool, optional
            If true, do not relay this sweep transfer.
        get_tx_hex : bool, optional
            Return the transactions as hex string after sending.
        get_tx_metadata : bool, optional
            Return the transaction metadata.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "sweep_dust",
            {
                "get_tx_keys": get_tx_keys,
                "do_not_relay": do_not_relay,
                "get_tx_hex": get_tx_hex,
                "get_tx_metadata": get_tx_metadata,
            },
        )

    async def sweep_unmixable(self) -> dict:
        """
        Sweep unmixable outputs from the wallet.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("sweep_unmixable", {})

    async def sweep_all(
        self,
        address: str,
        account_index: int,
        subaddr_indices: list,
        priority: int,
        mixin: int,
        ring_size: int,
        unlock_time: int,
        get_tx_keys: bool,
        below_amount: int,
        do_not_relay: bool,
        get_tx_hex: bool,
        get_tx_metadata: bool,
        payment_id: Optional[str] = None,
    ) -> dict:
        """
        Sweep all unlocked outputs in a specified subaddress to an address.

        Parameters
        ----------
        address : str
            Destination public address.
        account_index : int
            Account to sweep from.
        subaddr_indices : list
            Array of subaddress indices to sweep from.
        priority : int
            Set a priority for the transfer.
        mixin : int
            Number of outputs from the blockchain to mix with (0 means no mixing).
        ring_size : int
            Sets ringsize for each transaction.
        unlock_time : int
            Number of blocks before the Nerva can be spent (0 to not add a lock).
        get_tx_keys : bool
            Return the transaction keys after sending.
        below_amount : int
            Sweep all outputs below this amount.
        do_not_relay : bool
            If true, do not relay this sweep transfer.
        get_tx_hex : bool
            Return the transactions as hex string after sending.
        get_tx_metadata : bool
            Return the transaction metadata.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "sweep_all",
            {
                "address": address,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices,
                "priority": priority,
                "mixin": mixin,
                "ring_size": ring_size,
                "unlock_time": unlock_time,
                "get_tx_keys": get_tx_keys,
                "below_amount": below_amount,
                "do_not_relay": do_not_relay,
                "get_tx_hex": get_tx_hex,
                "get_tx_metadata": get_tx_metadata,
                "payment_id": payment_id,
            },
        )

    async def sweep_single(
        self,
        address: str,
        priority: int,
        mixin: int,
        ring_size: int,
        unlock_time: int,
        get_tx_key: bool,
        get_tx_hex: bool,
        get_tx_metadata: bool,
        do_not_relay: bool,
        payment_id: Optional[str] = None,
    ) -> dict:
        """
        Sweep a single output to an address.

        Parameters
        ----------
        address : str
            Destination public address.
        priority : int
            Set a priority for the transfer.
        mixin : int
            Number of outputs from the blockchain to mix with (0 means no mixing).
        ring_size : int
            Sets ringsize for each transaction.
        unlock_time : int
            Number of blocks before the Nerva can be spent (0 to not add a lock).
        get_tx_key : bool
            Return the transaction keys after sending.
        get_tx_hex : bool
            Return the transaction as hex string after sending.
        get_tx_metadata : bool
            Return the transaction metadata.
        do_not_relay : bool
            If true, the transfer won't be relayed to the Nerva network.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "sweep_single",
            {
                "address": address,
                "priority": priority,
                "mixin": mixin,
                "ring_size": ring_size,
                "unlock_time": unlock_time,
                "get_tx_key": get_tx_key,
                "get_tx_hex": get_tx_hex,
                "get_tx_metadata": get_tx_metadata,
                "do_not_relay": do_not_relay,
                "payment_id": payment_id,
            },
        )

    async def relay_tx(self, tx_hex: str) -> dict:
        """
        Relay a transaction previously created with "do_not_relay" set to true.

        Parameters
        ----------
        tx_hex : str
            Transaction in hex format.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("relay_tx", {"hex": tx_hex})

    async def store(self) -> dict:
        """
        Save the wallet file.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("store", {})

    async def get_payments(self, payment_id: str) -> dict:
        """
        Return a list of incoming payments using a given payment ID.

        Parameters
        ----------
        payment_id : str
            Payment ID to query.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_payments", {"payment_id": payment_id})

    async def get_bulk_payments(
        self, payment_ids: list, min_block_height: int
    ) -> dict:
        """
        Return a list of incoming payments using a given payment ID.

        Parameters
        ----------
        payment_ids : list
            Payment IDs to query.
        min_block_height : int
            The minimum block height to scan.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "get_bulk_payments",
            {"payment_ids": payment_ids, "min_block_height": min_block_height},
        )

    async def incoming_transfers(
        self,
        transfer_type: str,
        account_index: int,
        subaddr_indices: list,
        verbose: Optional[bool] = False,
    ) -> dict:
        """
        Return a list of incoming transfers to the wallet.

        Parameters
        ----------
        transfer_type : str
            "all": all the transfers.
            "available": only transfers which are not yet spent.
            "unavailable": only transfers which are already spent.
        account_index : int
            Return transfers for this account.
        subaddr_indices : list
            Array of subaddress indices to query.
        verbose : bool, optional
            Enable verbose output.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "incoming_transfers",
            {
                "transfer_type": transfer_type,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices,
                "verbose": verbose,
            },
        )

    async def query_key(self, key_type: str) -> dict:
        """
        Return the spend or view private key.

        Parameters
        ----------
        key_type : str
            "mnemonic": the mnemonic seed.
            "view_key": the view key.
            "spend_key": the spend key.
            "seed": the mnemonic seed.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("query_key", {"key_type": key_type})

    async def make_integrated_address(
        self, payment_id: str, standard_address: Optional[str] = None
    ) -> dict:
        """
        Make an integrated address from the wallet address and a payment ID.

        Parameters
        ----------
        payment_id : str
            Payment ID.
        standard_address : str, optional
            Destination public address. If not provided, the wallet's address is used.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "make_integrated_address",
            {"payment_id": payment_id, "standard_address": standard_address},
        )

    async def split_integrated_address(self, integrated_address: str) -> dict:
        """
        Retrieve the standard address and payment ID corresponding to an integrated address.

        Parameters
        ----------
        integrated_address : str
            Integrated address to split.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "split_integrated_address", {"integrated_address": integrated_address}
        )

    async def stop_wallet(self) -> dict:
        """
        Stop the wallet.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("stop_wallet", {})

    async def rescan_blockchain(self) -> dict:
        """
        Re-scan the blockchain.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("rescan_blockchain", {})

    async def set_tx_notes(self, txids: list[str], notes: list[str]) -> dict:
        """
        Set arbitrary string notes for transactions.

        Parameters
        ----------
        txids : list[str]
            Array of transaction IDs.
        notes : list[str]
            Notes for the transactions.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("set_tx_notes", {"txids": txids, "notes": notes})

    async def get_tx_notes(self, txids: list[str]) -> dict:
        """
        Get string notes for transactions.

        Parameters
        ----------
        txids : list[str]
            Array of transaction IDs.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_tx_notes", {"txids": txids})

    async def set_attribute(self, key: str, value: str) -> dict:
        """
        Set arbitrary attribute.

        Parameters
        ----------
        key : str
            Attribute name.
        value : str
            Attribute value.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("set_attribute", {"key": key, "value": value})

    async def get_attribute(self, key: str) -> dict:
        """
        Get an attribute.

        Parameters
        ----------
        key : str
            Attribute name.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_attribute", {"key": key})

    async def get_tx_key(self, txid: str) -> dict:
        """
        Get transaction secret key.

        Parameters
        ----------
        txid : str
            Transaction ID.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_tx_key", {"txid": txid})

    async def check_tx_key(self, txid: str, tx_key: str, address: str) -> dict:
        """
        Check a transaction in the blockchain with its secret key.

        Parameters
        ----------
        txid : str
            Transaction ID.
        tx_key : str
            Transaction secret key.
        address : str
            Destination public address.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "check_tx_key", {"txid": txid, "tx_key": tx_key, "address": address}
        )

    async def get_tx_proof(
        self, txid: str, address: str, message: Optional[str] = None
    ) -> dict:
        """
        Generate a signature to prove a transaction in the blockchain.

        Parameters
        ----------
        txid : str
            Transaction ID.
        address : str
            Destination public address.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "get_tx_proof", {"txid": txid, "address": address, "message": message}
        )

    async def check_tx_proof(
        self, txid: str, address: str, signature: str, message: Optional[str] = None
    ) -> dict:
        """
        Prove a transaction by checking its signature.

        Parameters
        ----------
        txid : str
            Transaction ID.
        address : str
            Destination public address.
        signature : str
            Transaction signature.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "check_tx_proof",
            {
                "txid": txid,
                "address": address,
                "signature": signature,
                "message": message,
            },
        )

    async def get_spend_proof(
        self, txid: str, message: Optional[str] = None
    ) -> dict:
        """
        Generate a signature to prove a spend using the key of the transaction.

        Parameters
        ----------
        txid : str
            Transaction ID.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "get_spend_proof", {"txid": txid, "message": message}
        )

    async def check_spend_proof(
        self, txid: str, signature: str, message: Optional[str] = None
    ) -> dict:
        """
        Prove a spend using the key of the transaction.

        Parameters
        ----------
        txid : str
            Transaction ID.
        signature : str
            Spend signature.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "check_spend_proof",
            {"txid": txid, "message": message, "signature": signature},
        )

    async def get_reserve_proof(
        self,
        all_reserve: bool,
        account_index: int,
        amount: int,
        message: Optional[str] = None,
    ) -> dict:
        """
        Generate a signature to prove of a reserve proof.

        Parameters
        ----------
        all_reserve : bool
            Proves all wallet reserve.
        account_index : int
            Account to prove reserve for.
        amount : int
            Amount to prove.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "get_reserve_proof",
            {
                "all": all_reserve,
                "account_index": account_index,
                "amount": amount,
                "message": message,
            },
        )

    async def check_reserve_proof(
        self, address: str, signature: str, message: Optional[str] = None
    ) -> dict:
        """
        Prove a wallet has a disposable reserve using a signature.

        Parameters
        ----------
        address : str
            Public address.
        signature : str
            Reserve proof signature.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "check_reserve_proof",
            {"address": address, "message": message, "signature": signature},
        )

    async def get_transfers(
        self,
        incoming: Optional[bool] = False,
        outgoing: Optional[bool] = False,
        pending: Optional[bool] = False,
        failed: Optional[bool] = False,
        pool: Optional[bool] = False,
        filter_by_height: Optional[bool] = False,
        min_height: Optional[int] = None,
        max_height: Optional[int] = None,
        account_index: Optional[int] = None,
        subaddr_indices: Optional[list[int]] = None,
    ) -> dict:
        """
        Return a list of transfers.

        Parameters
        ----------
        incoming : bool, optional
            Include incoming transfers.
        outgoing : bool, optional
            Include outgoing transfers.
        pending : bool, optional
            Include pending transfers.
        failed : bool, optional
            Include failed transfers.
        pool : bool, optional
            Include transfers from the daemon's transaction pool.
        filter_by_height : bool, optional
            Filter transfers by block height.
        min_height : int, optional
            Minimum block height to scan for transfers.
        max_height : int, optional
            Maximum block height to scan for transfers.
        account_index : int, optional
            Return transfers for this account.
        subaddr_indices : list[int], optional
            Array of subaddress indices to query.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "get_transfers",
            {
                "in": incoming,
                "out": outgoing,
                "pending": pending,
                "failed": failed,
                "pool": pool,
                "filter_by_height": filter_by_height,
                "min_height": min_height,
                "max_height": max_height,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices or [],
            },
        )

    async def get_transfer_by_txid(
        self, txid: str, account_index: Optional[int] = None
    ) -> dict:
        """
        Return a list of transfers for the given txid.

        Parameters
        ----------
        txid : str
            Transaction ID.
        account_index : int, optional
            Return transfers for this account.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "get_transfer_by_txid", {"txid": txid, "account_index": account_index}
        )

    async def sign(self, data: str) -> dict:
        """
        Sign a string.

        Parameters
        ----------
        data : str
            Data to sign.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("sign", {"data": data})

    async def verify(self, data: str, address: str, signature: str) -> dict:
        """
        Verify a signature on a string.

        Parameters
        ----------
        data : str
            Data to verify.
        address : str
            Public address.
        signature : str
            Signature to verify.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "verify", {"data": data, "address": address, "signature": signature}
        )

    async def export_outputs(self) -> dict:
        """
        Export all outputs in hex format.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("export_outputs", {})

    async def import_outputs(self, outputs_data_hex: str) -> dict:
        """
        Import outputs in hex format.

        Parameters
        ----------
        outputs_data_hex : str
            Outputs to import in hex format.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "import_outputs", {"outputs_data_hex": outputs_data_hex}
        )

    async def export_key_images(self) -> dict:
        """
        Export a signed set of key images.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("export_key_images", {})

    async def import_key_images(
        self, signed_key_images: list[str], key_image: str, signature: str
    ) -> dict:
        """
        Import signed key images list and verify their spent status.

        Parameters
        ----------
        signed_key_images : list[str]
            Array of signed key images in hex format.
        key_image : str
            Key image to import.
        signature : str
            Signature of the key image.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "import_key_images",
            {
                "signed_key_images": signed_key_images,
                "key_image": key_image,
                "signature": signature,
            },
        )

    async def make_uri(
        self,
        address: str,
        amount: Optional[int] = None,
        payment_id: Optional[str] = None,
        recipient_name: Optional[str] = None,
        tx_description: Optional[str] = None,
    ) -> dict:
        """
        Create a payment URI using the official URI spec.

        Parameters
        ----------
        address : str
            Destination public address.
        amount : int, optional
            Amount to send.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.
        recipient_name : str, optional
            Name of the payment recipient.
        tx_description : str, optional
            Description of the reason for the tx.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "make_uri",
            {
                "address": address,
                "amount": amount,
                "payment_id": payment_id,
                "recipient_name": recipient_name,
                "tx_description": tx_description,
            },
        )

    async def parse_uri(self, uri: str) -> dict:
        """
        Parse a payment URI to get payment information.

        Parameters
        ----------
        uri : str
            Payment URI.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("parse_uri", {"uri": uri})

    async def get_address_book(self, entries: list[int]) -> dict:
        """
        Return the wallet's address book.

        Parameters
        ----------
        entries : list[int]
            Array of address book entries.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_address_book", {"entries": entries})

    async def add_address_book(
        self,
        address: str,
        payment_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> dict:
        """
        Add an entry to the wallet's address book.

        Parameters
        ----------
        address : str
            Destination public address.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.
        description : str, optional
            Description of the address.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "add_address_book",
            {
                "address": address,
                "payment_id": payment_id,
                "description": description,
            },
        )

    async def edit_address_book(
        self,
        index: int,
        set_address: Optional[bool] = False,
        address: Optional[str] = None,
        set_description: Optional[bool] = False,
        description: Optional[str] = None,
        set_payment_id: Optional[bool] = False,
        payment_id: Optional[str] = None,
    ) -> dict:
        """
        Edit an existing entry in the wallet's address book.

        Parameters
        ----------
        index : int
            The index of the address book entry to edit.
        set_address : bool, optional
            Set the address.
        address : str, optional
            Destination public address.
        set_description : bool, optional
            Set the description.
        description : str, optional
            Description of the address.
        set_payment_id : bool, optional
            Set the payment ID.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "edit_address_book",
            {
                "index": index,
                "set_address": set_address,
                "address": address,
                "set_description": set_description,
                "description": description,
                "set_payment_id": set_payment_id,
                "payment_id": payment_id,
            },
        )

    async def delete_address_book(self, index: int) -> dict:
        """
        Delete an entry from the wallet's address book.

        Parameters
        ----------
        index : int
            The index of the address book entry to delete.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("delete_address_book", {"index": index})

    async def refresh(self, start_height: Optional[int] = None) -> dict:
        """
        Refresh the wallet.

        Parameters
        ----------
        start_height : int, optional
            Start height to refresh from.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("refresh", {"start_height": start_height})

    async def auto_refresh(
        self, enable: Optional[bool] = True, period: Optional[int] = None
    ) -> dict:
        """
        Set whether to automatically refresh the wallet.

        Parameters
        ----------
        enable : bool
            Enable or disable auto refresh.
        period : int, optional
            Set the refresh period.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "auto_refresh", {"enable": enable, "period": period}
        )

    async def rescan_spent(self) -> dict:
        """
        Re-scan spent outputs.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("rescan_spent", {})

    async def start_mining(
        self, threads_count: int, do_background_mining: bool, ignore_battery: bool
    ) -> dict:
        """
        Start mining in the wallet.

        Parameters
        ----------
        threads_count : int
            Number of threads to use for mining.
        do_background_mining : bool
            If true, mine in the background.
        ignore_battery : bool
            If true, mine even if battery is low.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "start_mining",
            {
                "threads_count": threads_count,
                "do_background_mining": do_background_mining,
                "ignore_battery": ignore_battery,
            },
        )

    async def set_donate_level(self, donate: int) -> dict:
        """
        Set the donation level for the Nerva network.

        Parameters
        ----------
        donate : int
            The donation level.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("set_donate_level", {"donate": donate})

    async def stop_mining(self) -> dict:
        """
        Stop mining in the wallet.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("stop_mining", {})

    async def get_languages(self) -> dict:
        """
        Return the list of available languages for the wallet's seed.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_languages", {})

    async def create_wallet(
        self,
        filename: str,
        language: str,
        password: Optional[str] = None,
    ) -> dict:
        """
        Create a new wallet.

        Parameters
        ----------
        filename : str
            Wallet file name.
        language : str
            Language for seed.
        password : str, optional
            Wallet password.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "create_wallet",
            {
                "filename": filename,
                "password": password or "",
                "language": language,
            },
        )

    async def create_hw_wallet(
        self, filename: str, language: str, device_name: str, restore_height: int
    ) -> dict:
        """
        Create a wallet from a hardware device.

        Parameters
        ----------
        filename : str
            Wallet file name.
        language : str
            Wallet language.
        device_name : str
            Hardware device name.
        restore_height : int
            Wallet restore height.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "create_hw_wallet",
            {
                "filename": filename,
                "language": language,
                "device_name": device_name,
                "restore_height": restore_height,
            },
        )

    async def open_wallet(
        self, filename: str, password: Optional[str] = None
    ) -> dict:
        """
        Open a wallet.

        Parameters
        ----------
        filename : str
            Wallet file name.
        password : str, optional
            Wallet password.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "open_wallet", {"filename": filename, "password": password or ""}
        )

    async def close_wallet(self) -> dict:
        """
        Close the wallet.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("close_wallet", {})

    async def change_wallet_password(
        self, old_password: Optional[str] = None, new_password: Optional[str] = None
    ) -> dict:
        """
        Change the wallet password.

        Parameters
        ----------
        old_password : str, optional
            Old wallet password.
        new_password : str, optional
            New wallet password.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "change_wallet_password",
            {"old_password": old_password or "", "new_password": new_password or ""},
        )

    async def restore_wallet_from_seed(
        self, filename: str, seed: str, restore_height: int
    ) -> dict:
        """
        Restore a wallet from a mnemonic seed.

        Parameters
        ----------
        filename : str
            Wallet file name.
        seed : str
            Wallet mnemonic seed.
        restore_height : int
            Wallet restore height.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "restore_wallet_from_seed",
            {"filename": filename, "seed": seed, "restore_height": restore_height},
        )

    async def restore_wallet_from_keys(
        self,
        filename: str,
        address: str,
        viewkey: str,
        spendkey: str,
        restore_height: int,
    ) -> dict:
        """
        Restore a wallet from a set of keys.

        Parameters
        ----------
        filename : str
            Wallet file name.
        address : str
            Wallet public address.
        viewkey : str
            Wallet view key.
        spendkey : str
            Wallet spend key.
        restore_height : int
            Wallet restore height.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "restore_wallet_from_keys",
            {
                "filename": filename,
                "address": address,
                "viewkey": viewkey,
                "spendkey": spendkey,
                "restore_height": restore_height,
            },
        )

    async def is_multisig(self) -> dict:
        """
        Check if the wallet is a multisig wallet.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("is_multisig", {})

    async def prepare_multisig(self) -> dict:
        """
        Prepare a wallet for multisig use.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("prepare_multisig", {})

    async def make_multisig(
        self, multisig_info: list, threshold: int, password: str
    ) -> dict:
        """
        Make a wallet multisig.

        Parameters
        ----------
        multisig_info : list
            Array of multisig info from other participants.
        threshold : int
            Number of signatures needed to sign a transfer.
        password : str
            Wallet password.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "make_multisig",
            {
                "multisig_info": multisig_info,
                "threshold": threshold,
                "password": password,
            },
        )

    async def export_multisig_info(self) -> dict:
        """
        Export multisig info for other participants.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("export_multisig_info", {})

    async def import_multisig_info(self, info: list[str]) -> dict:
        """
        Import multisig info from other participants.

        Parameters
        ----------
        info : list[str]
            Array of multisig info from other participants.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("import_multisig_info", {"info": info})

    async def finalize_multisig(
        self, multisig_info: list[str], password: str
    ) -> dict:
        """
        Finalize a multisig wallet.

        Parameters
        ----------
        multisig_info : list[str]
            Array of multisig info from other participants.
        password : str
            Wallet password.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "finalize_multisig",
            {"multisig_info": multisig_info, "password": password},
        )

    async def exchange_multisig_keys(
        self, multisig_info: list[str], password: str
    ) -> dict:
        """
        Exchange multisig keys with other participants.

        Parameters
        ----------
        multisig_info : list[str]
            Array of multisig info from other participants.
        password : str
            Wallet password.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "exchange_multisig_keys",
            {"multisig_info": multisig_info, "password": password},
        )

    async def sign_multisig(self, tx_data_hex: str) -> dict:
        """
        Sign a multisig transaction.

        Parameters
        ----------
        tx_data_hex : str
            Transaction in hex format.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("sign_multisig", {"tx_data_hex": tx_data_hex})

    async def submit_multisig(self, tx_data_hex: str) -> dict:
        """
        Submit a signed multisig transaction.

        Parameters
        ----------
        tx_data_hex : str
            Transaction in hex format.

        Returns
        -------
        dict
            The submitted transaction.

        """
        return await self._request("submit_multisig", {"tx_data_hex": tx_data_hex})

    async def validate_address(
        self,
        address: str,
        any_net_type: Optional[bool] = False,
        allow_openalias: Optional[bool] = False,
    ) -> dict:
        """
        Validate a public address.

        Parameters
        ----------
        address : str
            Public address.
        any_net_type : bool, optional
            Allow any net type.
        allow_openalias : bool, optional
            Allow OpenAlias addresses.


        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "validate_address",
            {
                "address": address,
                "any_net_type": any_net_type,
                "allow_openalias": allow_openalias,
            },
        )

    async def set_daemon(
        self,
        address: str,
        trusted: bool,
        ssl_support: Optional[str] = "autodetect",
        ssl_private_key_path: Optional[str] = None,
        ssl_certificate_path: Optional[str] = None,
        ssl_ca_file: Optional[str] = None,
        ssl_allowed_fingerprints: Optional[list[str]] = None,
        ssl_allow_any_cert: Optional[bool] = False,
    ) -> dict:
        """
        Set the daemon address.

        Parameters
        ----------
        address : str
            Daemon public address.
        trusted : bool
            If true, trust the daemon.
        ssl_support : str, optional
            SSL support (autodetect, enabled, disabled).
        ssl_private_key_path : str, optional
            SSL private key path.
        ssl_certificate_path : str, optional
            SSL certificate path.
        ssl_ca_file : str, optional
            SSL CA file.
        ssl_allowed_fingerprints : list[str], optional
            SSL allowed fingerprints.
        ssl_allow_any_cert : bool, optional
            Allow any certificate.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request(
            "set_daemon",
            {
                "address": address,
                "trusted": trusted,
                "ssl_support": ssl_support,
                "ssl_private_key_path": ssl_private_key_path,
                "ssl_certificate_path": ssl_certificate_path,
                "ssl_ca_file": ssl_ca_file,
                "ssl_allowed_fingerprints": ssl_allowed_fingerprints,
                "ssl_allow_any_cert": ssl_allow_any_cert,
            },
        )

    async def set_log_level(self, level: int) -> dict:
        """
        Set the log level.

        Parameters
        ----------
        level : int
            Log level.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("set_log_level", {"level": level})

    async def set_log_categories(self, categories: str) -> dict:
        """
        Set the log categories.

        Parameters
        ----------
        categories : str
            Log categories.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("set_log_categories", {"categories": categories})

    async def get_version(self) -> dict:
        """
        Get the wallet version.

        Returns
        -------
        dict
            The response from wallet RPC.

        """
        return await self._request("get_version", {})
