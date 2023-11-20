import pytest
from pydantic_core import ValidationError
from app.schemas.scheme_templates import RequestScheme, Template


class TestRequest:

    def test_test_request_scheme_validate_before_create_model(
        self,
        mock_data: tuple[dict[str, str], Template]
            ) -> None:
        """Test scheme validate data before create model
        """

        scheme = RequestScheme(**mock_data[0])
        assert scheme.email in mock_data[0].keys(), 'not validated email'
        assert scheme.phone in mock_data[0].keys(), 'not validated phone'
        assert scheme.date in mock_data[0].keys(), 'not validated date'
        assert scheme.text_fields[0] in mock_data[0].keys(), 'not validated text'
        assert len(scheme.text_fields) == 2, 'wrong text fields len'

    def test_request_scheme_raise_if_multiplre_emails(
        self,
        mock_data: tuple[dict[str, str], Template]
            ) -> None:
        """Test request validation raise error if multiple emails
        """
        mock_data[0]['yet_another_email'] = 'ww@ops.ru'
        with pytest.raises(
            ValidationError,
            match='To many emails in request data'
                ):
            RequestScheme(**mock_data[0])

    def test_request_scheme_raise_if_multiplre_phons(
        self,
        mock_data: tuple[dict[str, str], Template]
            ) -> None:
        """Test request validation raise error if multiple phones
        """
        mock_data[0]['yet_another_phone'] = '+7 000 000 00 00'
        with pytest.raises(
            ValidationError,
            match='To many phone numbers in request data'
                ):
            RequestScheme(**mock_data[0])

    def test_request_scheme_raise_if_multiplre_dates(
        self,
        mock_data: tuple[dict[str, str], Template]
            ) -> None:
        """Test request validation raise error if multiple dates
        """
        mock_data[0]['yet_another_date'] = '2012.12.01'
        with pytest.raises(
            ValidationError,
            match='To many dates in request data'
                ):
            RequestScheme(**mock_data[0])

    @pytest.mark.parametrize(
        "todel",
        ["some_email", "some_phone", "some_date", "some_text"]
            )
    def test_request_scheme_raise_if_not_all_fields_exist(
        self,
        todel: str,
        mock_data: tuple[dict[str, str], Template]
            ) -> None:
        """Test request validation raise error if uncompleted
        """
        del mock_data[0]['name']
        del mock_data[0][todel]
        with pytest.raises(
            ValidationError,
            match='Not all 4 fields are exist in request data'
                ):
            RequestScheme(**mock_data[0])
