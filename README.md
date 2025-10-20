# Remote Development Workshop

A hands-on workshop repository demonstrating **Docker-based remote development workflows**. This repository contains example code and configuration for the [Remote Development Workshop](https://idea-lab-1.gitbook.io/remote-development), teaching modern containerized development practices.

> **Workshop Focus**: This workshop teaches you how to develop applications entirely within Docker containers using IDE remote development features. No local Python installation required - everything runs in containers!

## What You'll Learn

- **Docker-Based Development**: Develop applications without installing languages/dependencies locally
- **IDE Docker Interpreters**: Use VS Code Remote Containers and PyCharm Docker interpreters
- **Reproducible Environments**: Ensure consistent development environments across teams
- **Container-First Workflows**: Modern development practices with containerization
- **Automated CI/CD**: Build and deploy Docker images automatically with GitHub Actions
- **Remote Development Best Practices**: Work efficiently with containerized applications

## Prerequisites

All you need is:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Git**: [Install Git](https://git-scm.com/downloads)
- **An IDE**: [VS Code](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/)

**No Python, pip, or virtual environments needed!** Everything runs inside Docker.

## Project Structure

```
remote-dev-workshop/
├── .github/
│   └── workflows/
│       └── docker-build.yml    # CI/CD pipeline for automated Docker builds
├── data/
│   └── sample_signal.csv       # Sample data for the example application
├── src/
│   └── main.py                 # Example Python application
├── tests/
│   └── test_fft.py            # Example test suite
├── results/                    # Output directory (auto-generated)
├── Dockerfile                  # Container environment definition
├── requirements.txt            # Python dependencies (installed in container)
└── README.md                   # This file
```

**Note**: The Python code (signal processing example) is just a sample application. The focus is on the **Docker-based development workflow**, not the specific application logic.

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/sbazrafkan/remote-dev-workshop.git
cd remote-dev-workshop
```

### 2. Build the Docker Image

```bash
docker build -t remote-dev-workshop .
```

This creates a containerized development environment with all dependencies pre-installed.

### 3. Choose Your Development Workflow

You have several options for working with this containerized environment (detailed below):
- **Option A**: VS Code with Remote Containers (recommended for VS Code users)
- **Option B**: PyCharm with Docker Interpreter (recommended for PyCharm users)
- **Option C**: Command-line Docker execution (for quick testing)

## Development Workflows

### Option A: VS Code with Remote Containers

This is the recommended approach for VS Code users - your IDE runs inside the container!

#### Setup Steps:

1. **Install the Dev Containers extension**:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
   - Search for "Dev Containers" (Microsoft)
   - Click Install

2. **Create a `.devcontainer/devcontainer.json` file** (or use the workshop materials):
   ```json
   {
     "name": "Remote Dev Workshop",
     "build": {
       "dockerfile": "../Dockerfile"
     },
     "workspaceMount": "source=${localWorkspaceFolder},target=/opt/project,type=bind",
     "workspaceFolder": "/opt/project"
   }
   ```

3. **Open in Container**:
   - Press `F1` (or Cmd/Ctrl+Shift+P)
   - Type "Dev Containers: Reopen in Container"
   - Wait for container to build and connect

4. **Start Developing**:
   - Your terminal is now inside the container
   - Run: `python src/main.py`
   - Edit code, run tests, debug - all inside the container!

#### Key Benefits:
- ✅ No local Python installation needed
- ✅ IntelliSense and debugging work seamlessly
- ✅ Extensions run inside the container
- ✅ Terminal automatically connected to container

### Option B: PyCharm with Docker Interpreter

PyCharm Professional supports Docker interpreters natively.

#### Setup Steps:

1. **Open the project** in PyCharm

2. **Configure Docker Interpreter**:
   - Go to: `Settings/Preferences` → `Project` → `Python Interpreter`
   - Click the gear icon → `Add Interpreter` → `On Docker...`
   - Select your Docker image: `remote-dev-workshop:latest`
   - PyCharm will configure the interpreter automatically

3. **Set Path Mappings**:
   - Local path: `<project root>`
   - Container path: `/opt/project`

4. **Run Configuration**:
   - Right-click `src/main.py` → `Run 'main'`
   - PyCharm executes the script inside the container

#### Key Benefits:
- ✅ Full IDE features with Docker interpreter
- ✅ Debugging inside containers
- ✅ Automatic dependency resolution
- ✅ Database tools work with containerized databases

### Option C: Command-Line Docker Execution

For quick testing or CI/CD pipelines:

#### Run the Example Application:

```bash
docker run -it --rm \
  -v $(pwd):/opt/project \
  -w /opt/project \
  remote-dev-workshop \
  src/main.py
```

**Command Breakdown**:
- `-it`: Interactive terminal
- `--rm`: Remove container after exit
- `-v $(pwd):/opt/project`: Mount current directory into container
- `-w /opt/project`: Set working directory
- `src/main.py`: Script to execute

#### Run Tests Inside Container:

```bash
docker run -it --rm \
  -v $(pwd):/opt/project \
  -w /opt/project \
  remote-dev-workshop \
  -m pytest tests/
```

#### Interactive Shell for Exploration:

```bash
docker run -it --rm \
  -v $(pwd):/opt/project \
  -w /opt/project \
  remote-dev-workshop \
  /bin/bash
```

Then inside the container:
```bash
python src/main.py
pytest tests/
pip list
```

#### JupyterLab for Interactive Development:

```bash
docker run -it --rm \
  -v $(pwd):/opt/project \
  -w /opt/project \
  -p 8888:8888 \
  remote-dev-workshop \
  -m jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

Open the URL shown in terminal (e.g., `http://127.0.0.1:8888/lab?token=...`)

## Understanding the Docker Setup

### The Dockerfile

The `Dockerfile` defines your development environment:

```dockerfile
FROM python:3.10-slim                    # Base image with Python
RUN apt-get update && apt-get install... # System dependencies
COPY requirements.txt .                  # Copy dependency list
RUN pip install -r requirements.txt      # Install Python packages
ENTRYPOINT ["python"]                    # Default command
```

**Key Points**:
- All dependencies are installed in the container image
- No need to install Python, NumPy, SciPy, etc. on your local machine
- The image is portable and works identically on any system
- Changes to `requirements.txt` require rebuilding the image

### The Example Application

The repository includes a simple Python application (`src/main.py`) that:
1. Loads data from CSV
2. Performs signal processing
3. Generates output plots

**This code is just an example** - the focus is on how you develop it using Docker, not what it does.

### Dependencies in the Container

All Python packages are defined in `requirements.txt` and installed during image build:
- `numpy`, `scipy`, `pandas`: Data processing libraries
- `matplotlib`: Visualization
- `pytest`: Testing framework
- `jupyterlab`: Interactive development environment

When you use Docker interpreters, your IDE automatically has access to these packages.

## Advanced Docker Workflows

### Adding New Dependencies

When you need to install additional Python packages:

1. **Update `requirements.txt`**:
   ```txt
   numpy==1.26.4
   scipy==1.11.2
   pandas==2.1.0
   matplotlib==3.7.2
   pytest==7.3.1
   jupyterlab==4.4.1
   seaborn==0.12.2    # New package
   ```

2. **Rebuild the Docker image**:
   ```bash
   docker build -t remote-dev-workshop .
   ```

3. **If using VS Code Remote Containers**: Press `F1` → "Dev Containers: Rebuild Container"

4. **If using PyCharm**: The interpreter will automatically detect the rebuilt image

### Working with Multiple Containers

For complex applications (e.g., app + database), use `docker-compose.yml`:

```yaml
version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/opt/project
    working_dir: /opt/project
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
```

Run with: `docker-compose up`

### Debugging Inside Containers

#### VS Code:
- Set breakpoints in your code
- Press `F5` to start debugging
- Debugger runs inside the container automatically

#### PyCharm:
- Right-click code → "Debug 'main'"
- PyCharm attaches debugger to Docker interpreter
- Full debugging features available

### Sharing Your Environment

Your `Dockerfile` + `requirements.txt` ensures anyone can recreate your exact environment:

```bash
# Teammate clones repo
git clone https://github.com/sbazrafkan/remote-dev-workshop.git
cd remote-dev-workshop

# Builds identical environment
docker build -t remote-dev-workshop .

# Runs with same dependencies
docker run -it remote-dev-workshop src/main.py
```

**Result**: "Works on my machine" problems eliminated!

## Testing

Tests run inside the Docker container to ensure consistency:

### Run Tests via Docker:

```bash
docker run -it --rm \
  -v $(pwd):/opt/project \
  -w /opt/project \
  remote-dev-workshop \
  -m pytest tests/ -v
```

### Run Tests in VS Code:

With Dev Containers extension:
1. Open terminal (it's automatically inside the container)
2. Run: `pytest tests/ -v`
3. Or use Testing sidebar to run tests with GUI

### Run Tests in PyCharm:

With Docker interpreter configured:
1. Right-click `tests/` folder
2. Select "Run 'pytest in tests'"
3. Tests execute inside the container automatically

**Key Benefit**: Tests run in the same environment as production, eliminating environment-related test failures.

## CI/CD Pipeline

The repository demonstrates **automated Docker image building** with GitHub Actions (`.github/workflows/docker-build.yml`).

### What It Does:

1. **Triggers automatically** when you push changes to:
   - `Dockerfile`
   - `requirements.txt`
   - Workflow file itself

2. **Build Process**:
   - Validates Docker Hub credentials
   - Builds multi-platform images (Linux amd64 & arm64)
   - Tags images with branch name, commit SHA, and `latest`
   - Pushes to Docker Hub automatically
   - Uses GitHub Actions cache for faster builds

3. **Benefits**:
   - ✅ Team members can pull pre-built images instead of building locally
   - ✅ Ensures Docker image builds successfully before merging PRs
   - ✅ Automates deployment pipeline
   - ✅ Multi-architecture support for different systems

### Setting Up CI/CD (Optional)

To enable automatic Docker Hub pushes:

1. **Create Docker Hub access token**:
   - Go to [Docker Hub](https://hub.docker.com/) → Account Settings → Security
   - Click "New Access Token"
   - Copy the token

2. **Add GitHub Secrets**:
   - Go to your repo → Settings → Secrets and variables → Actions
   - Add `DOCKERHUB_USERNAME` (your Docker Hub username)
   - Add `DOCKERHUB_TOKEN` (the access token from step 1)

3. **Push changes**: The workflow runs automatically!

### Pulling Pre-built Images

If CI/CD is configured, skip building locally:

```bash
docker pull <dockerhub-username>/remote-dev-workshop:latest
docker run -it --rm \
  -v $(pwd):/opt/project \
  -w /opt/project \
  <dockerhub-username>/remote-dev-workshop:latest \
  src/main.py
```

## Troubleshooting

### Issue: "Docker daemon is not running"

**Symptoms**: Docker commands fail with connection errors

**Solution**: Start Docker:
- **macOS/Windows**: Open Docker Desktop application
- **Linux**: `sudo systemctl start docker`

Verify with: `docker info`

### Issue: "Permission denied" when building Docker image

**Symptoms**: Build fails with permission errors

**Solution**:
- **Linux**: Add your user to docker group: `sudo usermod -aG docker $USER` (then log out/in)
- **macOS/Windows**: Ensure Docker Desktop is running with proper permissions

### Issue: VS Code can't connect to container

**Symptoms**: "Failed to connect" error in VS Code

**Solutions**:
1. Ensure Docker is running: `docker ps`
2. Rebuild container: `F1` → "Dev Containers: Rebuild Container"
3. Check `.devcontainer/devcontainer.json` file exists
4. Try: `F1` → "Dev Containers: Rebuild Container Without Cache"

### Issue: PyCharm can't find Docker interpreter

**Symptoms**: Python interpreter not available or shows errors

**Solutions**:
1. Verify Docker image is built: `docker images | grep remote-dev-workshop`
2. Settings → Project → Python Interpreter → Add → On Docker
3. If using Docker Compose, select "Docker Compose" instead of "Docker"
4. Check path mappings are correct: `/opt/project`

### Issue: Container exits immediately

**Symptoms**: Container starts and stops right away

**Solution**: Specify a command to run:
```bash
# Wrong:
docker run remote-dev-workshop

# Correct:
docker run remote-dev-workshop src/main.py
# Or for interactive shell:
docker run -it remote-dev-workshop /bin/bash
```

### Issue: Changes to code not reflected in container

**Symptoms**: Code modifications don't affect container execution

**Solutions**:
1. **Volume mount issue**: Ensure using `-v $(pwd):/opt/project`
2. **VS Code**: Code changes are automatically reflected (files are mounted)
3. **PyCharm**: Check path mappings in interpreter settings
4. **Cached image**: If Dockerfile changed, rebuild: `docker build -t remote-dev-workshop .`

### Issue: "Module not found" inside container

**Symptoms**: Import errors for Python packages

**Solutions**:
1. Check package is in `requirements.txt`
2. Rebuild image: `docker build -t remote-dev-workshop .`
3. Verify image has package: `docker run remote-dev-workshop -m pip list`
4. If using VS Code, rebuild container: `F1` → "Dev Containers: Rebuild Container"

### Issue: Port already in use (JupyterLab)

**Symptoms**: Can't start JupyterLab, port 8888 busy

**Solution**: Use a different port:
```bash
docker run -it --rm \
  -v $(pwd):/opt/project \
  -w /opt/project \
  -p 8889:8888 \   # Changed local port to 8889
  remote-dev-workshop \
  -m jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

Then access at: `http://127.0.0.1:8889`

### Issue: GitHub Actions workflow failing

**Common causes**:
1. **Secrets not set**: Add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` in repo settings
2. **Invalid token**: Regenerate Docker Hub access token
3. **Dockerfile syntax error**: Test build locally first: `docker build .`
4. **Architecture issues**: Check workflow logs for specific platform errors

### Getting More Help

1. **Check Docker logs**: `docker logs <container-id>`
2. **Inspect image**: `docker inspect remote-dev-workshop`
3. **Interactive debugging**: `docker run -it remote-dev-workshop /bin/bash`
4. **Workshop documentation**: [https://idea-lab-1.gitbook.io/remote-development](https://idea-lab-1.gitbook.io/remote-development)

## Workshop Documentation

This repository is the companion code for the **Remote Development Workshop**.

📚 **Full workshop documentation**: [https://idea-lab-1.gitbook.io/remote-development](https://idea-lab-1.gitbook.io/remote-development)

### What's in the Workshop:

- **Conceptual Overview**: Why containerized development matters
- **Step-by-Step Tutorials**: Detailed setup guides for VS Code and PyCharm
- **Best Practices**: Docker development patterns and workflows
- **Advanced Topics**: Multi-container apps, debugging, performance optimization
- **Real-World Examples**: Case studies and use cases
- **Team Workflows**: Collaborative development with containers

This README provides technical reference; the GitBook provides learning materials and context.

## Why Docker-Based Development?

### Traditional Development Problems:
- ❌ "Works on my machine" issues
- ❌ Complex dependency installation
- ❌ Version conflicts between projects
- ❌ Difficult onboarding for new team members
- ❌ Different environments for dev/test/prod

### Docker-Based Development Solutions:
- ✅ Identical environments for all developers
- ✅ No local language/tool installation needed
- ✅ Isolated project dependencies
- ✅ One-command setup for new developers
- ✅ Production parity from day one

## Contributing

We welcome improvements to this workshop material!

### How to Contribute:

1. **Fork** this repository
2. **Create a branch**: `git checkout -b feature/your-improvement`
3. **Make your changes** (test in Docker!)
4. **Commit**: `git commit -m 'Add: description of improvement'`
5. **Push**: `git push origin feature/your-improvement`
6. **Open a Pull Request** with description of changes

### Contribution Ideas:
- Add examples for other IDEs (IntelliJ, Sublime, etc.)
- Improve Docker configuration
- Add support for more languages (Node.js, Java, Go, etc.)
- Enhance CI/CD pipeline examples
- Fix bugs or improve documentation

## Additional Resources

- **Docker Documentation**: [https://docs.docker.com/](https://docs.docker.com/)
- **VS Code Dev Containers**: [https://code.visualstudio.com/docs/devcontainers/containers](https://code.visualstudio.com/docs/devcontainers/containers)
- **PyCharm Docker Integration**: [https://www.jetbrains.com/help/pycharm/docker.html](https://www.jetbrains.com/help/pycharm/docker.html)
- **Workshop GitBook**: [https://idea-lab-1.gitbook.io/remote-development](https://idea-lab-1.gitbook.io/remote-development)

## License

This project is part of the Remote Development Workshop educational materials. Free to use and modify for learning purposes.

---

**Questions?** Open an issue on GitHub or consult the [workshop documentation](https://idea-lab-1.gitbook.io/remote-development).
