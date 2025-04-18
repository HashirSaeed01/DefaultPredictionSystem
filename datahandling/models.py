from apps import db
import pandas as pd

class FinancialMetrics(db.Model):
    __tablename__ = 'FinancialMetrics'

    id = db.Column(db.Integer, primary_key=True)
    rowID = db.Column(db.Integer, nullable=False)
    material = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    musharaka = db.Column(db.Float, nullable=False)
    profit_rate = db.Column(db.Float, nullable=False)
    kibor_rate = db.Column(db.Float, nullable=False)
    kibor_tenure_name = db.Column(db.String, nullable=False)
    financing_amount = db.Column(db.Float, nullable=False)
    tenure = db.Column(db.Integer, nullable=False)
    actual_tenure = db.Column(db.Integer, nullable=False)
    program = db.Column(db.String, nullable=False)
    cos_qty = db.Column(db.Integer, nullable=False)
    repayment_status = db.Column(db.String, nullable=False)
    remaining_principal_amount = db.Column(db.Float, nullable=False)
    charity_amount = db.Column(db.Float, nullable=False)
    district = db.Column(db.String, nullable=False)
    business_years = db.Column(db.Integer, nullable=False)
    entity_type = db.Column(db.String, nullable=False)
    collection_period_days = db.Column(db.Integer, nullable=False)
    season = db.Column(db.String, nullable=False)
    repayment_days = db.Column(db.Integer, nullable=False)
    repayment_days_ratio = db.Column(db.Float, nullable=False)
    assisted_tv = db.Column(db.Integer, nullable=False)
    previous_transactions = db.Column(db.Integer, nullable=False)
    previous_data = db.Column(db.Float, nullable=False)
    ethic = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    gdp = db.Column(db.Float, nullable=False)
    kse100_index = db.Column(db.Float, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    target_variable = db.Column(db.String, nullable=False)
    prediction_percentage = db.Column(db.Float, nullable=True)  # Add this new column

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        """Creates a new FinancialMetrics record."""
        record = cls(**kwargs)
        db.session.add(record)
        db.session.commit()
        return record

    def update_field(self, field_name, new_value):
        """Updates a specific field of the record."""
        if hasattr(self, field_name):
            setattr(self, field_name, new_value)
            db.session.commit()
            return True
        return False

    @classmethod
    def from_dataframe(cls, df):
        """Creates multiple FinancialMetrics objects from a DataFrame."""
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]  
        records = [cls(**row) for row in df.to_dict(orient="records")]
        db.session.add_all(records)
        db.session.commit()
        return records

    def __repr__(self):
        return f"<FinancialMetrics rowID={self.rowID} material={self.material} program={self.program} target_variable={self.target_variable}>"
