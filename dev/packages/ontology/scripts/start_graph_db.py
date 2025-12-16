"""Script to start GraphDB docker container."""

import docker
import time
import requests
from pathlib import Path


GRAPHDB_IMAGE = "ontotext/graphdb:latest"
CONTAINER_NAME = "graphdb-ontology"
REPOSITORY_ID = "llm-ontology"
DEFAULT_PORT = 7200


def wait_for_graphdb(url: str, timeout: int = 120) -> bool:
    """GraphDB가 시작될 때까지 대기.
    
    Args:
        url: GraphDB URL
        timeout: 최대 대기 시간 (초)
        
    Returns:
        시작 성공 여부
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/rest/repositories", timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(2)
    return False


def create_repository(url: str, repo_id: str) -> bool:
    """GraphDB에 repository 생성.
    
    Args:
        url: GraphDB URL
        repo_id: Repository ID
        
    Returns:
        생성 성공 여부
    """
    repo_config = {
        "id": repo_id,
        "title": repo_id,
        "type": "graphdb:FreeSailRepository"
    }
    
    try:
        response = requests.post(
            f"{url}/rest/repositories",
            json=repo_config,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        return response.status_code in [200, 201, 409]
    except requests.exceptions.RequestException as e:
        print(f"Repository 생성 실패: {e}")
        return False


def load_ttl_file(url: str, repo_id: str, ttl_path: str) -> bool:
    """TTL 파일을 GraphDB에 로드.
    
    Args:
        url: GraphDB URL
        repo_id: Repository ID
        ttl_path: TTL 파일 경로
        
    Returns:
        로드 성공 여부
    """
    ttl_file = Path(ttl_path)
    if not ttl_file.exists():
        print(f"TTL 파일을 찾을 수 없습니다: {ttl_path}")
        return False
    
    try:
        with open(ttl_file, 'rb') as f:
            response = requests.post(
                f"{url}/rest/repositories/{repo_id}/statements",
                data=f.read(),
                headers={
                    "Content-Type": "application/x-turtle"
                },
                timeout=60
            )
            if response.status_code in [200, 201, 204]:
                print(f"TTL 파일 로드 완료: {ttl_path}")
                return True
            else:
                print(f"TTL 파일 로드 실패: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"TTL 파일 로드 중 오류: {e}")
        return False


def start_graph_db(ttl_path: str, port: int = DEFAULT_PORT) -> None:
    """GraphDB 도커 컨테이너 시작.
    
    Args:
        ttl_path: TTL 파일 경로
        port: GraphDB 포트 (기본값: 7200)
    """
    ttl_file = Path(ttl_path)
    if not ttl_file.exists():
        raise FileNotFoundError(f"TTL file not found: {ttl_path}")

    client = docker.from_env()
    graphdb_url = f"http://localhost:{port}"

    # 기존 컨테이너 확인 및 제거
    try:
        existing_container = client.containers.get(CONTAINER_NAME)
        if existing_container.status == "running":
            print(f"기존 컨테이너가 실행 중입니다: {CONTAINER_NAME}")
            print(f"GraphDB URL: {graphdb_url}")
            return
        else:
            print(f"기존 컨테이너 제거 중: {CONTAINER_NAME}")
            existing_container.remove()
    except docker.errors.NotFound:
        pass

    # GraphDB 이미지 pull
    print(f"GraphDB 이미지 확인 중: {GRAPHDB_IMAGE}")
    try:
        client.images.get(GRAPHDB_IMAGE)
        print("이미지가 이미 존재합니다.")
    except docker.errors.ImageNotFound:
        print("이미지 pull 중...")
        client.images.pull(GRAPHDB_IMAGE)
        print("이미지 pull 완료")

    # 데이터 디렉토리 생성
    data_dir = Path.home() / ".graphdb" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # 컨테이너 시작
    print(f"GraphDB 컨테이너 시작 중...")
    container = client.containers.run(
        GRAPHDB_IMAGE,
        name=CONTAINER_NAME,
        ports={7200: port},
        volumes={
            str(data_dir): {"bind": "/opt/graphdb/home/data", "mode": "rw"}
        },
        environment={
            "GRAPHDB_OPTS": "-Xmx2g -Xms2g"
        },
        detach=True,
        remove=False
    )

    print(f"컨테이너 시작됨: {container.id[:12]}")
    print(f"GraphDB 시작 대기 중... (최대 2분)")

    # GraphDB 시작 대기
    if not wait_for_graphdb(graphdb_url):
        print("GraphDB 시작 실패: 타임아웃")
        container.stop()
        container.remove()
        return

    print("GraphDB 시작 완료")

    # Repository 생성
    print(f"Repository 생성 중: {REPOSITORY_ID}")
    if create_repository(graphdb_url, REPOSITORY_ID):
        print(f"Repository 생성 완료: {REPOSITORY_ID}")
    else:
        print(f"Repository 생성 실패 또는 이미 존재: {REPOSITORY_ID}")

    # TTL 파일 로드
    print(f"TTL 파일 로드 중: {ttl_path}")
    if load_ttl_file(graphdb_url, REPOSITORY_ID, ttl_path):
        print("TTL 파일 로드 완료")
    else:
        print("TTL 파일 로드 실패")

    print(f"\nGraphDB 실행 중:")
    print(f"  URL: {graphdb_url}")
    print(f"  Repository: {REPOSITORY_ID}")
    print(f"  SPARQL Endpoint: {graphdb_url}/repositories/{REPOSITORY_ID}")
    print(f"\n컨테이너 중지: docker stop {CONTAINER_NAME}")
    print(f"컨테이너 제거: docker rm {CONTAINER_NAME}")


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # 기본 TTL 파일 경로
    default_ttl_path = Path(__file__).parent.parent / "data" / "llm_ontology.ttl"

    if len(sys.argv) > 1:
        ttl_path = sys.argv[1]
    else:
        ttl_path = str(default_ttl_path)
        print(f"기본 TTL 파일 사용: {ttl_path}")

    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    start_graph_db(ttl_path, port)

