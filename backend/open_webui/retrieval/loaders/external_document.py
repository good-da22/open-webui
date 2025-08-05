import requests
import logging, os
from typing import Iterator, List, Union

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])


class ExternalDocumentLoader(BaseLoader):
    def __init__(
        self,
        file_path,
        url: str,
        api_key: str,
        mime_type=None,
        **kwargs,
    ) -> None:
        self.url = url
        self.api_key = api_key
        self.file_path = file_path
        self.mime_type = mime_type

    def load(self) -> List[Document]:
        headers = {}
        if self.api_key is not None:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # 파일 준비
        with open(self.file_path, "rb") as f:
            files = {"document": (os.path.basename(self.file_path), f, self.mime_type or "application/octet-stream")}
            
            # OCR 모델 지정
            data = {"model": "ocr"}

            log.info(f"[ExternalDocumentLoader] Sending request to OCR API ", extra={"file_path": self.file_path})
            log.info(f"[ExternalDocumentLoader] URL: {self.url}, Headers: {headers}")

            try:
                # POST 요청으로 변경
                response = requests.post(
                    self.url,  # URL을 직접 사용 (기존 코드는 /process를 추가했음)
                    headers=headers,
                    files=files,
                    data=data
                )
            except Exception as e:
                log.error(f"Error connecting to endpoint: {e}")
                raise Exception(f"Error connecting to endpoint: {e}")

        if response.ok:
            response_data = response.json()
            if response_data:
                # OCR API 응답 형식에 맞춰 파싱
                if isinstance(response_data, dict):
                    # 텍스트 추출
                    text_content = response_data.get("text", "")
                    
                    # 메타데이터 구성
                    metadata = {
                        "source": os.path.basename(self.file_path),
                        "confidence": response_data.get("confidence", 0),
                        "model_version": response_data.get("modelVersion", ""),
                        "mime_type": response_data.get("mimeType", ""),
                        "num_pages": response_data.get("numBilledPages", 1),
                    }
                    
                    # 페이지 정보가 있으면 추가
                    if "metadata" in response_data and "pages" in response_data["metadata"]:
                        pages_info = response_data["metadata"]["pages"]
                        metadata["pages"] = pages_info
                        metadata["total_pages"] = len(pages_info)
                    
                    # 단어 정보가 있으면 단어 수 추가
                    if "pages" in response_data and len(response_data["pages"]) > 0:
                        total_words = 0
                        for page in response_data["pages"]:
                            if "words" in page:
                                total_words += len(page["words"])
                        metadata["total_words"] = total_words
                    
                    return [
                        Document(
                            page_content=text_content,
                            metadata=metadata
                        )
                    ]
                else:
                    raise Exception("Error loading document: Unexpected response format")
            else:
                raise Exception("Error loading document: No content returned")
        else:
            raise Exception(
                f"Error loading document: {response.status_code} {response.text}"
            )
