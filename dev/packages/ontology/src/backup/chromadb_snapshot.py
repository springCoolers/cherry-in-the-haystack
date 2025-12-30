"""ChromaDB snapshot management utilities."""

import tarfile
from pathlib import Path
from datetime import datetime
from typing import Optional


def create_snapshot(
    db_path: str,
    snapshot_dir: str = "snapshots",
    version: Optional[int] = None
) -> str:
    """ChromaDB를 tar.gz로 압축하여 스냅샷 저장.
    
    Args:
        db_path: ChromaDB 디렉토리 경로
        snapshot_dir: 스냅샷 저장 디렉토리
        version: 버전 번호 (None이면 자동 증가)
        
    Returns:
        생성된 스냅샷 파일 경로
    """
    db_path_obj = Path(db_path)
    snapshot_path = Path(snapshot_dir)
    snapshot_path.mkdir(parents=True, exist_ok=True)
    
    if not db_path_obj.exists():
        raise FileNotFoundError(f"ChromaDB path not found: {db_path}")
    
    if version is None:
        version = get_next_version(snapshot_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chromadb_v{version}_{timestamp}.tar.gz"
    snapshot_file = snapshot_path / filename
    
    print(f"ChromaDB 스냅샷 생성 중: {snapshot_file}")
    
    with tarfile.open(snapshot_file, "w:gz") as tar:
        tar.add(db_path, arcname=db_path_obj.name)
    
    print(f"스냅샷 생성 완료: {snapshot_file}")
    print(f"파일 크기: {snapshot_file.stat().st_size / (1024*1024):.2f} MB")
    
    cleanup_old_snapshots(snapshot_dir, keep=10)
    
    return str(snapshot_file)


def get_next_version(snapshot_dir: str) -> int:
    """다음 버전 번호 계산.
    
    Args:
        snapshot_dir: 스냅샷 디렉토리 경로
        
    Returns:
        다음 버전 번호
    """
    snapshot_path = Path(snapshot_dir)
    
    if not snapshot_path.exists():
        return 1
    
    snapshot_files = list(snapshot_path.glob("chromadb_v*.tar.gz"))
    
    if not snapshot_files:
        return 1
    
    max_version = 0
    for file in snapshot_files:
        try:
            version_str = file.stem.split("_")[1].replace("v", "")
            version = int(version_str)
            max_version = max(max_version, version)
        except (IndexError, ValueError):
            continue
    
    return max_version + 1


def cleanup_old_snapshots(snapshot_dir: str, keep: int = 10) -> None:
    """오래된 스냅샷 파일 정리.
    
    Args:
        snapshot_dir: 스냅샷 디렉토리 경로
        keep: 유지할 스냅샷 개수
    """
    snapshot_path = Path(snapshot_dir)
    
    if not snapshot_path.exists():
        return
    
    snapshot_files = sorted(
        snapshot_path.glob("chromadb_v*.tar.gz"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    for old_file in snapshot_files[keep:]:
        print(f"오래된 스냅샷 삭제: {old_file}")
        old_file.unlink()


def restore_snapshot(snapshot_file: str, target_path: str) -> None:
    """스냅샷에서 ChromaDB 복원.
    
    Args:
        snapshot_file: 스냅샷 파일 경로
        target_path: 복원할 디렉토리 경로
    """
    snapshot_file_obj = Path(snapshot_file)
    target_path_obj = Path(target_path)
    
    if not snapshot_file_obj.exists():
        raise FileNotFoundError(f"Snapshot file not found: {snapshot_file}")
    
    print(f"ChromaDB 복원 중: {snapshot_file} -> {target_path}")
    
    if target_path_obj.exists():
        import shutil
        print(f"기존 디렉토리 제거: {target_path}")
        shutil.rmtree(target_path)
    
    target_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    with tarfile.open(snapshot_file, "r:gz") as tar:
        tar.extractall(path=target_path_obj.parent)
    
    print(f"복원 완료: {target_path}")


def list_snapshots(snapshot_dir: str = "snapshots") -> list:
    """스냅샷 목록 조회.
    
    Args:
        snapshot_dir: 스냅샷 디렉토리 경로
        
    Returns:
        스냅샷 정보 리스트
    """
    snapshot_path = Path(snapshot_dir)
    
    if not snapshot_path.exists():
        return []
    
    snapshot_files = sorted(
        snapshot_path.glob("chromadb_v*.tar.gz"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    snapshots = []
    for file in snapshot_files:
        snapshots.append({
            "filename": file.name,
            "path": str(file),
            "size_mb": file.stat().st_size / (1024*1024),
            "created": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return snapshots

