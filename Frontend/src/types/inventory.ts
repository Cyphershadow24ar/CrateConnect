export interface InventoryItem {
  inventory_id: string;
  business_id: string;
  category_id: string;
  product_name: string;
  barcode: string | null;
  quantity: number | string;
  unit: string;
  purchase_date: string | null;
  expiry_date: string;
  created_at: string;
  updated_at: string;
}

export type TransactionType = 'ADDED' | 'UPDATED' | 'SOLD' | 'EXPIRED' | 'DONATED';

export interface TransactionCreate {
  business_id: string;
  inventory_id: string;
  transaction_type: TransactionType;
  quantity: number;
  reference?: string | null;
}

export interface TransactionResponse {
  transaction_id: string;
  business_id: string;
  inventory_id: string;
  transaction_type: TransactionType;
  quantity: number | string;
  reference: string | null;
  created_at: string;
}
