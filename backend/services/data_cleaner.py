"""
Data Cleaning Service
Handles AI-powered preprocessing and cleaning of extracted transaction data
"""
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import Counter


class DataCleaner:
    """Handles data cleaning and preprocessing for transactions"""
    
    # Common noise words to remove from descriptions
    NOISE_WORDS = [
        'ref', 'reference', 'txn', 'transaction', 'neft', 'imps', 'upi', 'rtgs',
        'atm', 'ach', 'ecs', 'nach', 'mmt', 'iob', 'sbi', 'hdfc', 'icici', 'axis',
        'transfer', 'payment', 'paid', 'received', 'debit', 'credit', 'card',
        'pos', 'ecom', 'online', 'net', 'banking', 'mobile', 'app'
    ]
    
    # Keywords for income identification
    INCOME_KEYWORDS = [
        'salary', 'wages', 'income', 'credit', 'deposit', 'refund', 'cashback',
        'dividend', 'interest', 'bonus', 'reimbursement', 'received', 'credited',
        'from', 'reversal', 'return', 'inward'
    ]
    
    # Keywords for expense identification
    EXPENSE_KEYWORDS = [
        'payment', 'purchase', 'buy', 'bought', 'paid', 'debit', 'withdrawal',
        'transfer', 'to', 'bill', 'fee', 'charge', 'subscription', 'order',
        'spent', 'expense', 'outward'
    ]

    def __init__(self):
        pass
    
    def clean_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """
        Clean and preprocess a list of transactions
        
        Steps:
        1. Remove duplicates
        2. Normalize dates
        3. Clean descriptions
        4. Validate transaction types
        5. Fill missing fields
        """
        if not transactions:
            return []
        
        # Step 1: Remove duplicates
        cleaned = self._remove_duplicates(transactions)
        
        # Step 2-5: Clean each transaction
        cleaned = [self._clean_transaction(t) for t in cleaned]
        
        # Remove None values (invalid transactions)
        cleaned = [t for t in cleaned if t is not None]
        
        # Sort by date
        cleaned.sort(key=lambda x: x.get('transaction_date', ''), reverse=True)
        
        return cleaned
    
    def _remove_duplicates(self, transactions: List[Dict]) -> List[Dict]:
        """Remove duplicate transactions"""
        seen = set()
        unique = []
        
        for trans in transactions:
            # Create a unique key from date + amount + description
            key = (
                trans.get('transaction_date', ''),
                trans.get('amount', 0),
                trans.get('description', '').lower().strip()[:50]
            )
            
            if key not in seen:
                seen.add(key)
                unique.append(trans)
        
        return unique
    
    def _clean_transaction(self, transaction: Dict) -> Optional[Dict]:
        """Clean a single transaction"""
        cleaned = transaction.copy()
        
        # Validate and normalize date
        date_val = cleaned.get('transaction_date')
        if date_val:
            normalized_date = self._normalize_date(date_val)
            if not normalized_date:
                return None
            cleaned['transaction_date'] = normalized_date
        else:
            return None
        
        # Validate amount
        amount = cleaned.get('amount')
        if not amount or amount <= 0:
            return None
        cleaned['amount'] = round(float(amount), 2)
        
        # Clean description
        description = cleaned.get('description', '')
        cleaned['description'] = self._clean_description(description)
        
        # Clean merchant
        merchant = cleaned.get('merchant', '')
        cleaned['merchant'] = self._clean_merchant(merchant, cleaned['description'])
        
        # Validate/infer transaction type
        trans_type = cleaned.get('type', '')
        if trans_type not in ['income', 'expense']:
            cleaned['type'] = self._infer_transaction_type(cleaned)
        
        return cleaned
    
    def _normalize_date(self, date_value) -> Optional[str]:
        """Normalize date to ISO format"""
        if not date_value:
            return None
        
        # Already in ISO format
        if isinstance(date_value, str) and re.match(r'^\d{4}-\d{2}-\d{2}', date_value):
            return date_value[:10]
        
        # Parse datetime object
        if isinstance(date_value, datetime):
            return date_value.strftime('%Y-%m-%d')
        
        return date_value[:10] if isinstance(date_value, str) else None
    
    def _clean_description(self, description: str) -> str:
        """Clean transaction description"""
        if not description:
            return ''
        
        # Convert to string and strip
        desc = str(description).strip()
        
        # Remove extra whitespace
        desc = ' '.join(desc.split())
        
        # Remove reference numbers (long digit sequences)
        desc = re.sub(r'\b\d{10,}\b', '', desc)
        
        # Remove common prefixes/suffixes
        desc = re.sub(r'^(UPI|NEFT|IMPS|RTGS|ATM|POS|ECS)[/-]?\s*', '', desc, flags=re.IGNORECASE)
        
        # Remove transaction IDs
        desc = re.sub(r'\b[A-Z0-9]{15,}\b', '', desc)
        
        # Clean up multiple spaces
        desc = ' '.join(desc.split())
        
        # Capitalize properly
        if desc:
            desc = desc.strip()
            if desc.isupper() or desc.islower():
                desc = desc.title()
        
        return desc[:255]  # Limit length
    
    def _clean_merchant(self, merchant: str, description: str) -> str:
        """Clean and extract merchant name"""
        if merchant:
            merchant = str(merchant).strip()
            # Remove reference numbers
            merchant = re.sub(r'\b\d{8,}\b', '', merchant)
            merchant = ' '.join(merchant.split())
            if len(merchant) > 2:
                return merchant[:100]
        
        # Try to extract from description
        if description:
            # Common patterns
            patterns = [
                r'(?:to|from|at|@)\s+([A-Za-z][A-Za-z0-9\s&\'\.]+)',
                r'^([A-Za-z][A-Za-z0-9\s&\'\.]{2,30}?)(?:\s+\d|$|-)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, description, re.IGNORECASE)
                if match:
                    extracted = match.group(1).strip()
                    # Clean extracted merchant
                    extracted = re.sub(r'\s+', ' ', extracted)
                    if 2 < len(extracted) < 50:
                        # Remove noise words from end
                        words = extracted.split()
                        while words and words[-1].lower() in self.NOISE_WORDS:
                            words.pop()
                        if words:
                            return ' '.join(words)
        
        return ''
    
    def _infer_transaction_type(self, transaction: Dict) -> str:
        """Infer transaction type from description and other fields"""
        description = (transaction.get('description', '') + ' ' + 
                      transaction.get('merchant', '')).lower()
        
        # Count keyword matches
        income_score = sum(1 for kw in self.INCOME_KEYWORDS if kw in description)
        expense_score = sum(1 for kw in self.EXPENSE_KEYWORDS if kw in description)
        
        # Check amount sign if preserved
        amount = transaction.get('original_amount', transaction.get('amount', 0))
        if isinstance(amount, (int, float)) and amount < 0:
            return 'expense'
        
        # Decide based on keywords
        if income_score > expense_score:
            return 'income'
        
        # Default to expense (most transactions are expenses)
        return 'expense'
    
    def get_cleaning_summary(self, original: List[Dict], cleaned: List[Dict]) -> Dict:
        """Get summary of cleaning operations"""
        return {
            'original_count': len(original),
            'cleaned_count': len(cleaned),
            'duplicates_removed': len(original) - len(cleaned),
            'income_count': sum(1 for t in cleaned if t.get('type') == 'income'),
            'expense_count': sum(1 for t in cleaned if t.get('type') == 'expense'),
            'date_range': self._get_date_range(cleaned),
            'total_income': sum(t.get('amount', 0) for t in cleaned if t.get('type') == 'income'),
            'total_expenses': sum(t.get('amount', 0) for t in cleaned if t.get('type') == 'expense'),
        }
    
    def _get_date_range(self, transactions: List[Dict]) -> Dict:
        """Get date range of transactions"""
        if not transactions:
            return {'start': None, 'end': None}
        
        dates = [t.get('transaction_date') for t in transactions if t.get('transaction_date')]
        if not dates:
            return {'start': None, 'end': None}
        
        return {
            'start': min(dates),
            'end': max(dates)
        }


# Global instance
data_cleaner = DataCleaner()
