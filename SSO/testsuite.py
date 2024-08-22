import pytest

# List of test files to run
test_files = [
    "test_login.py",
    "test_loginnegative.py",
    "test_logout.py"
]

if __name__ == "__main__":
    for test_file in test_files:
        pytest.main([test_file])


#enter "python test_suite.py" in the terminal to run the suite