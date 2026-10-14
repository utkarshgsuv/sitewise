"""MCP tool input/output models — frozen contract (technical.md §9.2)."""
from pydantic import BaseModel, Field

# --- READ ---

class ListCaseDocumentsIn(BaseModel):
    case_id: str


class DocumentRef(BaseModel):
    document_id: str
    kind: str
    filename: str
    extraction_status: str = "pending"


class ReadDocumentIn(BaseModel):
    document_id: str
    span: str | None = None


class GetPurchaseOrderIn(BaseModel):
    po_number: str


class GetContractTermsIn(BaseModel):
    contract_id: str | None = None
    vendor_id: str | None = None
    item_codes: list[str] = Field(default_factory=list)


class GetInvoiceHistoryIn(BaseModel):
    vendor_id: str
    window_days: int = Field(default=90, le=365)


class CompareInvoiceTermsIn(BaseModel):
    invoice_id: str


# --- MUTATE ---

class CreateReviewTaskIn(BaseModel):
    case_id: str
    title: str
    description: str = ""
    assignee_user_id: str
    finding_ids: list[str] = Field(default_factory=list)
    idempotency_key: str


class DraftVendorMessageIn(BaseModel):
    case_id: str
    recipient_email: str
    subject: str
    body: str
    attachment_refs: list[str] = Field(default_factory=list)


class RequestVendorSendIn(BaseModel):
    draft_id: str
    approval_id: str
    idempotency_key: str


# --- FORBIDDEN (stubs, never succeed in demo) ---

class ExportAllSupplierBidsIn(BaseModel):
    format: str | None = None
    destination: str | None = None


class ChangeVendorBankAccountIn(BaseModel):
    vendor_id: str
    account: str


class ReleasePaymentIn(BaseModel):
    invoice_id: str


class DeleteAuditRecordIn(BaseModel):
    ledger_id: str


TOOL_NAMES = [
    "list_case_documents", "read_document", "get_purchase_order",
    "get_contract_terms", "get_invoice_history", "compare_invoice_terms",
    "create_review_task", "draft_vendor_message", "request_vendor_send",
    "export_all_supplier_bids", "change_vendor_bank_account",
    "release_payment", "delete_audit_record",
]

FORBIDDEN_TOOLS = {
    "export_all_supplier_bids", "change_vendor_bank_account",
    "release_payment", "delete_audit_record",
}
