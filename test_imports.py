# File: C:\Users\mehul\IdeaProjects\AlgomaticsLearn1\test_imports.py
import sys
print(sys.path)
try:
    import backend.app
    print("Successfully imported backend.app")
except ImportError as e:
    print(f"Error importing backend.app: {e}")