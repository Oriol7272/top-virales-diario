# Payment System - PayPal Only (Stripe removed)

from fastapi import APIRouter, HTTPException, Request, Header, Depends
from typing import Optional
import os
from datetime import datetime
import logging

from models import CheckoutRequest, PaymentTransaction, PaymentStatus, SubscriptionTier, User
from subscription_plans import get_plan
from auth import AuthService, get_current_user, require_user

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self, db, auth_service: AuthService):
        self.db = db
        self.auth_service = auth_service
    
    async def create_payment_intent(self, request_data: CheckoutRequest, user: Optional[User] = None):
        """Create a payment intent for subscription (PayPal integration only)"""
        try:
            # Get plan details
            plan = get_plan(request_data.subscription_tier)
            if not plan:
                raise HTTPException(status_code=400, detail="Invalid subscription tier")
            
            # Calculate amount
            amount = plan.price_yearly if request_data.billing_cycle == "yearly" else plan.price_monthly
            
            # Create payment transaction record
            transaction = PaymentTransaction(
                user_id=user.id if user else None,
                email=request_data.email or (user.email if user else None),
                session_id=f"paypal_{datetime.utcnow().timestamp()}",
                amount=amount,
                currency="eur",
                status=PaymentStatus.PENDING,
                payment_method="paypal",
                subscription_tier=request_data.subscription_tier,
                metadata={"billing_cycle": request_data.billing_cycle}
            )
            
            await self.db.payment_transactions.insert_one(transaction.dict())
            logger.info(f"Created payment transaction {transaction.id}")
            
            return {
                "payment_id": transaction.id,
                "amount": amount,
                "currency": "EUR",
                "subscription_tier": request_data.subscription_tier.value
            }
            
        except Exception as e:
            logger.error(f"Error creating payment intent: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating payment: {str(e)}")

def create_payment_router(db, auth_service: AuthService) -> APIRouter:
    """Create payment router with basic payment endpoints"""
    router = APIRouter(prefix="/api/payments")
    payment_service = PaymentService(db, auth_service)
    
    @router.post("/create-intent")
    async def create_payment_intent(
        request_data: CheckoutRequest,
        user: Optional[User] = Depends(get_current_user)
    ):
        """Create a payment intent"""
        return await payment_service.create_payment_intent(request_data, user)
    
    @router.get("/transactions/me")
    async def get_my_transactions(user: User = Depends(require_user)):
        """Get current user's payment transactions"""
        try:
            transactions = await db.payment_transactions.find(
                {"user_id": user.id}
            ).sort("created_at", -1).to_list(50)
            return {"transactions": transactions, "total": len(transactions)}
        except Exception as e:
            logger.error(f"Error fetching user transactions: {str(e)}")
            raise HTTPException(status_code=500, detail="Error fetching transactions")
    
    return router