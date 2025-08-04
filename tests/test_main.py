from demo_application.main import main
import sys
from io import StringIO


def test_main():
    """Test that main() prints the expected message."""
    captured_output = StringIO()
    sys.stdout = captured_output
    main()
    sys.stdout = sys.__stdout__
    assert "Hello from demo application!" in captured_output.getvalue()
