# __init__.py
# Relative Path: app/database/postgres/__init__.py
from .process_tests import select_rules_data as axe_postgres, mark_rule_as_processed
from .fetch_unprocessed import fetch_unprocessed_rules