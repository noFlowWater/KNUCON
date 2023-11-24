from pydantic import BaseModel, validator 

class Report(BaseModel):
    report_id: str
    reason: int
    reported_uid: str
    reporter_uid: str
    
class ReportInput(BaseModel):
    reason: int
    reported_uid: str

    @validator('reason', 'reported_uid')
    def not_null(cls, v):
        if not v:
            raise ValueError('Empty values are not allowed.')
        return v
    
