import { useState, useCallback, useRef } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Alert,
  Stack,
  Chip,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Checkbox,
  FormControl,
  Select,
  MenuItem,
  Tooltip,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  InsertDriveFile as FileIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Edit as EditIcon,
  Save as SaveIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { uploadAPI, categoriesAPI } from '../services/api';

interface Category {
  id: number;
  name: string;
  type: string;
  icon: string;
  color: string;
}

interface ExtractedTransaction {
  transaction_date: string;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  merchant: string;
  suggested_category: string;
  category_id: number | null;
  category_confidence: number;
  selected?: boolean;
}

interface UploadSummary {
  original_count: number;
  cleaned_count: number;
  duplicates_removed: number;
  income_count: number;
  expense_count: number;
  total_income: number;
  total_expenses: number;
  file_type: string;
  original_filename: string;
  date_range: {
    start: string | null;
    end: string | null;
  };
}

interface FileUploadProps {
  onTransactionsImported?: () => void;
}

type UploadStatus = 'idle' | 'uploading' | 'processing' | 'preview' | 'saving' | 'success' | 'error';

function FileUpload({ onTransactionsImported }: FileUploadProps) {
  const [status, setStatus] = useState<UploadStatus>('idle');
  const [error, setError] = useState<string | null>(null);
  const [uploadId, setUploadId] = useState<number | null>(null);
  const [transactions, setTransactions] = useState<ExtractedTransaction[]>([]);
  const [summary, setSummary] = useState<UploadSummary | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectAll, setSelectAll] = useState(true);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const allowedTypes = [
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/pdf',
  ];
  const allowedExtensions = ['.csv', '.xlsx', '.xls', '.pdf'];

  const loadCategories = useCallback(async () => {
    try {
      const response = await categoriesAPI.getCategories();
      setCategories(response.data.categories || []);
    } catch (err) {
      console.error('Error loading categories:', err);
    }
  }, []);

  const handleUpload = async (file: File) => {
    setStatus('uploading');
    setError(null);

    try {
      // Load categories if not loaded
      if (categories.length === 0) {
        await loadCategories();
      }

      setStatus('processing');
      const response = await uploadAPI.uploadFile(file);
      
      const data = response.data;
      setUploadId(data.upload_id);
      setSummary(data.summary);
      
      // Mark all transactions as selected by default
      const transactionsWithSelection = data.transactions.map((t: ExtractedTransaction) => ({
        ...t,
        selected: true,
      }));
      setTransactions(transactionsWithSelection);
      setStatus('preview');
      
    } catch (err: unknown) {
      setStatus('error');
      const errorMessage = (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Failed to process file';
      setError(errorMessage);
    }
  };

  const handleFileSelect = (file: File) => {
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(extension)) {
      setError(`Invalid file type. Please upload: ${allowedExtensions.join(', ')}`);
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('File too large. Maximum size is 10MB.');
      return;
    }

    setSelectedFile(file);
    setError(null);
    handleUpload(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleConfirmImport = async () => {
    const selectedTransactions = transactions.filter(t => t.selected);
    
    if (selectedTransactions.length === 0) {
      setError('Please select at least one transaction to import');
      return;
    }

    setStatus('saving');
    setError(null);

    try {
      await uploadAPI.confirmTransactions(uploadId!, selectedTransactions as unknown as Record<string, unknown>[]);
      setStatus('success');
      
      if (onTransactionsImported) {
        onTransactionsImported();
      }
      
      // Reset after short delay
      setTimeout(() => {
        resetUpload();
      }, 2000);
      
    } catch (err: unknown) {
      setStatus('error');
      const errorMessage = (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Failed to save transactions';
      setError(errorMessage);
    }
  };

  const resetUpload = () => {
    setStatus('idle');
    setError(null);
    setUploadId(null);
    setTransactions([]);
    setSummary(null);
    setSelectedFile(null);
    setSelectAll(true);
    setEditingIndex(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const toggleSelectAll = () => {
    const newValue = !selectAll;
    setSelectAll(newValue);
    setTransactions(prev => prev.map(t => ({ ...t, selected: newValue })));
  };

  const toggleTransaction = (index: number) => {
    setTransactions(prev => {
      const updated = [...prev];
      updated[index] = { ...updated[index], selected: !updated[index].selected };
      return updated;
    });
  };

  const updateTransaction = (index: number, field: keyof ExtractedTransaction, value: unknown) => {
    setTransactions(prev => {
      const updated = [...prev];
      updated[index] = { ...updated[index], [field]: value };
      
      // If category changed, update category_id
      if (field === 'category_id') {
        const category = categories.find(c => c.id === value);
        if (category) {
          updated[index].suggested_category = category.name;
        }
      }
      
      return updated;
    });
  };

  const selectedCount = transactions.filter(t => t.selected).length;

  // Render upload zone
  if (status === 'idle' || status === 'error') {
    return (
      <Card>
        <CardContent>
          <Box
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            sx={{
              border: '2px dashed',
              borderColor: error ? 'error.main' : 'grey.300',
              borderRadius: 2,
              p: 4,
              textAlign: 'center',
              cursor: 'pointer',
              transition: 'all 0.2s',
              '&:hover': {
                borderColor: 'primary.main',
                bgcolor: 'grey.50',
              },
            }}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv,.xlsx,.xls,.pdf"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFileSelect(file);
              }}
              style={{ display: 'none' }}
            />
            
            <UploadIcon sx={{ fontSize: 48, color: 'grey.400', mb: 2 }} />
            
            <Typography variant="h6" gutterBottom>
              Upload Bank Statement
            </Typography>
            
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Drag & drop your file here, or click to browse
            </Typography>
            
            <Stack direction="row" spacing={1} justifyContent="center" sx={{ mb: 2 }}>
              <Chip label="CSV" size="small" variant="outlined" />
              <Chip label="Excel" size="small" variant="outlined" />
              <Chip label="PDF" size="small" variant="outlined" />
            </Stack>
            
            <Typography variant="caption" color="text.secondary">
              Max file size: 10MB
            </Typography>
          </Box>
          
          {error && (
            <Alert severity="error" sx={{ mt: 2 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}
        </CardContent>
      </Card>
    );
  }

  // Render uploading/processing state
  if (status === 'uploading' || status === 'processing') {
    return (
      <Card>
        <CardContent>
          <Stack spacing={2} alignItems="center" sx={{ py: 4 }}>
            <FileIcon sx={{ fontSize: 48, color: 'primary.main' }} />
            <Typography variant="h6">
              {status === 'uploading' ? 'Uploading...' : 'Processing file...'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {selectedFile?.name}
            </Typography>
            <Box sx={{ width: '100%', maxWidth: 300 }}>
              <LinearProgress />
            </Box>
            <Typography variant="caption" color="text.secondary">
              {status === 'processing' && 'Extracting transactions and categorizing with AI...'}
            </Typography>
          </Stack>
        </CardContent>
      </Card>
    );
  }

  // Render success state
  if (status === 'success') {
    return (
      <Card>
        <CardContent>
          <Stack spacing={2} alignItems="center" sx={{ py: 4 }}>
            <SuccessIcon sx={{ fontSize: 64, color: 'success.main' }} />
            <Typography variant="h6" color="success.main">
              Transactions Imported Successfully!
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {selectedCount} transactions have been added to your account.
            </Typography>
          </Stack>
        </CardContent>
      </Card>
    );
  }

  // Render preview state
  if (status === 'preview' || status === 'saving') {
    return (
      <Card>
        <CardContent>
          <Stack spacing={3}>
            {/* Header */}
            <Stack direction="row" justifyContent="space-between" alignItems="center">
              <Stack direction="row" alignItems="center" spacing={2}>
                <FileIcon color="primary" />
                <Box>
                  <Typography variant="h6">Review Extracted Transactions</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {summary?.original_filename}
                  </Typography>
                </Box>
              </Stack>
              <IconButton onClick={resetUpload} disabled={status === 'saving'}>
                <CloseIcon />
              </IconButton>
            </Stack>

            {/* Summary */}
            {summary && (
              <Stack direction="row" spacing={2} flexWrap="wrap">
                <Chip 
                  label={`${summary.cleaned_count} Transactions`} 
                  color="primary" 
                  variant="outlined" 
                />
                <Chip 
                  label={`Income: $${summary.total_income.toFixed(2)}`} 
                  color="success" 
                  variant="outlined" 
                />
                <Chip 
                  label={`Expenses: $${summary.total_expenses.toFixed(2)}`} 
                  color="error" 
                  variant="outlined" 
                />
                {summary.date_range.start && summary.date_range.end && (
                  <Chip 
                    label={`${summary.date_range.start} to ${summary.date_range.end}`} 
                    variant="outlined" 
                  />
                )}
              </Stack>
            )}

            {error && (
              <Alert severity="error" onClose={() => setError(null)}>
                {error}
              </Alert>
            )}

            {/* Transactions Table */}
            <TableContainer component={Paper} sx={{ maxHeight: 400 }}>
              <Table stickyHeader size="small">
                <TableHead>
                  <TableRow>
                    <TableCell padding="checkbox">
                      <Checkbox
                        checked={selectAll}
                        indeterminate={selectedCount > 0 && selectedCount < transactions.length}
                        onChange={toggleSelectAll}
                      />
                    </TableCell>
                    <TableCell>Date</TableCell>
                    <TableCell>Description</TableCell>
                    <TableCell>Merchant</TableCell>
                    <TableCell>Category</TableCell>
                    <TableCell align="right">Amount</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell align="center">Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {transactions.map((trans, index) => (
                    <TableRow 
                      key={index}
                      sx={{ 
                        opacity: trans.selected ? 1 : 0.5,
                        bgcolor: trans.selected ? 'inherit' : 'grey.50'
                      }}
                    >
                      <TableCell padding="checkbox">
                        <Checkbox
                          checked={trans.selected}
                          onChange={() => toggleTransaction(index)}
                        />
                      </TableCell>
                      <TableCell>
                        {new Date(trans.transaction_date).toLocaleDateString()}
                      </TableCell>
                      <TableCell sx={{ maxWidth: 200 }}>
                        <Tooltip title={trans.description}>
                          <Typography variant="body2" noWrap>
                            {trans.description || '-'}
                          </Typography>
                        </Tooltip>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" noWrap>
                          {trans.merchant || '-'}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        {editingIndex === index ? (
                          <FormControl size="small" sx={{ minWidth: 120 }}>
                            <Select
                              value={trans.category_id || ''}
                              onChange={(e) => updateTransaction(index, 'category_id', e.target.value)}
                            >
                              {categories
                                .filter(c => c.type === trans.type)
                                .map(cat => (
                                  <MenuItem key={cat.id} value={cat.id}>
                                    {cat.name}
                                  </MenuItem>
                                ))}
                            </Select>
                          </FormControl>
                        ) : (
                          <Stack direction="row" alignItems="center" spacing={1}>
                            <Chip
                              label={trans.suggested_category}
                              size="small"
                              variant="outlined"
                            />
                            {trans.category_confidence < 0.5 && (
                              <Tooltip title="Low confidence - please verify">
                                <ErrorIcon fontSize="small" color="warning" />
                              </Tooltip>
                            )}
                          </Stack>
                        )}
                      </TableCell>
                      <TableCell align="right">
                        <Typography
                          variant="body2"
                          sx={{
                            fontWeight: 600,
                            color: trans.type === 'income' ? 'success.main' : 'error.main'
                          }}
                        >
                          {trans.type === 'income' ? '+' : '-'}${trans.amount.toFixed(2)}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        {editingIndex === index ? (
                          <FormControl size="small" sx={{ minWidth: 100 }}>
                            <Select
                              value={trans.type}
                              onChange={(e) => updateTransaction(index, 'type', e.target.value)}
                            >
                              <MenuItem value="income">Income</MenuItem>
                              <MenuItem value="expense">Expense</MenuItem>
                            </Select>
                          </FormControl>
                        ) : (
                          <Chip
                            label={trans.type}
                            size="small"
                            color={trans.type === 'income' ? 'success' : 'error'}
                          />
                        )}
                      </TableCell>
                      <TableCell align="center">
                        {editingIndex === index ? (
                          <IconButton 
                            size="small" 
                            color="primary"
                            onClick={() => setEditingIndex(null)}
                          >
                            <SaveIcon fontSize="small" />
                          </IconButton>
                        ) : (
                          <IconButton 
                            size="small"
                            onClick={() => setEditingIndex(index)}
                          >
                            <EditIcon fontSize="small" />
                          </IconButton>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>

            {/* Actions */}
            <Stack direction="row" justifyContent="space-between" alignItems="center">
              <Typography variant="body2" color="text.secondary">
                {selectedCount} of {transactions.length} transactions selected
              </Typography>
              <Stack direction="row" spacing={2}>
                <Button 
                  variant="outlined" 
                  onClick={resetUpload}
                  disabled={status === 'saving'}
                >
                  Cancel
                </Button>
                <Button
                  variant="contained"
                  startIcon={status === 'saving' ? null : <SaveIcon />}
                  onClick={handleConfirmImport}
                  disabled={selectedCount === 0 || status === 'saving'}
                >
                  {status === 'saving' ? 'Saving...' : `Import ${selectedCount} Transactions`}
                </Button>
              </Stack>
            </Stack>
          </Stack>
        </CardContent>
      </Card>
    );
  }

  return null;
}

export default FileUpload;
