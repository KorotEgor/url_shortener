import logging

logger = logging.getLogger(__name__)


class TransUrl:
    def __init__(self, last_coomb=""):
        self.url_chars = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )

        coomb = "http://localhost:8080/urls/"
        if last_coomb:
            coomb += last_coomb[:-1]
        self.last_coomb = coomb

        last_ch_num = 1
        if last_coomb:
            last_ch_num = self.url_chars.find(last_coomb[-1]) + 1
        self.last_ch_num = last_ch_num

        last_added_ch_num = 0
        if len(last_coomb) > 1:
            last_added_ch_num = self.url_chars.find(last_coomb[-2])
        self.last_added_ch_num = last_added_ch_num

    async def get_short_url(self):
        new_char = self.url_chars[self.last_ch_num]

        if self.last_ch_num == 0:
            self.last_coomb += self.url_chars[self.last_added_ch_num]
            self.last_added_ch_num += 1

        self.last_ch_num = (self.last_ch_num + 1) % 62

        new_url = self.last_coomb + new_char
        logger.info(f"new_url: {new_url}")
        return new_url


async def get_last_coomb(urls_repo):
    url = await urls_repo.get_last_short_url()

    if url is None:
        return ""

    last_coomb = url[url.rfind("/") + 1 :]

    return last_coomb
