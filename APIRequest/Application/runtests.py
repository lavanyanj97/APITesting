import pytest

# List your test files in the order you want them to run
test_files = [
    'test_applicationpostpositive.py',
    'test_application_postvalidations.py',
    'test_applicationget.py',
    'test_applicationget_name.py',
    'test_applicationget_history.py',
    'test_applicationget_name.py'  # Duplicate, ensure this is intentional
]

# Run pytest for each test file in the specified order
for test_file in test_files:
    pytest.main([test_file])
