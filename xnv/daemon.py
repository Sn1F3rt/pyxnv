from typing import Optional

import aiohttp


__all__ = ["Daemon"]


class Daemon:
    """
    A class to interact with the Nerva daemon's JSON-RPC interface.

    Attributes:
    -----------
    url : str
        The URL of the daemon.
    timeout : float
        The timeout for the request.
    endpoint : str
        The endpoint for the request.
    headers : dict
        The headers for the request.

    """

    __slots__ = ["url", "timeout", "endpoint", "headers"]

    def __init__(
        self,
        host: Optional[str] = "localhost",
        port: Optional[int] = 5000,
        ssl: Optional[bool] = False,
        timeout: Optional[float] = 10.0,
    ):
        self.url = f"{'https' if ssl else 'http'}://{host}:{port}"
        self.timeout = timeout

        self.endpoint = "json_rpc"
        self.headers = {"Content-Type": "application/json"}

    async def _request(self, method: str, params: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}/{self.endpoint}",
                json={"jsonrpc": "2.0", "id": 0, "method": method, "params": params},
                headers=self.headers,
                timeout=self.timeout,
            ) as response:
                return await response.json()

    async def get_block_count(self) -> dict:
        """
        Get the current block count.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_block_count", {})

    async def on_get_block_hash(self, height: int) -> dict:
        """
        Get the block hash at a certain height.

        Parameters:
        -----------
        height : int
            The height of the block.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("on_get_block_hash", {"height": height})

    async def get_block_template(
        self, wallet_address: str, reserve_size: int
    ) -> dict:
        """
        Get a block template for mining.

        Parameters:
        -----------
        wallet_address : str
            The wallet address to mine to.

        reserve_size : int
            The reserve size.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request(
            "get_block_template",
            {"wallet_address": wallet_address, "reserve_size": reserve_size},
        )

    async def submit_block(self, block_blob: list[str]) -> dict:
        """
        Submit a block to the network.

        Parameters:
        -----------
        block_blob : list[str]
            (Optional) The block blob to submit.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("submit_block", {"blob": block_blob})

    async def get_last_block_header(self) -> dict:
        """
        Get the last block header.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_last_block_header", {})

    async def get_block_header_by_hash(self, block_hash: str) -> dict:
        """
        Get the block header by hash.

        Parameters:
        -----------
        block_hash : str
            The hash of the block.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_block_header_by_hash", {"hash": block_hash})

    async def get_block_header_by_height(self, height: int) -> dict:
        """
        Get the block header by height.

        Parameters:
        -----------
        height : int
            The height of the block.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_block_header_by_height", {"height": height})

    async def get_block_headers_range(
        self, start_height: int, end_height: int
    ) -> dict:
        """
        Get a range of block headers.

        Parameters:
        -----------
        start_height : int
            The start height.
        end_height : int
            The end height.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request(
            "get_block_headers_range",
            {"start_height": start_height, "end_height": end_height},
        )

    async def get_block(
        self, block_hash: Optional[str] = None, height: Optional[int] = None
    ) -> dict:
        """
        Get a block by hash or height.

        Parameters:
        -----------
        block_hash : str
            The hash of the block.
        height : int
            The height of the block.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        if block_hash and not height:
            return await self._request("get_block", {"hash": block_hash})

        elif height and not block_hash:
            return await self._request("get_block", {"height": height})

        else:
            raise ValueError("Either block_hash OR height must be provided.")

    async def get_connections(self) -> dict:
        """
        Get the connections to the daemon.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_connections", {})

    async def get_info(self) -> dict:
        """
        Get the information about the daemon.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_info", {})

    async def hard_fork_info(self) -> dict:
        """
        Get the hard fork information.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("hard_fork_info", {})

    async def set_bans(self, bans: list) -> dict:
        """
        Set bans for the daemon.

        Parameters:
        -----------
        bans : list
            The bans to set. Each ban should be a dictionary with the following keys:
                - host : str
                    Host to ban (IP in A.B.C.D format).
                - ip : int (optional)
                    IP to ban (int format).
                - ban : bool
                    Set `true` to ban, `false` to unban.
                - seconds : int
                    Time to ban in seconds.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("set_bans", {"bans": bans})

    async def get_bans(self) -> dict:
        """
        Get the bans of the daemon.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_bans", {})

    async def flush_txpool(self, txids: Optional[list] = None) -> dict:
        """
        Flush the transaction pool.

        Parameters:
        -----------
        txids : list
            (Optional) The transaction IDs to flush. If not provided, all transactions will be flushed.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("flush_txpool", {"txids": txids or []})

    async def get_output_histogram(
        self,
        amounts: list,
        min_count: int,
        max_count: int,
        unlocked: bool,
        recent_cutoff: int,
    ) -> dict:
        """
        Get the output histogram.

        Parameters:
        -----------
        amounts : list
            The amounts to get the histogram for.
        min_count : int
            The minimum count.
        max_count : int
            The maximum count.
        unlocked : bool
            Whether to get the unlocked outputs.
        recent_cutoff : int
            The recent cutoff.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request(
            "get_output_histogram",
            {
                "amounts": amounts,
                "min_count": min_count,
                "max_count": max_count,
                "unlocked": unlocked,
                "recent_cutoff": recent_cutoff,
            },
        )

    async def get_version(self) -> dict:
        """
        Get the version of the daemon.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_version", {})

    async def get_coinbase_tx_sum(self, height: int, count: int) -> dict:
        """
        Get the coinbase transaction sum.

        Parameters:
        -----------
        height : int
            The height of the block.
        count : int
            The count of blocks.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request(
            "get_coinbase_tx_sum", {"height": height, "count": count}
        )

    async def get_fee_estimate(self, grace_blocks: Optional[int] = None) -> dict:
        """
        Get the fee estimate.

        Parameters:
        -----------
        grace_blocks : int
            (Optional) The grace blocks.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request(
            "get_fee_estimate",
            {"grace_blocks": grace_blocks} if grace_blocks else {},
        )

    async def get_alternate_chains(self) -> dict:
        """
        Get the alternate chains.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_alternate_chains", {})

    async def relay_tx(self, txids: list) -> dict:
        """
        Relay transactions to the network.

        Parameters:
        -----------
        txids : list
            The transaction IDs to relay.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("relay_tx", {"txids": txids})

    async def sync_info(self) -> dict:
        """
        Get the sync information of the daemon.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("sync_info", {})

    async def get_txpool_backlog(self) -> dict:
        """
        Get the transaction pool backlog.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_txpool_backlog", {})

    async def get_output_distribution(
        self, amounts: list, from_height: int, to_height: int, cumulative: bool
    ) -> dict:
        """
        Get the output distribution.

        Parameters:
        -----------
        amounts : list
            The amounts to get the distribution for.
        from_height : int
            The height to start from.
        to_height : int
            The height to end at.
        cumulative : bool
            Whether to get the cumulative distribution.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request(
            "get_output_distribution",
            {
                "amounts": amounts,
                "from_height": from_height,
                "to_height": to_height,
                "cumulative": cumulative,
            },
        )

    async def prune_blockchain(self) -> dict:
        """
        Prune the blockchain.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("prune_blockchain", {})

    async def flush_cache(self, bad_txs: Optional[bool] = False) -> dict:
        """
        Flush the cache.

        Parameters:
        -----------
        bad_txs : bool
            Whether to flush the bad transactions.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("flush_cache", {"bad_txs": bad_txs})

    async def get_generated_coins(self, height: Optional[int] = None) -> dict:
        """
        Get the generated coins.

        Parameters:
        -----------
        height : int
            (Optional) The height.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request(
            "get_generated_coins", {"height": height} if height else {}
        )

    async def get_min_version(self) -> dict:
        """
        Get the minimum version of the daemon.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_min_version", {})

    async def get_tx_pubkey(self, extra: str) -> dict:
        """
        Get the transaction public key.

        Parameters:
        -----------
        extra : str
            The extra data.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("get_tx_pubkey", {"extra": extra})

    async def decode_outputs(
        self, tx_hashes: list, sec_view_key: str, address: str
    ) -> dict:
        """
        Decode the outputs of transactions.

        Parameters:
        -----------
        tx_hashes : list
            The transaction hashes.
        sec_view_key : str
            The secret view key.
        address : str
            The address to decode.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request(
            "decode_outputs",
            {
                "tx_hashes": tx_hashes,
                "sec_view_key": sec_view_key,
                "address": address,
            },
        )

    async def add_peer(self, host: str) -> dict:
        """
        Add a peer to the daemon.

        Parameters:
        -----------
        host : str
            The host of the peer.

        Returns:
        --------
        dict
            The response from the daemon.

        """
        return await self._request("add_peer", {"host": host})
