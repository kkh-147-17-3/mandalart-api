### API 문서화 (Swagger)
- https://mandalart.ugsm.co.kr/docs


### 개발환경
- Python: 3.12
- Package Manager: Poetry
- Framework: FastAPI
- Type Checker: mypy
- Test: pytest

### 실행방법 (Docker)
```sh
docker compose -f docker-compose-blue.yml -p mandalart-blue up -d 
```

### mypy 실행방법
```sh
mypy . --check-untyped-defs
```

### pytest 실행방법
```sh
pytest .
```