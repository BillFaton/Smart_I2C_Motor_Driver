# Documentation

This directory contains the MkDocs documentation for the Smart I2C Motor Driver.

## Building Documentation Locally

### Using pip

```bash
pip install -e .[docs]
mkdocs serve
```

### Using uv (faster)

```bash
uv pip install -e .[docs]
mkdocs serve
```

Visit http://127.0.0.1:8000 to view the documentation.

## GitHub Pages Deployment

Documentation is automatically deployed to GitHub Pages when you push to the main branch.

### Initial Setup

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to Settings → Pages
   - Under "Source", select "Deploy from a branch"
   - Choose the `gh-pages` branch and `/root` folder
   - Click Save

3. **Wait for deployment**:
   - The GitHub Action will run automatically
   - Check the "Actions" tab to monitor progress
   - Once complete, your docs will be live at:
     `https://yourusername.github.io/smart-i2c-motor-driver`

### Manual Deployment

If you need to deploy manually:

```bash
mkdocs gh-deploy
```

This will build and push directly to the `gh-pages` branch.

## Documentation Structure

```
docs/
├── index.md                    # Home page
├── installation.md             # Installation guide
├── getting-started.md          # Quick start tutorial
├── troubleshooting.md          # Common issues
├── user-guide/
│   ├── basic-usage.md         # Basic usage patterns
│   └── cli.md                 # CLI reference
└── reference/
    ├── core.md                # Core API reference
    └── transports.md          # Transport API reference
```

## Adding New Pages

1. Create a new `.md` file in the appropriate directory
2. Add it to the `nav` section in `mkdocs.yml`
3. Commit and push to deploy

## MkDocs Material Theme

This project uses the Material theme with the following features:

- Dark/light mode toggle
- Search functionality
- Code syntax highlighting
- API documentation auto-generation (mkdocstrings)
- Mobile-responsive design

## Troubleshooting

### Build Fails

If the documentation build fails:

1. Check for syntax errors in Markdown files
2. Verify all links are valid
3. Ensure mkdocstrings can import the package:
   ```bash
   python -c "import smart_i2c_motor_driver"
   ```

### GitHub Pages Not Updating

1. Check the Actions tab for errors
2. Verify the `gh-pages` branch exists
3. Confirm GitHub Pages is enabled in repository settings
4. Check that the workflow has write permissions:
   - Settings → Actions → General → Workflow permissions
   - Select "Read and write permissions"
