import asyncio
import logging
from dataclasses import dataclass
from typing import Optional, Tuple

from plcx.constants import MAX_TRY, TIMEOUT

logger = logging.getLogger(__name__)


async def connect(
    host: str, port: int, time_out: float = TIMEOUT, max_try: int = MAX_TRY,
) -> Tuple[asyncio.streams.StreamReader, asyncio.streams.StreamWriter]:
    """
    Create connection to server.

    :param host: host url or ip
    :param port: host port
    :param time_out: waiting time out, use in connection and reading response [.5 second]
    :param max_try: maximum attention to create server [3 times]
    :return:
    """
    try_count = 0
    while True:
        try:
            logger.info(f"try `{try_count}` to establish connection to server `{host}:{port}`")
            return await asyncio.wait_for(asyncio.open_connection(host=host, port=port), timeout=time_out)
        except (OSError, asyncio.TimeoutError) as error:
            try_count += 1
            if try_count >= max_try:
                logger.error(error)  # log error without traceback
                raise error

            await asyncio.sleep(0.3)  # wait for new try


async def clientx(
    host: str,
    port: int,
    message: bytes,
    response_bytes: int = 0,  # zero means no response
    time_out: float = TIMEOUT,
    max_try: int = MAX_TRY,
) -> bytes:
    """
    Send message to server.

    :param host: host url or ip
    :param port: host port
    :param message: bytes message
    :param response_bytes: max number of bytes to read [0 == empty response]
    :param time_out: waiting time out, use in connection and reading response [.5 second]
    :param max_try: maximum attention to create server [3 times]
    :return:
    """
    # open connection with timeout
    reader, writer = await connect(host=host, port=port, time_out=time_out, max_try=max_try)

    # send message to server
    writer.write(message)
    logger.debug(f"send message to server `{message}`")

    # get response with timeout
    response = await asyncio.wait_for(reader.read(response_bytes), timeout=time_out)
    logger.debug(f"receive response `{response}` form server")

    # close connection
    writer.close()
    logger.info("connection closed")

    return response


@dataclass
class ClientX:
    host: str
    port: int
    response_bytes: int = 0
    time_out: float = TIMEOUT
    max_try: int = MAX_TRY

    def send(
        self,
        message: bytes,
        response_bytes: Optional[int] = None,
        time_out: Optional[float] = None,
        max_try: Optional[int] = None,
    ) -> bytes:
        """
        Send message.

        :param message: bytes massage
        :param response_bytes: max number of bytes to read [0 == empty response]
        :param time_out: waiting time out, use in connection and reading response [.5 second]
        :param max_try: maximum attention to create server [3 times]
        :return: response bytes message or None
        """
        logger.debug(f"try send message with client to `{self.host}:{self.port}`")

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            clientx(
                self.host,
                self.port,
                message,
                response_bytes or self.response_bytes,
                time_out or self.time_out,
                max_try or self.max_try,
            )
        )
