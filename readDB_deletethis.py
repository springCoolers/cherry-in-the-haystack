import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

from src.db.connection import get_session
from src.db.models import Book, ParagraphChunk, KeyIdea, ProcessingProgress

# 세션 생성
session = get_session()

try:
    # 쿼리 실행
    books = session.query(Book).all()
    for book in books:
        print(f"ID: {book.id}, Title: {book.title}")

finally:
    session.close()