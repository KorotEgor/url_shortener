import logging

logger = logging.getLogger(__name__)


class TransUrl:
    def __init__(self):
        self.url_chars = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )
        self.last_coomb = "http://localhost:8080/urls/"
        self.last_ch_num = 1
        self.last_added_ch_num = 0

    async def get_short_url(self):
        new_char = self.url_chars[self.last_ch_num]

        if self.last_ch_num == 0:
            self.last_coomb += self.url_chars[self.last_added_ch_num]
            self.last_added_ch_num += 1

        self.last_ch_num = (self.last_ch_num + 1) % 62

        new_url = self.last_coomb + new_char
        logger.info(f"new_url: {new_url}")
        return new_url
