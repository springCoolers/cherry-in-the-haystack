# Development Guide: API (Auto-News)

## Prerequisites

### System Requirements

- **OS**: Linux or macOS (Windows via WSL2)
- **CPU**: 2+ cores (8+ recommended)
- **Memory**: 6GB minimum (16GB recommended)
- **Disk**: 20GB minimum (100GB recommended)

### Required Software

- **Docker**: Latest version
- **Docker Compose**: Latest version
- **Make**: Build automation
- **Git**: Version control

### Optional for Kubernetes

- **kubectl**: Kubernetes CLI
- **Helm**: v3+
- **ArgoCD CLI**: For GitOps deployment

## Environment Setup

### 1. Clone Repository

```bash
cd dev/apps/api
```

### 2. Configure Environment Variables

Create environment file from template:

```bash
# Template will be copied automatically by make deps
# Located at: build/.env
```

**Required Environment Variables**:

```bash
# LLM Provider (choose one or more)
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
OLLAMA_BASE_URL=http://localhost:11434

# Notion Integration
NOTION_TOKEN=secret_...
NOTION_DATABASE_ID_INDEX_INBOX=...
NOTION_DATABASE_ID_INDEX_TOREAD=...

# Database Connections
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=...
MYSQL_DATABASE=auto_news

BOT_REDIS_URL=redis://redis:6379/0

# Milvus Vector DB
MILVUS_HOST=milvus
MILVUS_PORT=19530

# Optional: External APIs
TWITTER_BEARER_TOKEN=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
YOUTUBE_API_KEY=...
```

### 3. Install Dependencies

```bash
make deps
```

This command:
- Creates workspace directories
- Sets up build folder
- Generates `.env` file from template
- Prepares Docker network

## Local Development

### Build and Deploy

```bash
# Build Docker image
make build

# Deploy Airflow stack
make deploy

# Initialize databases
make init

# Start services
make start
```

### Access Services

- **Airflow UI**: http://localhost:8080
  - Username: `airflow`
  - Password: `airflow`

- **Adminer (DB UI)**: http://localhost:8070

### Common Commands

```bash
# View logs
make logs

# Check service status
make ps

# Stop services
make stop

# Clean up
make clean

# Run tests
make test

# Push DAGs to running instance
make push_dags

# Enable DAGs
make enable_dags
```

## Development Workflow

### 1. Modify Source Code

Source files located in:
- `src/*.py` - Core application logic
- `dags/*.py` - Airflow DAG definitions

### 2. Rebuild and Redeploy

```bash
# Rebuild Docker image
make build

# Deploy changes
make deploy

# Push updated DAGs
make push_dags
```

### 3. Test Changes

- Monitor Airflow UI for DAG execution
- Check task logs for errors
- Verify output in Notion workspace

## Project Structure

```
dev/apps/api/
├── src/                 # Source code
│   ├── af_*.py          # Airflow task operators
│   ├── ops_*.py         # Core operators
│   ├── llm_*.py         # LLM integration
│   ├── embedding_*.py   # Embedding providers
│   └── *_cli.py         # Database clients
├── dags/                # Airflow DAGs
├── docker/              # Docker configuration
├── helm/                # Kubernetes Helm charts
├── Makefile             # Build automation
└── pyproject.toml       # Python dependencies
```

## Adding New Content Sources

### 1. Create Operator

Create `src/ops_newsource.py`:

```python
from ops_base import OperatorBase

class OperatorNewSource(OperatorBase):
    def pull(self):
        # Fetch from source
        pass

    def dedup(self, pages):
        # Deduplicate
        pass

    def summarize(self, pages):
        # LLM summarization
        pass

    def publish(self, pages):
        # Publish to Notion
        pass
```

### 2. Create Airflow Operators

Create `src/af_newsource_pull.py`, `af_newsource_save.py`

### 3. Create DAG

Create `dags/newsource_pulling.py`:

```python
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG('newsource_pulling', ...) as dag:
    pull = BashOperator(
        task_id='pull',
        bash_command='python3 af_newsource_pull.py'
    )
```

### 4. Deploy

```bash
make build
make deploy
make push_dags
make enable_dags
```

## Debugging

### View Airflow Logs

```bash
# All services
make logs

# Specific service
docker logs auto-news-airflow-webserver
```

### Access Airflow Container

```bash
docker exec -it auto-news-airflow-worker bash
cd ~/airflow/run/auto-news/src
python3 af_pull.py --help
```

### Database Access

Via Adminer UI: http://localhost:8070

Or via CLI:

```bash
# MySQL
docker exec -it auto-news-mysql mysql -u root -p

# Redis
docker exec -it auto-news-redis redis-cli
```

## Testing

### Unit Tests

```bash
cd src
python3 -m pytest tests/
```

### Integration Tests

Run full DAG in Airflow UI:
1. Navigate to http://localhost:8080
2. Enable DAG
3. Trigger manually
4. Monitor execution
5. Check Notion for output

### LLM Testing

Test LLM integration:

```bash
cd src
python3 -c "from llm_agent import LLMAgentSummary; agent = LLMAgentSummary(); print(agent.summarize('test text'))"
```

## Troubleshooting

### Airflow Not Starting

```bash
# Check logs
make logs

# Reinitialize
make clean
make deps
make build
make deploy
make init
make start
```

### DAG Not Appearing

```bash
# Ensure DAG is valid Python
python3 dags/your_dag.py

# Push DAGs
make push_dags

# Restart scheduler
docker restart auto-news-airflow-scheduler
```

### Database Connection Issues

Check environment variables in `build/.env`:
- MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD
- BOT_REDIS_URL
- MILVUS_HOST, MILVUS_PORT

### LLM API Errors

- Verify API keys in `.env`
- Check rate limits
- Monitor API usage

## Kubernetes Development

### Build for K8s

```bash
# Build and tag
make k8s-docker-build repo=your-repo tag=0.1.0

# Push to registry
make k8s-docker-push repo=your-repo tag=0.1.0
```

### Deploy to K8s

```bash
# Create namespace
make k8s-namespace-create

# Create secrets
make k8s-secret-create

# Install via Helm
make k8s-helm-install

# Enable DAGs
make k8s-airflow-dags-enable
```

### Access K8s Services

```bash
# Port forward Airflow
kubectl port-forward service/auto-news-webserver 8080:8080 -n auto-news

# Port forward Milvus UI
kubectl port-forward service/auto-news-milvus-attu 9100:3001 -n auto-news
```

## Code Style

### Python

- Follow PEP 8
- Use type hints where possible
- Document functions and classes
- Keep functions focused and small

### Naming Conventions

- `af_*.py`: Airflow task operators
- `ops_*.py`: Core business logic operators
- `llm_*.py`: LLM-related modules
- `embedding_*.py`: Embedding providers
- `*_cli.py`: Database/service clients

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-source

# Make changes
# ... edit files ...

# Commit
git add .
git commit -m "Add new source integration"

# Push
git push origin feature/new-source

# Create PR on GitHub
```

## Performance Optimization

### Caching

- Use Redis caching for embeddings (4-week TTL)
- Cache LLM responses when possible (2-week TTL)
- Implement deduplication early in pipeline

### Batch Processing

- Process items in batches
- Use Airflow parallelism settings
- Optimize database queries

### Resource Limits

Configure in `helm/values.yaml`:

```yaml
resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 500m
    memory: 1Gi
```

## Documentation

### Code Documentation

- Docstrings for all public functions/classes
- Inline comments for complex logic
- README for each major component

### Update Documentation

When making significant changes:
1. Update inline docstrings
2. Update README if needed
3. Update architecture docs if architecture changes
4. Update this development guide

## Getting Help

- **Project Wiki**: https://github.com/finaldie/auto-news/wiki
- **GitHub Issues**: https://github.com/finaldie/auto-news/issues
- **Original README**: `dev/apps/api/README.md`

## Next Steps

1. Review [Architecture Documentation](./architecture-api.md) for system design
2. Explore [Source Tree Analysis](./source-tree-analysis.md) for codebase navigation
3. Check [Data Models](./data-models-api.md) for database schemas
4. See [Project Overview](./project-overview.md) for high-level context
