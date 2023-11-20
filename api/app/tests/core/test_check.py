from app.core.check import check_text
from app.schemas.scheme_templates import Template


def test_check_text_return_correct_data(
    mock_data: tuple[dict[str, str], Template]
        ) -> None:
    """Test check test correct data
    """
    result = check_text(
        [mock_data[1].model_dump(), ],
        [mock_data[1].name, ],
            )
    assert isinstance(result, list), 'wrong type'
    assert len(result) == 1, 'wrong len'
    assert result[0] == mock_data[1].model_dump(), 'wrong data'


def test_check_text_return_filtered_data(
    mock_data: tuple[dict[str, str], Template]
        ) -> None:
    """Test check test filtered
    """
    result = check_text(
        [mock_data[1].model_dump(), ],
        ['some imposible name', ],
            )
    assert isinstance(result, list), 'wrong type'
    assert len(result) == 0, 'wrong len'
