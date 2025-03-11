from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(60), unique=True, nullable=False)
    username=db.Column(db.String(60), unique=True, nullable=False)
    password=db.Column(db.String(80), nullable=False)
    address=db.Column(db.String(80), nullable=True)
    pincode=db.Column(db.String(10), nullable=True)
    role=db.Column(db.String(10), nullable=False,default='customer')
    is_approved=db.Column(db.Boolean,nullable=False, default=False)
    is_flagged=db.Column(db.Boolean,nullable=False, default=False)
    last_seen=db.Column(db.DateTime, nullable=True, default=datetime.now())
    avg_rating=db.Column(db.Float, default=0.0)
    rating_count=db.Column(db.Integer, default=0)
    # sp_file=db.Column(db.String(80), nullable=True)
    # sp_experience=db.Column(db.String(80), nullable=True)
    service_id=db.Column(db.Integer, db.ForeignKey('householdServices.id',ondelete='SET NULL'), nullable=True)
    service=db.relationship('HouseholdServices',back_populates='service_professionals')
    customer_requests=db.relationship('HouseholdServiceRequest',back_populates='customer',foreign_keys='HouseholdServiceRequest.customer_id')
    service_professional_requests=db.relationship('HouseholdServiceRequest',back_populates='service_professional',foreign_keys='HouseholdServiceRequest.service_professional_id')


    def convert_to_json(self):
        return {
            "id":self.id,
            "email":self.email,
            "username":self.username,
            "address":self.address,
            "pincode":self.pincode,
            "role":self.role,
            "approved":self.is_approved,
            "is_flagged":self.is_flagged,
            "avg_rating":self.avg_rating,
            "rating_count":self.rating_count,
            "service_id":self.service_id
        }

class HouseholdServices(db.Model):
    __tablename__ = "householdServices"
    id=db.Column(db.Integer, primary_key=True)
    service_name=db.Column(db.String(80), unique=True, nullable=False)
    service_description=db.Column(db.String(80), nullable=False)
    base_price=db.Column(db.Float, nullable=False)
    time_required=db.Column(db.String(80), nullable=False)
    service_professionals=db.relationship('User',back_populates='service',cascade="all,delete")
    request=db.relationship('HouseholdServiceRequest',back_populates='service',cascade="all,delete")

    def __repr__(self):
        return f"HouseholdServices('{self.service_name}')"
    
    def convert_to_json(self):
        return {
            "id":self.id,
            "service_name":self.service_name,
            "service_description":self.service_description,
            "base_price":self.base_price,
            "time_required":self.time_required,
            "service_professionals":[sp.convert_to_json() for sp in self.service_professionals]
        }

class HouseholdServiceRequest(db.Model):
    __tablename__ = "householdServiceRequest"
    id=db.Column(db.Integer, primary_key=True)
    service_id=db.Column(db.Integer, db.ForeignKey('householdServices.id'),nullable=True)
    customer_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    service_professional_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    request_type=db.Column(db.String(80), nullable=False)
    description=db.Column(db.Text, nullable=True)
    status=db.Column(db.String(80), nullable=True)
    date_created=db.Column(db.Date, nullable=False,default=datetime.now().date())
    closed_by = db.Column(db.String(20), nullable=True)  # "customer" or "service_professional"
    date_closed=db.Column(db.Date, nullable=True)
    rating_by_customer=db.Column(db.Float,default=0.0)
    review_by_customer=db.Column(db.String(80), nullable=True)
    service=db.relationship('HouseholdServices',back_populates='request')
    customer=db.relationship('User',back_populates='customer_requests',foreign_keys=[customer_id])
    service_professional=db.relationship('User',back_populates='service_professional_requests',foreign_keys=[service_professional_id])

    def convert_to_json(self):
        return {
            "id":self.id,
            "sp_username":self.service_professional.username if self.service_professional else None,
            "service_id":self.service_id,
            "customer_id":self.customer_id,
            "service_professional_id":self.service_professional_id,
            "request_type":self.request_type,
            "description":self.description,
            "status":self.status,
            "date_created":self.date_created.strftime('%Y-%m-%d') if self.date_created else None,
            "date_closed":self.date_closed.strftime('%Y-%m-%d') if self.date_closed else None,
            "closed_by": self.closed_by,  # Include who closed the request
            "rating_by_customer":self.rating_by_customer,
            "review_by_customer":self.review_by_customer
        }