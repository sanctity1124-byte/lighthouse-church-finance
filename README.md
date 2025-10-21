
# 등대교회 재정관리 (Installer-ready)

이 레포지토리는 등대교회 재정관리 프로그램의 GitHub 자동 빌드(설치형 EXE)용 샘플입니다.

## 로컬에서 실행 (개발용)
1. Python 설치 (3.8+ 권장)
2. 가상환경 생성 및 활성화 (선택)
3. 패키지 설치:
   pip install -r requirements.txt
4. 실행:
   python main.py

## GitHub Actions로 설치형 EXE 빌드
이 레포지토리를 GitHub에 올리면 `.github/workflows/build-installer.yml`이 자동으로 실행되어 Windows용 설치파일(.exe)을 생성합니다.
생성된 설치파일은 Actions의 Artifacts 또는 Release에서 다운로드 가능합니다.
