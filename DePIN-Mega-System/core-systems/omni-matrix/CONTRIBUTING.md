# Contributing to Omni-Matrix

Thank you for your interest in contributing to Omni-Matrix! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- 🐛 **Bug Reports**: Report issues you encounter
- 💡 **Feature Requests**: Suggest new features or improvements
- 📝 **Documentation**: Improve docs and tutorials
- 🔧 **Code**: Submit bug fixes or new features
- 🧪 **Testing**: Help test and validate changes

## 🚀 Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/omni-matrix.git
   cd omni-matrix
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Create Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Code Guidelines

### Python Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Maximum line length: 100

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description.
    
    Args:
        param1: Description
        param2: Description
        
    Returns:
        Description of return value
    """
    return True
```

### Testing

- Write tests for new features
- Maintain >80% code coverage
- Run tests before submitting

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=omni-matrix --cov-report=html
```

### Documentation

- Update README.md if needed
- Add docstrings to functions
- Update configuration docs

## 🔧 Development Setup

### Environment Variables

```bash
# Copy example
cp .env.example .env

# Edit with your test keys
nano .env
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install
```

## 📋 Submitting Changes

1. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

2. **Push to Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Fill in the template
   - Submit PR

### Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

**Example:**
```
feat(ai): add support for GPT-4 Turbo

Implement GPT-4 Turbo integration with improved
token efficiency and reduced latency.

Closes #123
```

## 🏗️ Architecture Guidelines

### Adding New Networks

1. Add to `config/default.json`
2. Implement in `modules/resource_scavenger.py`
3. Add health check in `modules/network_mesh.py`
4. Write tests

### Adding New AI Models

1. Add endpoint to `modules/ai_dispatcher.py`
2. Update `model_endpoints` dictionary
3. Add to fallback chain
4. Test inference

### Adding Storage Backends

1. Implement in `modules/storage_sharder.py`
2. Add `_store_on_*` method
3. Add `_retrieve_from_*` method
4. Update config

## 🐛 Bug Reports

When reporting bugs, include:

- **Description**: Clear description
- **Steps**: How to reproduce
- **Expected**: What should happen
- **Actual**: What happens
- **Environment**: OS, Python version, etc.
- **Logs**: Relevant log output

## 💡 Feature Requests

When requesting features:

- **Use Case**: Why is this needed?
- **Proposal**: How should it work?
- **Alternatives**: Other approaches considered
- **Impact**: Who benefits?

## 🏷️ Labels

- `bug`: Something is broken
- `enhancement`: New feature
- `documentation`: Docs improvement
- `good first issue`: Easy for beginners
- `help wanted`: Need assistance
- `priority/high`: Urgent

## 📞 Contact

- GitHub Issues: [github.com/omni-matrix/omni-matrix/issues](https://github.com/omni-matrix/omni-matrix/issues)
- Discord: [discord.gg/omni-matrix](https://discord.gg/omni-matrix)
- Email: dev@omni-matrix.io

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 🙏 Thank You!

Your contributions make Omni-Matrix better for everyone!

---

<p align="center">
  <strong>Built with 💙 by the Omni-Matrix Community</strong>
</p>
