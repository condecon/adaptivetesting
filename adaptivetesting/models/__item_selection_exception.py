class ItemSelectionException(Exception):
    """Custom exception for item selection errors in adaptive testing."""
    def __init__(self, *args):
        super().__init__(*args)
