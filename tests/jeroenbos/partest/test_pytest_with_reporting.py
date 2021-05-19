class TestPytestWithReporting:
    def test_importing_fixtures(self, temp_test_file):
        assert isinstance(temp_test_file, str)
        assert temp_test_file.endswith(".py")
