from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from domain.report.report_schema import ReportInput
import domain.report.report_crud as report_crud
from util import get_current_user_id
from db import get_db_connection

router = APIRouter(
    prefix = '/reports'
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("") # POST /reports: create new report
def file_report(file_report: ReportInput, conn=Depends(get_db_connection), reporter_uid: str = Depends(get_current_user_id)):
    return report_crud.file_report(file_report, reporter_uid)

@router.get("")  # GET /reports: GET all reports
def list_report(user_id: Optional[str] = None, conn=Depends(get_db_connection)):
    return report_crud.list_report(user_id, conn)