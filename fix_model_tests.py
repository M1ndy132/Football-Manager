#!/usr/bin/env python3
"""
Script to fix SQLAlchemy model test assertions by replacing direct attribute comparisons with getattr calls.
"""
import re

def fix_model_test_file():
    file_path = r"c:\Users\Amanda\AppData\Local\GitHubDesktop\app-3.5.2\Football-Manager\app\tests\unit test\model.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match assert statements with model attribute comparisons
    pattern = r'assert (\w+)\.(\w+) (==|!=) (.+)'
    
    def replace_assertion(match):
        object_name = match.group(1)
        attribute = match.group(2)
        operator = match.group(3)
        value = match.group(4)
        
        # Skip if it's already using getattr or if it's checking .id or other special cases
        if attribute in ['id', 'created_at', 'updated_at'] or 'getattr' in match.group(0):
            return match.group(0)
        
        return f"assert getattr({object_name}, '{attribute}') {operator} {value}"
    
    # Apply the replacement
    fixed_content = re.sub(pattern, replace_assertion, content)
    
    # Also add refresh calls where needed
    commit_pattern = r'(\s+test_db\.commit\(\))\n(\s+)(assert \w+\.id is not None)'
    refresh_replacement = r'\1\n\2test_db.refresh(\w+)  # Refresh to ensure values are loaded\n\2\3'
    
    # This is more complex, let's do it manually for now
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed model test file assertions")

if __name__ == "__main__":
    fix_model_test_file()
