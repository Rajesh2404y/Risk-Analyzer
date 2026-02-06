"""
File Processing Service
Handles extraction of transaction data from CSV, Excel, and PDF files
"""
import os
import re
import pandas as pd
import pdfplumber
import chardet
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from io import BytesIO


class FileProcessor:
    """Handles file processing for different file types"""
    
    # Common date formats to try
    DATE_FORMATS = [
        '%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y',
        '%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y',
        '%d %b %Y', '%d %B %Y', '%b %d, %Y', '%B %d, %Y',
        '%d.%m.%Y', '%m.%d.%Y',
        '%Y%m%d',
    ]
    
    # Column name mappings for auto-detection
    COLUMN_MAPPINGS = {
        'date': ['date', 'transaction date', 'txn date', 'value date', 'posting date', 
                 'trans date', 'transaction_date', 'txn_date'],
        'description': ['description', 'particulars', 'narration', 'details', 'remarks',
                       'transaction description', 'memo', 'reference', 'desc'],
        'debit': ['debit', 'withdrawal', 'dr', 'debit amount', 'withdrawals', 
                  'amount debit', 'dr.', 'debit_amount'],
        'credit': ['credit', 'deposit', 'cr', 'credit amount', 'deposits',
                   'amount credit', 'cr.', 'credit_amount'],
        'amount': ['amount', 'transaction amount', 'txn amount', 'value', 'sum',
                   'transaction_amount', 'txn_amount'],
        'balance': ['balance', 'running balance', 'closing balance', 'available balance',
                    'current balance', 'bal'],
        'merchant': ['merchant', 'payee', 'vendor', 'beneficiary', 'recipient', 'to/from'],
        'category': ['category', 'type', 'transaction type', 'txn type']
    }

    def __init__(self):
        self.supported_extensions = ['.csv', '.xlsx', '.xls', '.pdf']
    
    def get_file_type(self, filename: str) -> str:
        """Determine file type from extension"""
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.csv':
            return 'csv'
        elif ext in ['.xlsx', '.xls']:
            return 'excel'
        elif ext == '.pdf':
            return 'pdf'
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def process_file(self, file_content: bytes, filename: str) -> Tuple[List[Dict], Dict]:
        """
        Process uploaded file and extract transactions
        
        Returns:
            Tuple of (transactions_list, processing_details)
        """
        file_type = self.get_file_type(filename)
        
        if file_type == 'csv':
            return self._process_csv(file_content)
        elif file_type == 'excel':
            return self._process_excel(file_content)
        elif file_type == 'pdf':
            return self._process_pdf(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _process_csv(self, file_content: bytes) -> Tuple[List[Dict], Dict]:
        """Process CSV file"""
        details = {'file_type': 'csv', 'rows_read': 0, 'rows_processed': 0}
        
        # Detect encoding
        detected = chardet.detect(file_content)
        encoding = detected.get('encoding', 'utf-8')
        details['encoding'] = encoding
        
        try:
            # Try reading with detected encoding
            df = pd.read_csv(BytesIO(file_content), encoding=encoding)
        except Exception:
            # Fallback to common encodings
            for enc in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(BytesIO(file_content), encoding=enc)
                    details['encoding'] = enc
                    break
                except Exception:
                    continue
            else:
                raise ValueError("Could not decode CSV file with any known encoding")
        
        details['rows_read'] = len(df)
        details['columns_found'] = list(df.columns)
        
        transactions = self._extract_transactions_from_dataframe(df, details)
        return transactions, details
    
    def _process_excel(self, file_content: bytes) -> Tuple[List[Dict], Dict]:
        """Process Excel file"""
        details = {'file_type': 'excel', 'rows_read': 0, 'rows_processed': 0}
        
        try:
            # Read first sheet by default
            df = pd.read_excel(BytesIO(file_content), engine='openpyxl')
            details['rows_read'] = len(df)
            details['columns_found'] = list(df.columns)
            
            transactions = self._extract_transactions_from_dataframe(df, details)
            return transactions, details
        except Exception as e:
            raise ValueError(f"Error reading Excel file: {str(e)}")
    
    def _process_pdf(self, file_content: bytes) -> Tuple[List[Dict], Dict]:
        """Process PDF file - extract tables"""
        details = {'file_type': 'pdf', 'pages_read': 0, 'rows_read': 0, 'rows_processed': 0}
        
        try:
            all_data = []
            
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                details['pages_read'] = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages):
                    # Try to extract tables
                    tables = page.extract_tables()
                    
                    for table in tables:
                        if table and len(table) > 1:
                            # First row is likely header
                            headers = [str(h).strip() if h else f'col_{i}' 
                                       for i, h in enumerate(table[0])]
                            
                            for row in table[1:]:
                                if row and any(cell for cell in row):
                                    row_dict = {}
                                    for i, cell in enumerate(row):
                                        if i < len(headers):
                                            row_dict[headers[i]] = str(cell).strip() if cell else ''
                                    all_data.append(row_dict)
                    
                    # If no tables found, try text extraction
                    if not tables:
                        text = page.extract_text()
                        if text:
                            # Try to parse structured text
                            lines = text.split('\n')
                            for line in lines:
                                parsed = self._parse_text_line(line)
                                if parsed:
                                    all_data.append(parsed)
            
            details['rows_read'] = len(all_data)
            
            if not all_data:
                details['warning'] = 'No tabular data found in PDF'
                return [], details
            
            # Convert to DataFrame for processing
            df = pd.DataFrame(all_data)
            details['columns_found'] = list(df.columns)
            
            transactions = self._extract_transactions_from_dataframe(df, details)
            return transactions, details
            
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
    
    def _parse_text_line(self, line: str) -> Optional[Dict]:
        """Try to parse a text line as a transaction"""
        # Pattern: Date Description Amount
        date_pattern = r'(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}|\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2})'
        amount_pattern = r'([\d,]+\.?\d*)'
        
        date_match = re.search(date_pattern, line)
        if not date_match:
            return None
        
        amounts = re.findall(amount_pattern, line)
        if not amounts:
            return None
        
        # Get description as text between date and first amount
        date_str = date_match.group(1)
        date_end = date_match.end()
        
        # Find first amount position
        first_amount = amounts[0]
        amount_pos = line.find(first_amount, date_end)
        
        if amount_pos > date_end:
            description = line[date_end:amount_pos].strip()
        else:
            description = ''
        
        return {
            'date': date_str,
            'description': description,
            'amount': first_amount
        }
    
    def _extract_transactions_from_dataframe(self, df: pd.DataFrame, details: Dict) -> List[Dict]:
        """Extract and normalize transactions from a DataFrame"""
        # Map columns
        column_map = self._detect_columns(df)
        details['column_mapping'] = column_map
        
        if not column_map.get('date'):
            # Try to find date in first column
            if len(df.columns) > 0:
                column_map['date'] = df.columns[0]
        
        transactions = []
        
        for idx, row in df.iterrows():
            try:
                trans = self._parse_row(row, column_map)
                if trans:
                    transactions.append(trans)
            except Exception as e:
                continue
        
        details['rows_processed'] = len(transactions)
        return transactions
    
    def _detect_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """Auto-detect column mappings"""
        column_map = {}
        df_columns = [str(col).lower().strip() for col in df.columns]
        
        for field, possible_names in self.COLUMN_MAPPINGS.items():
            for col_idx, col in enumerate(df_columns):
                if col in possible_names or any(name in col for name in possible_names):
                    column_map[field] = df.columns[col_idx]
                    break
        
        return column_map
    
    def _parse_row(self, row: pd.Series, column_map: Dict[str, str]) -> Optional[Dict]:
        """Parse a single row into a transaction"""
        # Parse date
        date_col = column_map.get('date')
        if date_col and pd.notna(row.get(date_col)):
            date_val = self._parse_date(row[date_col])
        else:
            return None
        
        if not date_val:
            return None
        
        # Parse amount
        amount = 0.0
        transaction_type = 'expense'
        
        debit_col = column_map.get('debit')
        credit_col = column_map.get('credit')
        amount_col = column_map.get('amount')
        
        if debit_col and pd.notna(row.get(debit_col)):
            debit_val = self._parse_amount(row[debit_col])
            if debit_val and debit_val > 0:
                amount = debit_val
                transaction_type = 'expense'
        
        if credit_col and pd.notna(row.get(credit_col)):
            credit_val = self._parse_amount(row[credit_col])
            if credit_val and credit_val > 0:
                amount = credit_val
                transaction_type = 'income'
        
        # If no debit/credit, use amount column
        if amount == 0 and amount_col and pd.notna(row.get(amount_col)):
            amount_val = self._parse_amount(row[amount_col])
            if amount_val:
                amount = abs(amount_val)
                # Negative usually means expense
                transaction_type = 'expense' if amount_val < 0 else 'income'
        
        if amount == 0:
            return None
        
        # Parse description
        desc_col = column_map.get('description')
        description = str(row.get(desc_col, '')).strip() if desc_col and pd.notna(row.get(desc_col)) else ''
        
        # Parse merchant (often same as description or separate)
        merchant_col = column_map.get('merchant')
        merchant = str(row.get(merchant_col, '')).strip() if merchant_col and pd.notna(row.get(merchant_col)) else ''
        
        return {
            'transaction_date': date_val.isoformat(),
            'type': transaction_type,
            'amount': round(amount, 2),
            'description': description,
            'merchant': merchant or self._extract_merchant(description),
        }
    
    def _parse_date(self, value) -> Optional[datetime]:
        """Parse date from various formats"""
        if pd.isna(value):
            return None
        
        if isinstance(value, (datetime, pd.Timestamp)):
            return value
        
        value_str = str(value).strip()
        
        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(value_str, fmt)
            except ValueError:
                continue
        
        # Try pandas datetime parser as fallback
        try:
            return pd.to_datetime(value_str).to_pydatetime()
        except Exception:
            return None
    
    def _parse_amount(self, value) -> Optional[float]:
        """Parse amount from various formats"""
        if pd.isna(value):
            return None
        
        if isinstance(value, (int, float)):
            return float(value)
        
        value_str = str(value).strip()
        
        # Remove currency symbols and whitespace
        value_str = re.sub(r'[₹$€£¥\s]', '', value_str)
        
        # Handle parentheses for negative (accounting format)
        is_negative = value_str.startswith('(') and value_str.endswith(')')
        if is_negative:
            value_str = value_str[1:-1]
        
        # Handle minus sign
        if value_str.startswith('-'):
            is_negative = True
            value_str = value_str[1:]
        
        # Remove commas
        value_str = value_str.replace(',', '')
        
        try:
            amount = float(value_str)
            return -amount if is_negative else amount
        except ValueError:
            return None
    
    def _extract_merchant(self, description: str) -> str:
        """Extract merchant name from description"""
        if not description:
            return ''
        
        # Common patterns to extract merchant
        # Pattern: "Payment to MERCHANT"
        patterns = [
            r'(?:to|from|at|@)\s+([A-Za-z0-9\s&]+)',
            r'^([A-Za-z0-9\s&]+?)(?:\s+\d|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                merchant = match.group(1).strip()
                if len(merchant) > 2 and len(merchant) < 50:
                    return merchant
        
        # Return first few words as merchant
        words = description.split()[:3]
        return ' '.join(words)


# Global instance
file_processor = FileProcessor()
