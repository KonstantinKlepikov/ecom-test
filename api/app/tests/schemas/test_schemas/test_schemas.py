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

    # TODO: test raises and variants
