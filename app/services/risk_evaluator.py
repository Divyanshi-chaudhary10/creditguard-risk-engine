from sqlalchemy.orm import Session
from app.models.schemas import ApplicantAccount

class RiskOrchestrator:
    def __init__(self, db: Session):
        self.db = db

    def evaluate_and_lock(self, applicant_id: int, loan_amount: float):
        """
        Evaluates risk while preventing race conditions using Row-Level Locking.
        """
        # "with_for_update" creates a SELECT ... FOR UPDATE lock in PostgreSQL
        account = self.db.query(ApplicantAccount).filter(
            ApplicantAccount.id == applicant_id
        ).with_for_update().first()

        if not account:
            return {"error": "Applicant not found"}

        # Simulate fraud check logic
        is_fraudulent = self.check_historical_patterns(account)
        
        if is_fraudulent:
            account.status = "FLAGGED"
            self.db.commit()
            return {"decision": "REJECTED", "reason": "High Fraud Probability"}

        # Update balance safely within the lock
        account.total_exposure += loan_amount
        self.db.commit()
        return {"decision": "APPROVED", "new_exposure": account.total_exposure}

    def check_historical_patterns(self, account):
        # Placeholder for complex ML logic
        return False