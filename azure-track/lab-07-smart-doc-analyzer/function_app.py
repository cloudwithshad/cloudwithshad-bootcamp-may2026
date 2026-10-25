import os
import uuid
import json
import logging
import traceback
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="analyze")
def analyze_document(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Analyze document HTTP trigger invoked.")
    
    blob_name = req.params.get("file", "test_1.pdf")
    container_name = "documents"

    try:
        storage_conn = os.environ.get("AzureWebJobsStorage")
        doc_intel_endpoint = os.environ.get("DOC_INTEL_ENDPOINT")
        doc_intel_key = os.environ.get("DOC_INTEL_KEY")
        language_endpoint = os.environ.get("LANGUAGE_ENDPOINT")
        language_key = os.environ.get("LANGUAGE_KEY")
        cosmos_conn = os.environ.get("COSMOS_CONNECTION_STRING")

        # 1. Download blob from docanalyzerstore
        blob_service = BlobServiceClient.from_connection_string(storage_conn)
        blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)
        blob_bytes = blob_client.download_blob().readall()

        # 2. Document Intelligence OCR
        doc_client = DocumentAnalysisClient(
            endpoint=doc_intel_endpoint, 
            credential=AzureKeyCredential(doc_intel_key)
        )
        poller = doc_client.begin_analyze_document("prebuilt-read", document=blob_bytes)
        result = poller.result()
        extracted_text = " ".join([line.content for page in result.pages for line in page.lines])

        # 3. Azure AI Language (Sentiment)
        text_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=AzureKeyCredential(language_key)
        )
        sentiment_resp = text_client.analyze_sentiment([extracted_text[:5000] if extracted_text else "sample text"])[0]

        # 4. Save to Cosmos DB
        cosmos_client = CosmosClient.from_connection_string(cosmos_conn)
        db = cosmos_client.get_database_client("DocAnalyzerDB")
        container = db.get_container_client("AnalysisResults")

        doc_record = {
            "id": str(uuid.uuid4()),
            "document_id": blob_name,
            "page_count": len(result.pages),
            "extracted_text_preview": extracted_text[:200] if extracted_text else "",
            "sentiment": sentiment_resp.sentiment,
            "positive_score": sentiment_resp.confidence_scores.positive
        }

        container.create_item(body=doc_record)

        return func.HttpResponse(
            json.dumps({
                "status": "Success",
                "message": f"Successfully processed {blob_name} and persisted to Cosmos DB",
                "record": doc_record
            }, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        error_details = {
            "status": "Failed",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }
        return func.HttpResponse(
            json.dumps(error_details, indent=2),
            mimetype="application/json",
            status_code=200
        )