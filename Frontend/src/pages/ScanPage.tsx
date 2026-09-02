import React, { useState } from 'react';
import { BarcodeScanner } from '../components/BarcodeScanner';
import { inventoryService } from '../services/inventoryService';
import type { InventoryItem, TransactionType } from '../types/inventory';

// Demo barcodes provided in specification for quick testing
const DEMO_BARCODES = [
  { barcode: '8901234567890', name: 'Fresh Milk' },
  { barcode: '8901234567891', name: 'Bread' },
  { barcode: '8901234567892', name: 'Fresh Spinach' },
  { barcode: '8901234567893', name: 'Frozen Peas' },
  { barcode: '8901234567894', name: 'Rice Bag' },
  { barcode: '8901234567895', name: 'Orange Juice' },
  { barcode: '8901234567901', name: 'Greek Yogurt' },
  { barcode: '8901234567902', name: 'Apple Juice' },
  { barcode: '8901234567903', name: 'Wheat Flour' },
];

export const ScanPage: React.FC = () => {
  const [isScannerOpen, setIsScannerOpen] = useState(false);
  const [scannedBarcode, setScannedBarcode] = useState<string | null>(null);
  const [item, setItem] = useState<InventoryItem | null>(null);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [notFoundBarcode, setNotFoundBarcode] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Stock Adjustment Form State
  const [selectedAction, setSelectedAction] = useState<TransactionType>('SOLD');
  const [quantityInput, setQuantityInput] = useState<string>('1');

  const handleLookup = async (barcode: string) => {
    setLoading(true);
    setErrorMessage(null);
    setSuccessMessage(null);
    setNotFoundBarcode(null);
    setItem(null);
    setScannedBarcode(barcode);

    try {
      const foundItem = await inventoryService.lookupByBarcode(barcode);
      setItem(foundItem);
      // Default suggested quantity
      setQuantityInput('1');
    } catch (err: any) {
      if (err.response?.status === 404) {
        setNotFoundBarcode(barcode);
      } else {
        setErrorMessage(
          err.response?.data?.detail || err.message || 'Failed to lookup barcode. Please check connection.'
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const handleScanSuccess = (barcode: string) => {
    setIsScannerOpen(false);
    handleLookup(barcode);
  };

  const handleStockUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!item) return;

    const qty = parseFloat(quantityInput);
    if (isNaN(qty) || qty <= 0) {
      setErrorMessage('Please enter a valid quantity greater than 0.');
      return;
    }

    const currentQty = typeof item.quantity === 'string' ? parseFloat(item.quantity) : item.quantity;
    if (selectedAction === 'SOLD' && qty > currentQty) {
      setErrorMessage(
        `Insufficient stock. Available: ${currentQty} ${item.unit}, attempted to sell: ${qty} ${item.unit}.`
      );
      return;
    }

    setActionLoading(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      // Record transaction using item's actual business_id and inventory_id
      await inventoryService.createTransaction({
        business_id: item.business_id,
        inventory_id: item.inventory_id,
        transaction_type: selectedAction,
        quantity: qty,
        reference: `RAPID-${selectedAction}-SCAN`,
      });

      // Refresh item state to get updated server quantity
      const refreshedItem = await inventoryService.getInventory(item.inventory_id);
      setItem(refreshedItem);

      const actionText = selectedAction === 'SOLD' ? 'Deducted' : 'Added';
      setSuccessMessage(
        `Successfully ${actionText.toLowerCase()} ${qty} ${item.unit} for ${item.product_name}. New stock: ${refreshedItem.quantity} ${refreshedItem.unit}.`
      );
      setQuantityInput('1');
    } catch (err: any) {
      setErrorMessage(
        err.response?.data?.detail ||
          err.response?.data?.error?.message ||
          err.message ||
          'Failed to record stock transaction.'
      );
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-16 pt-6 text-slate-900">
      <div className="mx-auto max-w-2xl px-4 sm:px-6">
        {/* Header Section */}
        <div className="mb-6 flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
                Barcode & QR Scanner
              </h1>
              <p className="text-sm text-slate-500">
                Scan inventory items for instant lookup and rapid stock adjustment.
              </p>
            </div>
            <button
              onClick={() => setIsScannerOpen(true)}
              className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-700 active:scale-95"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"
                />
              </svg>
              Scan Code
            </button>
          </div>
        </div>

        {/* Scanner Modal */}
        {isScannerOpen && (
          <BarcodeScanner
            onScan={handleScanSuccess}
            onError={(err) => setErrorMessage(err)}
            onClose={() => setIsScannerOpen(false)}
          />
        )}

        {/* Global Notifications */}
        {errorMessage && (
          <div className="mb-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 flex items-start justify-between">
            <div>
              <strong className="font-semibold">Error: </strong>
              <span>{errorMessage}</span>
            </div>
            <button
              onClick={() => setErrorMessage(null)}
              className="ml-2 font-bold text-red-600 hover:text-red-800"
            >
              ✕
            </button>
          </div>
        )}

        {successMessage && (
          <div className="mb-4 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800 flex items-start justify-between">
            <div>
              <strong className="font-semibold">Success: </strong>
              <span>{successMessage}</span>
            </div>
            <button
              onClick={() => setSuccessMessage(null)}
              className="ml-2 font-bold text-emerald-600 hover:text-emerald-800"
            >
              ✕
            </button>
          </div>
        )}

        {/* Loading Spinner */}
        {loading && (
          <div className="my-8 flex flex-col items-center justify-center gap-2 text-slate-500">
            <div className="h-8 w-8 animate-spin rounded-full border-3 border-emerald-600 border-t-transparent" />
            <p className="text-sm">Looking up item details...</p>
          </div>
        )}

        {/* Not Found State */}
        {notFoundBarcode && !loading && (
          <div className="my-6 rounded-2xl border border-amber-200 bg-amber-50/70 p-6 text-center shadow-sm">
            <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-amber-100 text-xl text-amber-600">
              🔍
            </div>
            <h3 className="text-base font-semibold text-amber-900">Item Not Found</h3>
            <p className="mt-1 text-sm text-amber-700">
              No inventory item found with barcode{' '}
              <code className="rounded bg-amber-200/60 px-1.5 py-0.5 font-mono text-xs font-bold text-amber-900">
                {notFoundBarcode}
              </code>
            </p>
            <div className="mt-4 flex justify-center gap-3">
              <button
                onClick={() => setIsScannerOpen(true)}
                className="rounded-xl bg-amber-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-amber-700"
              >
                Scan Another Code
              </button>
              <button
                onClick={() => setNotFoundBarcode(null)}
                className="rounded-xl border border-amber-300 bg-white px-4 py-2 text-sm font-semibold text-amber-900 hover:bg-amber-50"
              >
                Dismiss
              </button>
            </div>
          </div>
        )}

        {/* Scanned Item Details & Rapid Stock Update Card */}
        {item && !loading && (
          <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            {/* Item Card Header */}
            <div className="border-b border-slate-100 bg-slate-50/80 px-6 py-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <span className="inline-block rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800 uppercase tracking-wide">
                    Verified Item
                  </span>
                  <h2 className="mt-1 text-xl font-bold text-slate-900">{item.product_name}</h2>
                </div>
                <div className="text-right">
                  <span className="text-xs font-medium text-slate-400">Current Stock</span>
                  <div className="text-2xl font-black text-emerald-700">
                    {item.quantity}{' '}
                    <span className="text-sm font-normal text-slate-500">{item.unit}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Metadata Grid */}
            <div className="grid grid-cols-2 gap-4 border-b border-slate-100 px-6 py-4 sm:grid-cols-4">
              <div>
                <dt className="text-xs font-medium text-slate-400">Barcode</dt>
                <dd className="mt-0.5 font-mono text-xs font-semibold text-slate-700">
                  {item.barcode || 'N/A'}
                </dd>
              </div>
              <div>
                <dt className="text-xs font-medium text-slate-400">Expiry Date</dt>
                <dd className="mt-0.5 text-xs font-semibold text-slate-700">
                  {item.expiry_date}
                </dd>
              </div>
              <div>
                <dt className="text-xs font-medium text-slate-400">Purchase Date</dt>
                <dd className="mt-0.5 text-xs font-semibold text-slate-700">
                  {item.purchase_date || 'N/A'}
                </dd>
              </div>
              <div>
                <dt className="text-xs font-medium text-slate-400">Unit</dt>
                <dd className="mt-0.5 text-xs font-semibold text-slate-700">
                  {item.unit}
                </dd>
              </div>
            </div>

            {/* Rapid Stock Adjustment Section */}
            <form onSubmit={handleStockUpdate} className="p-6">
              <h3 className="text-sm font-semibold text-slate-900">Rapid Stock Update</h3>
              <p className="mt-0.5 text-xs text-slate-500">
                Adjust inventory by creating an audit-tracked transaction.
              </p>

              {/* Action Buttons */}
              <div className="mt-4 grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setSelectedAction('SOLD')}
                  className={`flex flex-col items-center justify-center rounded-xl border p-3 text-center transition ${
                    selectedAction === 'SOLD'
                      ? 'border-red-500 bg-red-50 text-red-800 shadow-sm ring-1 ring-red-500'
                      : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <span className="text-lg">🛒</span>
                  <span className="mt-1 text-sm font-semibold">Sell Stock (SOLD)</span>
                  <span className="text-xs text-slate-500">Deducts quantity</span>
                </button>

                <button
                  type="button"
                  onClick={() => setSelectedAction('ADDED')}
                  className={`flex flex-col items-center justify-center rounded-xl border p-3 text-center transition ${
                    selectedAction === 'ADDED'
                      ? 'border-emerald-500 bg-emerald-50 text-emerald-800 shadow-sm ring-1 ring-emerald-500'
                      : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <span className="text-lg">📦</span>
                  <span className="mt-1 text-sm font-semibold">Add Stock (ADDED)</span>
                  <span className="text-xs text-slate-500">Increases quantity</span>
                </button>
              </div>

              {/* Quantity Input */}
              <div className="mt-4">
                <label htmlFor="quantity" className="block text-xs font-semibold text-slate-700">
                  Quantity ({item.unit})
                </label>
                <div className="mt-1 flex gap-2">
                  <input
                    id="quantity"
                    type="number"
                    min="0.001"
                    step="any"
                    value={quantityInput}
                    onChange={(e) => setQuantityInput(e.target.value)}
                    required
                    className="block w-full rounded-xl border border-slate-300 bg-white px-3.5 py-2.5 text-sm font-medium text-slate-900 shadow-sm focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                  />
                  {/* Quick increment presets */}
                  <div className="flex gap-1">
                    {[1, 5, 10].map((inc) => (
                      <button
                        key={inc}
                        type="button"
                        onClick={() => setQuantityInput(String(inc))}
                        className="rounded-lg border border-slate-200 bg-slate-50 px-2.5 text-xs font-semibold text-slate-600 hover:bg-slate-100"
                      >
                        +{inc}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Submit Button */}
              <div className="mt-5 flex items-center justify-between gap-3">
                <button
                  type="submit"
                  disabled={actionLoading}
                  className={`w-full rounded-xl py-3 text-sm font-bold text-white shadow-sm transition active:scale-98 disabled:opacity-50 ${
                    selectedAction === 'SOLD'
                      ? 'bg-red-600 hover:bg-red-700'
                      : 'bg-emerald-600 hover:bg-emerald-700'
                  }`}
                >
                  {actionLoading
                    ? 'Updating Stock...'
                    : selectedAction === 'SOLD'
                    ? `Confirm Sale (-${quantityInput || 0} ${item.unit})`
                    : `Confirm Restock (+${quantityInput || 0} ${item.unit})`}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Empty State / Prompt to Scan */}
        {!item && !loading && !notFoundBarcode && (
          <div className="mt-8 rounded-2xl border-2 border-dashed border-slate-300 p-8 text-center">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-100 text-2xl text-emerald-600">
              📷
            </div>
            <h3 className="mt-3 text-base font-semibold text-slate-800">No item selected</h3>
            <p className="mt-1 text-sm text-slate-500">
              Click &quot;Scan Code&quot; to open the camera, or choose a demo barcode below.
            </p>
            <div className="mt-5">
              <button
                onClick={() => setIsScannerOpen(true)}
                className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-emerald-700"
              >
                Open Camera Scanner
              </button>
            </div>
          </div>
        )}

        {/* Demo Barcodes Quick Selector */}
        <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Quick Test Barcodes (Click to Test)
          </h4>
          <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-3">
            {DEMO_BARCODES.map((d) => (
              <button
                key={d.barcode}
                type="button"
                onClick={() => handleLookup(d.barcode)}
                className={`flex flex-col items-start rounded-xl border p-2.5 text-left transition hover:border-emerald-500 hover:bg-emerald-50/50 ${
                  scannedBarcode === d.barcode
                    ? 'border-emerald-500 bg-emerald-50 ring-1 ring-emerald-500'
                    : 'border-slate-100 bg-slate-50/50'
                }`}
              >
                <span className="text-xs font-bold text-slate-800">{d.name}</span>
                <span className="font-mono text-[10px] text-slate-500">{d.barcode}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
