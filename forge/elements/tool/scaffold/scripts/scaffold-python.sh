#!/bin/bash
# Scaffold a Python project
set -e

PROJECT_NAME="${1:-my-project}"
PROJECT_DESC="${2:-A new Python project}"

echo "Scaffolding Python project: $PROJECT_NAME"

# Create directory structure
mkdir -p "$PROJECT_NAME/src/$PROJECT_NAME"
mkdir -p "$PROJECT_NAME/tests"

# Copy templates and substitute variables
TEMPLATE_DIR="$(dirname "$0")/../templates/python"

# Function to process template
process_template() {
    local template="$1"
    local output="$2"
    sed -e "s/{{project_name}}/$PROJECT_NAME/g" \
        -e "s/{{project_description}}/$PROJECT_DESC/g" \
        "$template" > "$output"
}

# Process templates
process_template "$TEMPLATE_DIR/pyproject.toml.template" "$PROJECT_NAME/pyproject.toml"
process_template "$TEMPLATE_DIR/README.md.template" "$PROJECT_NAME/README.md"
process_template "$TEMPLATE_DIR/src/__init__.py.template" "$PROJECT_NAME/src/$PROJECT_NAME/__init__.py"
process_template "$TEMPLATE_DIR/src/cli.py.template" "$PROJECT_NAME/src/$PROJECT_NAME/cli.py"

# Create empty test file
cat > "$PROJECT_NAME/tests/test_basic.py" << EOF
"""Basic tests for $PROJECT_NAME"""

def test_import():
    """Test that the package can be imported."""
    import ${PROJECT_NAME//-/_}
    assert ${PROJECT_NAME//-/_}.__version__ == "0.1.0"
EOF

# Create .gitignore
cat > "$PROJECT_NAME/.gitignore" << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
env/
venv/
EOF

echo "✓ Python project scaffolded successfully!"
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  pip install -e '.[dev]'"
echo "  $PROJECT_NAME"
