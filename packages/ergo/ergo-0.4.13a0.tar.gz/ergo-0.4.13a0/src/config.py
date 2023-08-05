"""Summary."""
from typing import Dict, Optional

from src.topic import PubTopic, SubTopic, Topic


class Config:
    """Summary."""

    def __init__(self, config: Dict[str, str]):
        """Summary.

        Args:
            config (Dict[str, str]): Description
        """
        self._func: str = config['func']
        self._namespace: Optional[str] = config.get('namespace', 'local')
        self._pubtopic: Topic = PubTopic(config.get('pubtopic'))
        self._subtopic: Topic = SubTopic(config.get('subtopic'))
        self._host: Optional[str] = config.get('host')
        self._exchange: Optional[str] = config.get('exchange')
        self._protocol: str = config.get('protocol', 'stack')  # http, amqp, stdio, stack

    @property
    def namespace(self) -> Optional[str]:
        """Summary.

        Returns:
            TYPE: Description
        """
        return self._namespace

    @property
    def subtopic(self) -> Topic:
        """Summary.

        Returns:
            TYPE: Description
        """
        return self._subtopic

    @property
    def pubtopic(self) -> Topic:
        """Summary.

        Returns:
            TYPE: Description
        """
        return self._pubtopic

    @property
    def func(self) -> str:
        """Summary.

        Returns:
            TYPE: Description
        """
        return self._func

    @property
    def host(self) -> Optional[str]:
        """Summary.

        Returns:
            TYPE: Description
        """
        return self._host

    @property
    def exchange(self) -> Optional[str]:
        """Summary.

        Returns:
            TYPE: Description
        """
        return self._exchange

    @property
    def protocol(self) -> str:
        """Summary.

        Returns:
            TYPE: Description
        """
        return self._protocol
