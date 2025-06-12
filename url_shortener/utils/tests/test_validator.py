from url_shortener.utils.validator import validate_url


async def test_validate_url():
    is_cor_url1 = await validate_url("http://localhost:8080/urls/a")
    assert is_cor_url1

    is_cor_url2 = await validate_url("wrong_url")
    assert not is_cor_url2
