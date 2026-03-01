# DB 설계 제안 - auto-news 벤치마킹

Created: September 30, 2025 7:04 PM
Tags: Product Spec
Hide: No
체크 표시됨: No

### DB의 조건

1. 처음에는 일단 간단하게 만들어보져 
2. 나중에는 linkedin, twitter, youtube 등이 있어야 하고, 이것들과 호환 할 생각을 설계 단계에 하긴 해야 합니다. 
3. 원문 그대로를 저장한 후 파싱합시다 (성민님 제안) 

---

### 내용 정리

### 현재 DB 구조

- 영상님 문의 결과, 현재 사용하고 있는 데이터베이스는 있으나 스키마가 정리되어있지 않음. 그럼 이참에 다시 만들어도 되긴 할듯.

### 오토뉴스 참고

[워크플로우]

1. 다양한 콘텐츠에서 데이터 수집
    - 이 결과물은 DB가 아닌 json 파일로 저장함.
    - RSS
        
        ```json
        {
          "md5_article_id_1": {
            "id": "md5_article_id" -> "{list_name}_{title}_{published_date}" 로 생성,
            "source": "RSS",
            "list_name": "TechCrunch",
            "title": "기사 제목",
            "url": "https://...",
            "created_time": "2025-10-10T12:00:00",
            "published": "Thu, 03 Mar 2022 08:00:00 GMT",
            "published_key": "2022-03-03"
          },
          ...
        }
        ```
        
    - Reddit
        
        ```json
        {
          "MachineLearning": [
            {
              "hash_id": "md5_hash",
              "long_id": "reddit_post_id",
              "title": "포스트 제목",
              "text": "포스트 본문",
              "url": "https://reddit.com/...",
              "permalink": "/r/subreddit/...",
              "is_video": True,
              "is_image": False,
              "is_gallery": False,
              "is_external_link": False,
              "video": {
                "video_url": "https://..."
              },
              "gallery_medias": []
            },
            ...
          ]
        }
        ```
        
    - Twitter
        
        ```json
        {
          "AI_list": [
            {
              "tweet_id": "123456789",
              "name": "@username",
              "text": "트윗 내용",
              "created_at_pdt": "2025-10-10T12:00:00",
              "url": "https://twitter.com/...",
              "reply_to_name": "@reply_user",
              "reply_text": "답글 내용",
              "reply_url": "...",
              "reply_deleted": False,
              "retweeted": False,
              "embed": "임베드 URL",
              "user_desc": "사용자 설명",
              "reply_user_desc": "답글 사용자 설명"
            },
            ...
          ]
        }
        ```
        
    - 유튜브
        - 자막을 LLM으로 요약
        
        ```json
        {
          "notion_page_id_1": {
            "id": "notion_page_id",
            "title": "제목",
            "source_url": "https://youtube.com/watch?v=...",
            "created_time": "2025-10-10T12:00:00",
            "__transcript": "자막 전체 텍스트",
            "__title": "실제 영상 제목",
            "__description": "영상 설명",
            "__thumbnail_url": "썸네일 URL",
            "__publish_date": "2025-10-01T00:00:00",
            "__author": "채널명",
            "__view_count": 123456,
            "__length": 600  # 초 단위
          },
          ...
        }
        ```
        
2. AI를 통한 필터링 
    - 콘텐츠의 품질과 관련성을 AI로 평가하여 선별
    - 기본 로직
        - **LLM 기반 품질 평가**: GPT를 사용해 콘텐츠를 0-1 점수로 평가
        - **관련성 점수 계산**: 유사한 기존 콘텐츠들의 사용자 평점 평균
        - **최종 점수**: 사용자 평점 × 0.8 + 관련성 점수 × 0.2
        - **임계값 필터링**: 최소 점수 이상의 콘텐츠만 선별
3. 중복 제거 및 유사도 검색
    - 동일하거나 매우 유사한 콘텐츠를 제거하고 관련 콘텐츠를 찾음
    - 데이터 베이스 기반
        - **데이터베이스 기반**: 기존에 저장된 콘텐츠와 page_id 비교
        - **사용자 평점 업데이트**: 중복이지만 평점이 변경된 경우 업데이트 큐에 추가
    - 벡터 검색 기반
        - **임베딩 기반**: Milvus 벡터 DB에서 의미적 유사도 검색
        - **거리 임계값**: max_distance 설정으로 유사도 기준 조절
        - **메트릭 타입**: L2, Cosine 등 다양한 거리 계산 방식 지원
4. 개인화된 콘텐츠 큐레이션
    - **콘텐츠 분류 및 태깅**
        - **토픽 추출**: LLM이 콘텐츠에서 주요 토픽과 카테고리 자동 추출
        - **태그 시스템**: Notion의 태그 시스템과 연동하여 콘텐츠 분류
        - **관심사 기반 큐레이션**: 사용자의 관심 토픽과 카테고리 기반 선별
    - **시간 기반 큐레이션**
        - **주간/월간 컬렉션**: 시간대별로 콘텐츠를 그룹화하여 큐레이션
        - **최신성 고려**: 최근 1주일간의 콘텐츠를 우선적으로 선별
        - **Takeaway 페이지**: 사용자가 중요하게 표시한 콘텐츠 우선 포함
    - 가공 후 추가되는 데이터
        - 이 부분을 최종적으로 노션 데이터베이스에 올린다.
        
        ```json
        {
          # ... 원본 필드들 ...
          "__summary": "LLM 생성 요약",
          "__topics": [("AI", 0.9), ("ML", 0.8)],  # (토픽, 점수)
          "__categories": [("Technology", 0.95)],  # (카테고리, 점수)
          "__rate": 0.85,  # 0~1 사이 점수
          "__feedback": "LLM 피드백",
          "__relevant_score": 4.5  # Milvus 관련성 점수
        }
        ```
        
    
    ```json
    {
      # ... 원본 필드들 ...
      "__extracted": {
    	  "insight or topic": ["뫄뫄"], 
    	  "supporting evidences" : ["글감 1", "글감 2"], 
    	  "tool name" : "midjourney" # 툴을 소개하는 글일 경우, midjourney에 대해 다뤘다는 걸 알려주는 필드 
    	  "top use" : "이미지 생성"  
    	  
    	  },
    
    }
    ```
    
5. Notion에 저장
    - 공통 필드
        - blocks에 해당하는 부분을 이어붙여서 벡터디비에 저장함.
        
        ```json
        Properties (데이터베이스 컬럼):
        ├─ Name (title)              : 제목
        ├─ Source (select)           : "Twitter", "Reddit", "RSS", "Youtube", "Article"
        ├─ Created at (date)         : 생성일시
        ├─ Topic (multi_select)      : ["AI", "ML", ...] (Top-3)
        ├─ Category (multi_select)   : ["Technology", ...] (Top-3)
        ├─ Rating (number)           : LLM 평점 (0~100)
        └─ Relevant Score (number)   : Milvus 관련성 점수 (0~10)
        
        Blocks (페이지 본문 내용):
        - Summary (paragraph)
        - 소스별로 다른 추가 블록
        ```
        
    - RSS 전용 필드
        
        ```json
        Properties:
        └─ List Name (multi_select) : ["TechCrunch", "Hacker News"]
        
        Blocks:
        ├─ Summary (paragraph)
        └─ Link                    : 원본 기사 링크
        ```
        
    - Reddit 전용필드
        
        ```json
        Properties:
        └─ List Name (multi_select) : ["MachineLearning", "programming"]
        
        Blocks:
        ├─ Summary (paragraph)
        ├─ Video block             : is_video=True일 때
        ├─ Image block             : is_image=True일 때
        ├─ Gallery images          : is_gallery=True일 때
        ├─ Embed block             : 외부 링크
        └─ Link                    : Reddit 포스트 링크
        ```
        
    - 트위터 전용 필드
        
        ```json
        Properties:
        ├─ To (rich_text)           : 답글 대상 (@username)
        ├─ List Name (multi_select) : ["AI_list", "Tech_list"]
        
        Blocks:
        ├─ Quote block              : 답글 원본 트윗
        ├─ Embed block              : 임베드 콘텐츠
        ├─ Paragraph               : "@username: 트윗 내용"
        └─ Link                    : 원본 트윗 링크
        
        Comments:
        - 사용자 프로필 설명
        - 답글 사용자 프로필 설명
        ```
        
    - 유튜브 전용 필드
        
        ```json
        Blocks:
        ├─ Summary (paragraph)
        ├─ Translation (toggle)    : 요약 번역 (있는 경우)
        └─ Video block             : 임베드된 유튜브 영상
        
        Comments:
        - Author: 채널명
        - Description: 영상 설명
        - Publishing date: 발행일
        - Duration: N 분
        - View count: 조회수
        ```
        

[DB 구조]

1. **PostgreSQL - Airflow 메타데이터 관리**
    - DAG 실행 기록 (dag_run 테이블)
    - 태스크 실행 상태 (task_instance 테이블)
    - 연결 정보 (connection 테이블)
    - 변수 정보 (variable 테이블)
2. **MySQL - 애플리케이션 메타데이터**
    - patch 테이블: 시스템 패치 관리
    - index_pages 테이블: Notion 데이터베이스 인덱스
3. **Redis - 캐시 및 중복 제거**
    - 중복 처리 방지 플래그
    - 임시 캐시 데이터
    - 사용자 평점 정보
    - LLM 응답 캐시 (2주 TTL)
4. **Milvus - 벡터 검색 및 유사도 계산**
    - 문서 임베딩 벡터 (1536차원)
    - 아이템 ID
    - 유사도 검색 인덱스

### DB 구조 제안

- 정확한 설계안이 나와야 (어떤 소스를 가져오고 소스에서 어떤걸 보여줄건지 화면이 있는게 베스트) 이에 따라 설계할 수 있긴 함.
    - 정해야하는 것
        1. 어떤 출처를 가지고 올건지
        2. 각 출처에서 어떤 정보를 파싱해올건지
        3. 가저온 출처에서 LLM을 통해 추출하고자 하는 것은 뭔지 (요약, 주제 등)
        4. 추가적으로 저장하고 싶은 데이터 있는지 (조회수, 지식팀 점수 등)조
- 기존에도 노션 쓰고 있었으니까 노션이 나을듯.
    - 다양한 UI는 못함 (대시보드랄지…)
    - 미리 정보를 다 저장해야되고 DB를 바로 붙여서 쓸수가 없음..
- 대신에 노션을 쓰더라도 나중에 마이그레이션을 위해 **DB**를 하나두고 백업용으로 사용하기.
    - 나중에 노션 안쓸때 해당 DB만 연동할 수 있도록.
    - 그리고 노션 데이터 자체도 이중화해서 저장이 필요하니까
- RDBMS + VectorDB + Notion으로 시작
    - RDBMS의 경우 Postgresql 사용 (jsonb 필드를 사용하기 좋음 - 자유도 높음)
        - 테이블 (AI의 도움을 받아 필드 예시를 적었고, 이 중에서 꼭 필요한 것만 골라야함. 복잡하다고 생각되면 processed_data, document 둘중 하나만 쓰고, contents_extracts, user_content 둘 중 하나만 쓰기)
            - raw_data
                - 역할: 수집한 그대로 저장
                목적: 백업, 재처리, 디버깅
                접근: 개발자만
                - 보관 기간: 일단 다 저장한다 ~~보통 30~90일 (오래된 건 삭제)~~
                - 필드
                    
                    ```json
                    식별:
                    - id (Primary Key)
                    - run_id (어느 실행에서 수집했는지)
                    - source (twitter, reddit, rss, youtube, article)
                    - item_id (소스의 고유 ID, 예: tweet_id, post_id)
                    
                    상태:
                    - status (raw, processing, completed, failed)
                    - created_at (수집 시각)
                    - processed_at (처리 시각)
                    - error_message (실패 시 에러)
                    
                    데이터:
                    - data ~~(JSONB)~~ ← 원본 데이터 전체 (구조가 소스마다 다름)
                    	- html, 
                    	- url, 
                    	- source
                    	... 
                    	 
                      • Twitter:  ~~{tweet_id, name, text, reply_text, embed, ...~~}
                      • Reddit: ~~{post_id, title, text, subreddit, is_video, ...}~~
                      • YouTube: ~~{video_id, title, transcript, duration, ...}~~
                    ```
                    
            - **processed_data (postgres 현재 syncdb와 같은 것)**
                - 역할: 파이프라인 처리 결과
                목적: 필터링, 점수 계산, 요약 생성
                접근: 개발자/내부 시스템
                - 보관 기간: 30~90일 (분석 후 삭제 가능)
                - 필드
                    
                    ```json
                    연결:
                    - id (Primary Key)
                    - run_id
                    - source
                    - item_id
                    - raw_data_id (원본 참조)
                    
                    파이프라인 상태:
                    - status (processing, completed, filtered_out, failed)
                    - processed_at
                    - error_message
                    
                    가공 결과:
                    - relevant_score (Milvus 유사도 점수, 예: 4.5)
                    - summary (LLM이 생성한 요약)
                    - topics (분류된 토픽들, 예: ["AI", "Machine Learning"])
                    - categories (카테고리, 예: ["Technology", "Research"])
                    - rating (LLM 평가 점수, 0~100)
                    - feedback (LLM 피드백 텍스트)
                    
                    메타:
                    - created_at
                    - updated_at
                    ```
                    
            - **documents**
                - 역할: 하나의 완전한 문서, 발췌 대상의 부모 역할
                    
                    목적: 완전한 문서 단위 영구 보관용, processed_data에서 게시용으로 최종 선별된 것만 저장. 
                    
                    접근: 시스템
                    
                - 보관 기간: 영구 보관
                - 필드
                    
                    ```json
                    식별:
                    - id (Primary Key)
                    - source (출처)
                    - source_id (소스의 원본 ID)
                    - source_url (원본 링크, 중복 체크용)
                    - processed_data_id
                    
                    문서 정보:
                    - title (제목)
                    - author (작성자)
                    - published_at (원본 발행일)
                    
                    콘텐츠:
                    - full_content (전체 내용, 텍스트)
                    - full_content_type (text, html, markdown)
                    - structured_content (JSONB) ← 구조화된 데이터
                      • YouTube: 챕터 정보
                      • 기사: 섹션 구조
                      • Reddit: 댓글 트리
                    
                    메타데이터:
                    - duration (영상/오디오 길이, 초)
                    - word_count (단어 수)
                    - language (언어)
                    - thumbnail_url (썸네일)
                    
                    처리 상태:
                    - processing_status (raw, extracting, completed)
                    
                    시간:
                    - created_at
                    - updated_at
                    ```
                    
            - contents_extracts
                - 역할: 문서에서 발췌한 부분. 전체 문서도 하나의 extraction으로 저장 가능
                    
                    목적: 최종적으로 게시하는 단위
                    
                    접근: 시스템 내부
                    
                - 보관 기간: 영구 보관
                    
                    ```json
                    연결:
                    - id (Primary Key)
                    - document_id (부모 문서)
                    
                    발췌 유형:
                    - extract_type
                      • 'full': 전체 문서
                      • 개념어
                      • 실험결과
                      • 조언
                      • 미래 전망
                      • 핵심 주장
                    
                    위치 (소스에 따라 다름):
                    - start_position, end_position (글자 위치)
                      → 기사, 포스트에 사용
                    - start_time, end_time (초 단위)
                      → YouTube, 오디오에 사용
                    
                    내용:
                    - title (발췌의 제목, 예: "AI란 무엇인가")
                    - content (발췌된 텍스트)
                    - content_type (text, html, markdown)
                    
                    AI 처리:
                    - summary (발췌 부분의 요약)
                    - key_points (핵심 포인트들, 배열)
                    - topics (관련 토픽)
                    - categories (카테고리)
                    
                    품질:
                    - importance_score (중요도, 0~5)
                      → LLM이 평가
                      → 높을수록 중요
                    - relevance_score (관련성)
                    
                    메타:
                    - language
                    - word_count
                    - created_at
                    ```
                    
            - **user_content**
                - 역할: 사용자에게 보여줄 콘텐츠 - 최종 가공본과 서비스에서 제공하는 데이터를 분리하기 위함. 사용자 인터렉션 정보 추가 (조회수 등)
                목적: API/웹/앱 서비스 - 일단 이 결과물을  notion db와 연동하기 (노션 백업용)
                접근: 모든 사용자
                - 필드
                    
                    ```json
                    연결:
                    - id (Primary Key)
                    - document_id (원본 문서)
                    - extract_id (발췌, NULL이면 전체 문서)
                    
                    표시 정보:
                    - display_title (사용자에게 보이는 제목)
                      예: "AI란 무엇인가 (5분 핵심)"
                    - display_summary (한 줄 요약)
                    - thumbnail_url (썸네일 이미지)
                    
                    콘텐츠 유형:
                    - content_type
                      • 'article': 기사 전체
                      • 'video_full': 영상 전체
                      • 'video_clip': 영상 클립
                      • 'tweet': 트윗
                      • 'post': 포스트 전체
                      • 'highlight': 발췌 하이라이트
                    
                    메타데이터:
                    - topics (배열)
                    - categories (배열)
                    - tags (해시태그)
                    - difficulty_level (beginner, intermediate, advanced)
                    - estimated_time (읽는데 걸리는 시간, 초)
                    
                    품질:
                    - quality_score (내부 평가 점수)
                    - relevance_score (관련성)
                    
                    발행 상태:
                    - status (draft, published, archived, hidden)
                    - published_at (발행 시각)
                    - featured (추천 콘텐츠 여부, true/false)
                    - trending (인기 콘텐츠 여부, true/false)
                    
                    사용자 인터랙션:
                    - view_count (조회수)
                    - like_count (좋아요)
                    - bookmark_count (북마크)
                    - share_count (공유)
                    - comment_count (댓글, 있다면)
                    - user_rating_avg (사용자 평점 평균)
                    
                    검색:
                    - search_vector (전문 검색용 벡터)
                    
                    시간:
                    - created_at (생성일)
                    - updated_at (수정일)
                    - last_viewed_at (마지막 조회)
                    ```
                    
    - (창진) 각 테이블의 역할을 요약하면 이렇게 되나요?
        - raw_data
            - 수집된 raw data (HTML)이 저장되는 테이블
            - 압축이 잘 되야 비용 절약
        - processed_data
            - notion과 싱크되는 부분
            - raw_data 또는 documents 바탕으로 LLM이 추출한 정보들 포함 (tag, category...)
            - notion에서 지식팀이 평가한 평가 점수 등이 반영됨
        - documents
            - raw_data를 바탕으로 parse된 clean text 및 구조화된 데이터
        - contents_extracts (다소 애매?)
            - 문서에서 발췌한 부분??
            - (질문) 문서(아티클) 1개에서 여러 정보를 추출 가능할 경우 1:N으로 여러 extracts가 생성 가능한 구조인지? → 맞다면 노션에서 평가하는 단계 전에 추출되어야 할 것 같아요. 아니면 해당 단계에서 수동으로 작성
        - user_content
            - 사용자에게 보여줄 콘텐츠 - 최종 가공본과 서비스에서 제공하는 데이터를 분리하기 위함. 사용자 인터렉션 정보 추가 (조회수 등)
    - 현재 단계에서 워크플로우는 이렇게 되는건가요?
        
        ```mermaid
        flowchart TD
            A[TTRSS] -->|데이터 수집| B(raw_data)
            B --> |HTML 파싱| D(documents)
            D --> |중복 제거, LLM Extract| C(processed_data)
            E[Notion] <--> |sync| C
            C -->|평가 통과| F(user_content, contents_extracts)
        ```
        
    - 유사한 문서 검색이나 중복 제거 위해서 벡터디비 필요
        
        

## 무엇을 추출해야 할까

- DB - json to extract #1 0 **crawling Sebastian Raschka’s Substack RSS feed** - 성준
    
    Perfect — since your goal is to **crawl Sebastian Raschka’s Substack RSS feed** to collect and structure information useful for making an **“LLM Handbook for Engineers”**, we’ll design a **specialized JSON schema** focused on **LLM research, engineering practice, benchmarks, tools, and open-source tech**.
    
    Below is the optimized **field definition (JSON structure)** + **rationale per field** for extraction.
    
    ---
    
    ## 🧠 Context
    
    **Source:** `https://magazine.sebastianraschka.com/feed`
    
    **Crawl method:** RSS feed (with optional HTML expansion for full content)
    
    **Purpose:** Build a structured dataset of technical knowledge (LLMs, MLOps, benchmarks, SOTA methods, open tools, productivity frameworks) for later merging, deduplication, and topic clustering.
    
    ---
    
    ## 📘 JSON Schema — Optimized for “LLM Handbook for Engineers”
    
    ```json
    {
      "llm_related_features": {
        "architecture": {
          "model_name": "string",                  // e.g., LLaMA 3, Mistral, GPT-4
          "architecture_type": "Decoder | Encoder | Mixture-of-Experts | Diffusion-Transformer",
          "parameters_billion": "float",
          "training_data": "string",
          "training_framework": "PyTorch | JAX | DeepSpeed | Megatron",
          "tokenizer_type": "BPE | SentencePiece | tiktoken"
        },
    
        "benchmarks": {
          "datasets": ["MMLU", "ARC", "GSM8K", "BBH"],
          "metrics": [
            {
              "metric_name": "Accuracy | F1 | BLEU | WinRate",
              "value": "float"
            }
          ],
          "comparison_models": ["GPT-4", "Claude 3", "Gemma 2"],
          "hardware_spec": "A100 | H100 | TPUv5e",
          "evaluation_framework": "EvalPlus | lm-eval-harness | HELM"
        },
    
        "sota_summary": {
          "paper_title": "string",
          "conference": "ICLR | NeurIPS | arXiv",
          "publication_date": "YYYY-MM-DD",
          "main_contribution": "string",
          "limitations": "string"
        },
    
        "tools_and_frameworks": {
          "category": "Fine-tuning | Deployment | Quantization | Evaluation",
          "tool_name": "string",
          "repo_url": "string",
          "key_features": ["string"],
          "integration_example": "string"
        },
    
        "productivity_and_workflows": {
          "category": "Prompt Engineering | Experiment Tracking | Data Cleaning",
          "tools": ["Weights & Biases", "LangSmith", "PromptLayer"],
          "methods": ["RAG optimization", "agent orchestration", "prompt tuning"],
          "recommended_pipelines": "string"
        }
      },
    }
    
    ```
    
    ---
    
    ## 🧩 Key Extraction Strategy
    
    | Field Group | How to Extract | Libraries / Techniques |
    | --- | --- | --- |
    | `metadata` | Direct from RSS (`entry.title`, `entry.link`, `entry.published`, etc.) | `feedparser`, `dateutil` |
    | `content.text` | Fetch `entry.link` → extract main body text | `newspaper3k`, `trafilatura`, `BeautifulSoup` |
    | `keywords` | Auto-extraction via TF-IDF, KeyBERT, or RAKE | `keybert`, `spacy`, `nltk` |
    | `architecture`, `benchmarks`, etc. | NLP-based entity extraction (NER/custom patterns for “LLM”, “GPT”, “Mistral”, “eval”) | `spacy`, regex rules, OpenAI embeddings |
    | `tools_and_frameworks` | Identify GitHub or PyPI links | regex `https://github.com/` / `/pypi.org/` |
    | `sentiment`, `tone` | Lightweight classification | `transformers` sentiment pipeline |
    | `relevance_score` | Cosine similarity to embedding vector of `"LLM engineering handbook topics"` | `sentence-transformers` |
    
    ---
    
    ## 💡 Example (Populated)
    
    ```json
    {
      "llm_related_features": {
        "architecture": {
          "model_name": "LLaMA 3",
          "architecture_type": "Decoder",
          "parameters_billion": 70,
          "training_framework": "PyTorch + FSDP"
        },
        "benchmarks": {
          "datasets": ["MMLU", "GSM8K"],
          "metrics": [
            {"metric_name": "Accuracy", "value": 0.84}
          ],
          "comparison_models": ["GPT-4", "Claude 3"]
        },
        "tools_and_frameworks": {
          "category": "Fine-tuning",
          "tool_name": "LoRA",
          "repo_url": "https://github.com/microsoft/LoRA",
          "key_features": ["parameter-efficient tuning"]
        }
      },
    
    }
    
    ```
    
    ---
    
    Would you like me to now provide a **Python script template** that:
    
    - Parses the RSS feed,
    - Extracts these fields (with placeholder analyzers),
    - And outputs `.jsonl` structured data for merging into your “LLM Handbook” corpus?
- DB
    - **핵심 메타데이터:** 글ID, 제목, 저자(예: **Nathan Lambert**), 공동저자(예: **Florian Brand**), 발행일, 출처 도메인(예: **interconnects.ai**), 섹션/시리즈(예: Artifacts Log, 랭킹 등), 오디오/비디오 유무, 접근 레벨(무료/유료), 글 종류(에세이/리뷰/랭킹/논평).
    - **주요 개념어(키워드):** AI 2027, RE(Research Engineer) 자동화, **reasoning models**, **thinking/searching/acting**, **continual learning**, **agentic app**, **open models**, 중국 오픈모델 생태계, GRPO, ARC-AGI, MCP/ACP, long-context, inference-time scaling 등.
    - **핵심 주장(스탠스):** 글 단위의 요지(문장), 스탠스 라벨(찬성/반대/중립), 강도(1–5), 근거 요약.
    예: “RE 완전 자동화는 3–7년 내 일부 달성되나 인간+툴 페어링을 능가해야 진정한 자동화이며, **특이점은 가깝지 않다**.”
    - **타임라인·예측:** 연·분기·구간(예: 1–3년/3–4년/2026/2027), 사건·이정표(예: 1GW 데이터센터 **2026 중반**, 쇼핑 에이전트 **2025-09**, 로컬 Sora2류 **~2년**), 불확실성 범위(낮음/중간/높음).
    - **인물·조직·지리 엔티티:** 인물(예: **Dwarkesh Patel**, **Francois Chollet**, **Li Qiang**), 연구기관/랩(예: **DeepSeek**, **Qwen**, **Zhipu**, **Shanghai AI Lab**), 기업(예: **OpenAI**, **Anthropic**, **Stripe**, **Shopify**), 국가·도시(중국, 베이징, 미국, 버클리, 몬트리올).
    - **모델·제품·프로토콜:** 모델명·버전(예: **DeepSeek V3/R1**, **Qwen 3**, **GLM 4.5**, **o3**, **GPT‑5 Thinking/Pro**, **Claude 4.5 Sonnet**), 모달리티(VLM/비디오/오디오), 라이선스(오픈/제한), 툴·프로토콜(예: **MCP**, **ACP**), 에이전트(코딩 에이전트, 웹 에이전트, 쇼핑 에이전트).
    - **기술 프리미티브·방법:**
        - Reasoning: **Thinking**(CoT/trace), **Searching**(비정규/검색 인덱스), **Acting**(코드 실행/로보틱스).
        - 학습·추론: RL(예: **GRPO**), hybrid attention, long-context(400K–1M+), inference-time scaling, toolformer류 설계.
        - 시스템: 메모리 기능, 커넥터/리트리벌, 병렬 추론, 에이전틱 워크플로.
    - **수치·자원(컴퓨트·토크노믹스):** FLOPs(예: **4e27**), 데이터센터 규모(예: **1GW**, 칩 **40–50만 Blackwell**), 비용(개발자당 **$200k+**/소비자 **$20k-** 추정, 시설 **$40B**, 업계 **$350B**), 토큰 길이(400K/1M+), 추론 토큰 증감(비용 단계상승/향후 효율화 전망).
    - **정책·거버넌스·지정학:** 중국 **AI+** 계획(오픈모델 수 목표, “자율·통제”), 미국 **White House AI Action Plan** 유사성, 규제 논점(오픈모델 금지 주장 vs 개방 필요), 칩 생태계(화웨이, Nvidia), “무질서 경쟁” 발언, 분배·규제 영향.
    - **시장·제품 전략·모네타이즈:** 에이전틱 커머스(**Buy it in ChatGPT**, **ACP**, **Stripe/Shopify**), 라우터 전략(가치 높은 질의에 고비용 모델), 앱 전환(이메일/캘린더/여행/뱅킹), 오픈 vs 클로즈드 스택(서빙/툴 품질), 벤치마크 대비 실사용 가치.
    - **오픈모델 생태계(중국 랩 랭킹):** 랩명, 포커스, 릴리즈 빈도, 오픈 가중치/라이선스, 커뮤니티 지원(MLX/GGUF/CLI), 데이터셋 공개 여부, 엣지/멀티모달 역량, 주목/부상/명예 언급 카테고리.
    - **정서·톤·불확실성:** 낙관/경고(사회 대비 미흡, 복잡성의 저주), 속도 체감(선형 vs 점프·정체), 불확실성 포인트(가격/채택 2–4년, 2028–29 흐림), 위험(설득·개인적 상호작용 리스크).
    - **인용·코멘트·대화 맥락:** 직접 인용문(텍스트), 출처 글/토크(예: **ARC‑AGI 대화**, **The Curve** 강연), 댓글 스레드 요점(질문·반응), 외부 참조(WSJ, Economist, ChinaTalk 등).
    - **근거 링크·참조 그래프:** 내부 참조(url://ID), 외부 링크(도메인), 상호 참조(글↔글), 관련 시리즈/랭킹/로그 연결.
    - **추출 메타(품질관리):** 추출 버전, LLM 프롬프트 ID, 신뢰도(1–5), 검토 상태(초안/검수/확정), 타임스탬프.
- DB -
    
    ```jsx
    {
    
      "executive_summary": {
        "main_theme": "LLM industry's transition from research to tangible revenue",
        "key_insights": [
          "ChatGPT reaches 700M weekly users (13% of global online population)",
          "OpenAI hits $12B ARR, targeting $20B by year-end",
          "Anthropic revenue climbs 5x YTD to $5B"
        ],
        "market_sentiment": "bullish",
        "impact_assessment": "high"
      },
    
      "content_sections": {
        "introduction": {
          "author_commentary": "Evidence of the LLM industry's transition from research and hype to tangible revenue...",
          "week_overview": "Major developments in AI monetization and adoption metrics",
          "key_narrative": "AI is moving from nascent technology into mature commercial arena"
        },
    
        "major_news": [
          {
            "rank": 1,
            "headline": "Google DeepMind Is Rolling Out Gemini 2.5 Deep Think",
            "category": "model_release",
            "organization": "Google DeepMind",
            "summary": "Introduces Deep Think feature with parallel reasoning for complex tasks",
            "technical_details": {
              "model_name": "Gemini 2.5 Deep Think",
              "architecture_features": ["parallel reasoning", "gold-medal IMO performance"],
              "availability": "Google AI Ultra subscribers",
              "performance_metrics": {
                "benchmark": "IMO",
                "level": "bronze (everyday use), gold (complex problems)"
              }
            },
            "business_impact": "Enhances competitive position in reasoning tasks",
            "source_url": "https://blog.google/products/gemini/gemini-2-5-deep-think/",
            "analysis": "Designed for faster everyday use vs hours for complex problems"
          },
          {
            "rank": 2,
            "headline": "Chinese AI Lab Z.ai Launched GLM 4.5",
            "category": "model_release",
            "organization": "Z.ai",
            "summary": "Released GLM-4.5 and GLM-4.5-Air MoE models",
            "technical_details": {
              "model_variants": [
                {
                  "name": "GLM-4.5",
                  "total_params": "355B",
                  "active_params": "32B",
                  "architecture": "Mixture of Experts"
                },
                {
                  "name": "GLM-4.5-Air",
                  "total_params": "106B",
                  "active_params": "12B",
                  "architecture": "Mixture of Experts"
                }
              ],
              "capabilities": ["reasoning", "coding", "agentic tasks", "web browsing"],
              "ranking": "third overall on major benchmarks"
            },
            "source_url": "https://z.ai/blog/glm-4.5"
          }
        ],
       
       "research_papers": [
          {
            "title": "A Survey of Self-Evolving Agents: On Path to Artificial Super Intelligence",
            "arxiv_id": "2507.21046",
            "authors": ["Not specified"],
            "institution": "Not specified",
            "key_contributions": [
              "Organizes efforts around evolving agent components",
              "Analyzes algorithmic designs and evaluation metrics",
              "Applications in coding, education, healthcare"
            ],
            "technical_approach": "Survey of self-evolving agent architectures",
            "benchmarks": null,
            "code_availability": false
          },
          {
            "title": "MLE-STAR: Machine Learning Engineering via Search and Targeted Refinement",
            "arxiv_id": "2506.15692",
            "key_contributions": [
              "Automates complex ML pipeline design",
              "Uses search engine for effective models",
              "Iterative refinement of ML components"
            ],
            "methodology": "Search + targeted refinement approach"
          }
        ],
    
        "tools_and_resources": [
          {
            "category": "experiment_tracking",
            "name": "Trackio",
            "description": "Lightweight experiment tracking Python library",
            "github_url": "https://github.com/gradio-app/trackio",
            "built_on": ["HuggingFace Datasets", "HuggingFace Spaces"],
            "license": "open-source"
          },
          {
            "category": "coding_agent",
            "name": "OpenCode",
            "description": "AI coding agent built for the terminal",
            "github_url": "https://github.com/sst/opencode"
          },
          {
            "category": "agent_framework",
            "name": "AgentSociety",
            "description": "Framework for building agents in urban simulation",
            "github_url": "https://github.com/tsinghua-fib-lab/agentsociety/"
          }
        ]
    ```
    
- DB 위처럼 뽑는다면 어떻게 나올까요 한번 해본것 - 가영
    
    GPT한테 던져준 섭스택 예시:
    
    [https://magazine.sebastianraschka.com/p/from-gpt-2-to-gpt-oss-analyzing-the](https://magazine.sebastianraschka.com/p/from-gpt-2-to-gpt-oss-analyzing-the)
    
    ## documents
    
    **역할:** 하나의 완전한 문서 (의미적으로 유사한 글 중 대표일 가능성 있음)
    
    ```json
    식별:
    - id: "doc_20250809_raschka_gptoss"
    - source: "sebastianraschka.com"
    - source_id: "from-gpt-2-to-gpt-oss-analyzing-the"
    - source_url: "https://magazine.sebastianraschka.com/p/from-gpt-2-to-gpt-oss-analyzing-the"
    - canonical_url: "https://magazine.sebastianraschka.com/p/from-gpt-2-to-gpt-oss-analyzing-the"
    - content_hash: "a2e3d8c1f46f89fbc7a928... (SHA256 예시)"
    - simhash64: 49827102947293847   ← (추가: 의미중복 필터 대비용)
    - cluster_id: "clu_202508_gpt_architecture"   ← (추가: GPT-architecture 관련 클러스터)
    - is_representative: true                     ← (추가: 이 클러스터의 대표 문서)
    - representative_id: null
    
    문서 정보:
    - title: "From GPT-2 to gpt-oss: Analyzing the Architectural Advances"
    - author: "Sebastian Raschka"
    - published_at: "2025-08-09T00:00:00Z"
    
    콘텐츠:
    - full_content_type: "html"
    - full_content: "This article provides a technical comparison of OpenAI's new gpt-oss models (20B and 120B) with earlier GPT-2–GPT-4 models, analyzing architectural evolution..."
    - structured_content:
        {
          "sections": [
            {"title": "Introduction", "summary": "Motivation for gpt-oss release and open model transparency"},
            {"title": "Architectural Evolution", "points": ["Layer scaling", "GQA", "Sliding Window Attention", "RMSNorm"]},
            {"title": "Quantization & Efficiency", "points": ["MXFP4 quantization", "single-GPU inference feasibility"]},
            {"title": "Comparative Benchmarks", "points": ["gpt-oss vs Qwen3", "Depth vs Width trade-offs"]},
            {"title": "Outlook", "summary": "Trends toward modular and open LLM architectures"}
          ]
        }
    
    메타데이터:
    - duration: null
    - word_count: 2350
    - language: "en"
    - thumbnail_url: "https://substackcdn.com/image/fetch/w_1200/..."
    - source_credibility: 0.95
    - ref_count: 12
    - has_repo: false
    - first_seen_at: "2025-08-09T02:00:00Z"
    
    품질 및 가치 평가 (LLM 저지 관련):
    - judge_scores: {"originality": 4.8, "depth": 4.6, "technical_accuracy": 4.9, "weighted_total": 92.5}   ← (추가)
    - judge_rationale: "The article provides a technically accurate and highly detailed comparison of architectural shifts between GPT-2 and gpt-oss, demonstrating originality in synthesis."   ← (추가)
    - sampling_weight: 0.82   ← (추가: SoftDedup용 가중치)
    - novelty_score: 0.87     ← (추가: semantic overlap 기반 새로움 지표)
    
    처리 상태:
    - processing_status: "completed"
    
    시간:
    - created_at: "2025-08-09T03:00:00Z"
    - updated_at: "2025-08-09T03:00:00Z"
    
    ```
    
    ---
    
    ## contents_extracts
    
    **역할:** 대표 문서 내 핵심 발췌 (요약, 아키텍처 비교 중심)
    
    ```json
    연결:
    - id: "extract_gptoss_summary"
    - document_id: "doc_20250809_raschka_gptoss"
    
    발췌 유형:
    - extract_type: "core_summary"
    
    내용:
    - title: "Key Architectural Shifts in GPT-oss"
    - content: "GPT-oss introduces Grouped Query Attention and Sliding Window Attention to optimize memory use and latency, alongside MXFP4 quantization for efficient single-GPU inference."
    - content_type: "text"
    
    AI 처리:
    - summary: "Describes how OpenAI’s gpt-oss model family optimizes transformer architecture with new attention and quantization strategies."
    - key_points: [
        "Grouped Query Attention (GQA) adoption",
        "MXFP4 quantization format for efficiency",
        "Depth–width trade-off redesign",
        "Improved normalization (RMSNorm)"
      ]
    - topics: ["LLM Architecture", "Attention Mechanisms", "Quantization"]
    - categories: ["AI Research", "Open Model Analysis"]
    
    품질:
    - importance_score: 4.7
    - relevance_score: 0.94
    - judge_score: 4.8   ← (추가: LLM 저지 발췌단위 평가)
    - sampling_weight: 0.88   ← (추가: SoftDedup 기반 희소도 반영)
    
    메타:
    - language: "en"
    - word_count: 185
    - created_at: "2025-08-09T03:00:00Z"
    
    ```
    
    ---
    
    ## user_content
    
    **역할:** 사용자에게 보여줄 콘텐츠 (대표 문서만 게시)
    
    ```json
    연결:
    - id: "uc_20250809_gptoss"
    - document_id: "doc_20250809_raschka_gptoss"
    - extract_id: "extract_gptoss_summary"
    
    표시 정보:
    - display_title: "From GPT-2 to GPT-oss: What Changed Architecturally?"
    - display_summary: "Sebastian Raschka analyzes OpenAI’s gpt-oss series, focusing on quantization, attention redesign, and model efficiency."
    - thumbnail_url: "https://substackcdn.com/image/fetch/w_800/..."
    
    콘텐츠 유형:
    - content_type: "article"
    
    메타데이터:
    - topics: ["LLM Architecture", "OpenAI Models", "Research Analysis"]
    - categories: ["AI Research"]
    - tags: ["gpt-oss", "gpt-2", "quantization", "architecture"]
    - difficulty_level: "intermediate"
    - estimated_time: 7
    
    품질:
    - quality_score: 92
    - relevance_score: 0.95
    - judge_score: 4.8   ← (추가: LLM 저지 통합 점수)
    - sampling_weight: 0.82   ← (추가: 희소도 기반 노출 가중치)
    
    발행 상태:
    - status: "published"
    - published_at: "2025-08-09T03:30:00Z"
    - featured: true
    - trending: true
    
    검색:
    - search_vector: to_tsvector('english', 'GPT-oss OpenAI architecture quantization attention Raschka analysis')
    
    의미적 중복 관리:   ← (추가: 의미적 중복제어 신호)
    - cluster_id: "clu_202508_gpt_architecture"
    - is_representative: true
    - representative_id: null
    
    시간:
    - created_at: "2025-08-09T03:30:00Z"
    - updated_at: "2025-08-09T03:30:00Z"
    - last_viewed_at: null
    
    ```
    
- DB - 이양규
    - GPT, Gemini, Claude 같은 API 기반 모델을 사용한다면 토큰 수, 생성에서 발생한 비용 같은 것이 포함되면 좋을듯 - LiteLLM에서 해당 기능을 지원함 ([https://www.litellm.ai/](https://www.litellm.ai/))
    - 추출 값을 LLM이 생성한다면 전체 값을 대문자 혹은 소문자로 변환하는 과정을 거쳤으면 나중에 편할 것 같다. (어떤건 ICRL인데 어떤건 icrl일 경우를 대비) - 원본 소스에서 그대로 추출하기 때문에 그럴 경우는 적을 것 같기도 함