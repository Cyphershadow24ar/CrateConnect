import { api } from './api';
import type { InventoryItem, TransactionCreate, TransactionResponse } from '../types/inventory';

export const inventoryService = {
  /**
   * Look up an inventory item by barcode within the current business context.
   */
  async lookupByBarcode(barcode: string): Promise<InventoryItem> {
    const response = await api.get<InventoryItem>(`/inventory/barcode/${encodeURIComponent(barcode)}`);
    return response.data;
  },

  /**
   * Look up an inventory item by ID.
   */
  async getInventory(inventoryId: string): Promise<InventoryItem> {
    const response = await api.get<InventoryItem>(`/inventory/${inventoryId}`);
    return response.data;
  },

  /**
   * Fetch all inventory items (optionally filtered).
   */
  async listInventory(): Promise<InventoryItem[]> {
    const response = await api.get<InventoryItem[]>('/inventory');
    return response.data;
  },

  /**
   * Record an inventory transaction (rapid stock update e.g. SOLD or ADDED).
   */
  async createTransaction(payload: TransactionCreate): Promise<TransactionResponse> {
    const response = await api.post<TransactionResponse>('/transactions', payload);
    return response.data;
  },
};
