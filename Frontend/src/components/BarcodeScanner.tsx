import React, { useEffect, useRef, useState } from 'react';
import { BrowserMultiFormatReader, type IScannerControls } from '@zxing/browser';

export interface BarcodeScannerProps {
  onScan: (barcode: string) => void;
  onError?: (errorMessage: string) => void;
  onClose?: () => void;
}

export const BarcodeScanner: React.FC<BarcodeScannerProps> = ({
  onScan,
  onError,
  onClose,
}) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const controlsRef = useRef<IScannerControls | null>(null);
  const [cameraState, setCameraState] = useState<'requesting' | 'active' | 'error'>('requesting');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [manualBarcode, setManualBarcode] = useState('');
  const [devices, setDevices] = useState<MediaDeviceInfo[]>([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState<string>('');

  // Enumerate cameras
  useEffect(() => {
    async function getCameras() {
      try {
        if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
          return;
        }
        const devList = await navigator.mediaDevices.enumerateDevices();
        const videoInputs = devList.filter((d) => d.kind === 'videoinput');
        setDevices(videoInputs);
        if (videoInputs.length > 0) {
          setSelectedDeviceId((currentId) => {
            if (currentId) return currentId;
            const backCam = videoInputs.find(
              (d) =>
                d.label.toLowerCase().includes('back') ||
                d.label.toLowerCase().includes('rear') ||
                d.label.toLowerCase().includes('environment')
            );
            return backCam ? backCam.deviceId : videoInputs[0].deviceId;
          });
        }
      } catch {
        // Non-fatal, decodeFromConstraints will use default
      }
    }
    getCameras();
  }, []);

  // Initialize and run the scanner
  useEffect(() => {
    let isCancelled = false;
    const codeReader = new BrowserMultiFormatReader();

    async function startScanning() {
      if (!videoRef.current) return;
      setCameraState('requesting');
      setErrorMessage(null);

      try {
        // Stop any previous active scanner controls
        if (controlsRef.current) {
          controlsRef.current.stop();
          controlsRef.current = null;
        }

        const constraints: MediaStreamConstraints = {
          video: selectedDeviceId
            ? { deviceId: { exact: selectedDeviceId } }
            : { facingMode: { ideal: 'environment' } },
        };

        const controls = await codeReader.decodeFromConstraints(
          constraints,
          videoRef.current,
          (result, error) => {
            if (isCancelled) return;

            if (result) {
              const text = result.getText();
              if (text && text.trim().length > 0) {
                // Stop camera immediately on successful scan
                try {
                  controls.stop();
                } catch {
                  // Ignore
                }
                controlsRef.current = null;
                onScan(text.trim());
              }
            }

            // Note: ZXing continuously fires NotFoundException on every video frame
            // without a barcode. We deliberately do NOT log or show those to avoid false errors.
            if (error && error.name !== 'NotFoundException') {
              // Only notify about genuine device/stream failure
              if (
                error.name === 'NotAllowedError' ||
                error.name === 'NotFoundError' ||
                error.name === 'NotReadableError'
              ) {
                const msg = `Camera error: ${error.message || error.name}`;
                setErrorMessage(msg);
                setCameraState('error');
                onError?.(msg);
              }
            }
          }
        );

        if (!isCancelled) {
          controlsRef.current = controls;
          setCameraState('active');
        } else {
          controls.stop();
        }
      } catch (err: unknown) {
        if (isCancelled) return;
        let humanMsg = 'Unable to access camera.';
        if (err instanceof Error) {
          if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
            humanMsg = 'Camera permission was denied. Please allow camera access in your browser settings.';
          } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
            humanMsg = 'No camera device found on this device.';
          } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
            humanMsg = 'Camera is in use by another application or tab.';
          } else {
            humanMsg = err.message || humanMsg;
          }
        }
        setErrorMessage(humanMsg);
        setCameraState('error');
        onError?.(humanMsg);
      }
    }

    const videoEl = videoRef.current;

    startScanning();

    return () => {
      isCancelled = true;
      if (controlsRef.current) {
        try {
          controlsRef.current.stop();
        } catch {
          // Ignore cleanup errors
        }
        controlsRef.current = null;
      }
      if (videoEl) {
        const stream = videoEl.srcObject as MediaStream | null;
        if (stream) {
          stream.getTracks().forEach((track) => track.stop());
          videoEl.srcObject = null;
        }
      }
    };
  }, [selectedDeviceId, onScan, onError]);

  const handleManualSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (manualBarcode.trim()) {
      if (controlsRef.current) {
        try {
          controlsRef.current.stop();
        } catch {
          // Ignore
        }
      }
      onScan(manualBarcode.trim());
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm">
      <div className="relative flex max-h-[95vh] w-full max-w-lg flex-col overflow-hidden rounded-2xl bg-neutral-900 shadow-2xl ring-1 ring-white/10">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-neutral-800 px-5 py-4">
          <div className="flex items-center gap-2">
            <span className="flex h-3 w-3 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <h2 className="text-lg font-semibold text-white">Scan Barcode or QR</h2>
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="rounded-lg p-2 text-neutral-400 hover:bg-neutral-800 hover:text-white transition"
              aria-label="Close scanner"
            >
              ✕
            </button>
          )}
        </div>

        {/* Video / Camera Viewport */}
        <div className="relative flex aspect-video w-full items-center justify-center overflow-hidden bg-black sm:aspect-square">
          <video
            ref={videoRef}
            className={`h-full w-full object-cover transition-opacity duration-300 ${
              cameraState === 'active' ? 'opacity-100' : 'opacity-0'
            }`}
            muted
            playsInline
            autoPlay
          />

          {/* Reticle / Viewfinder Overlay */}
          {cameraState === 'active' && (
            <div className="pointer-events-none absolute inset-0 flex items-center justify-center p-8">
              <div className="relative aspect-square w-64 max-w-full rounded-xl border-2 border-dashed border-emerald-400/80 shadow-[0_0_20px_rgba(16,185,129,0.3)]">
                {/* Corner Accents */}
                <div className="absolute -left-1 -top-1 h-5 w-5 border-l-4 border-t-4 border-emerald-400" />
                <div className="absolute -right-1 -top-1 h-5 w-5 border-r-4 border-t-4 border-emerald-400" />
                <div className="absolute -bottom-1 -left-1 h-5 w-5 border-b-4 border-l-4 border-emerald-400" />
                <div className="absolute -bottom-1 -right-1 h-5 w-5 border-b-4 border-r-4 border-emerald-400" />
                {/* Animated Laser Scan Bar */}
                <div className="absolute left-2 right-2 h-0.5 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_8px_#34d399] animate-bounce" />
              </div>
            </div>
          )}

          {/* State Overlays */}
          {cameraState === 'requesting' && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-neutral-900/90 text-neutral-300">
              <div className="h-8 w-8 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
              <p className="text-sm font-medium">Starting camera...</p>
            </div>
          )}

          {cameraState === 'error' && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 p-6 text-center bg-neutral-900 text-neutral-200">
              <div className="rounded-full bg-red-500/20 p-3 text-red-400 text-2xl">📷</div>
              <p className="text-sm font-medium text-red-300">{errorMessage}</p>
              <p className="text-xs text-neutral-400">
                You can manually type the barcode below to continue.
              </p>
            </div>
          )}
        </div>

        {/* Footer Controls & Manual Entry */}
        <div className="flex flex-col gap-4 border-t border-neutral-800 bg-neutral-900/95 p-4">
          {/* Camera switcher if multiple cameras exist */}
          {devices.length > 1 && (
            <div className="flex items-center gap-2">
              <label htmlFor="cameraSelect" className="text-xs font-medium text-neutral-400">
                Camera:
              </label>
              <select
                id="cameraSelect"
                value={selectedDeviceId}
                onChange={(e) => setSelectedDeviceId(e.target.value)}
                className="flex-1 rounded-lg border border-neutral-700 bg-neutral-800 px-2 py-1 text-xs text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
              >
                {devices.map((d, i) => (
                  <option key={d.deviceId || i} value={d.deviceId}>
                    {d.label || `Camera ${i + 1}`}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Instructions */}
          <p className="text-center text-xs text-neutral-400">
            Align barcode or QR code inside the frame to scan automatically.
          </p>

          {/* Manual Input Fallback */}
          <form onSubmit={handleManualSubmit} className="flex gap-2">
            <input
              type="text"
              placeholder="Or enter barcode manually..."
              value={manualBarcode}
              onChange={(e) => setManualBarcode(e.target.value)}
              className="flex-1 rounded-xl border border-neutral-700 bg-neutral-800 px-3.5 py-2 text-sm text-white placeholder-neutral-500 focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
            <button
              type="submit"
              disabled={!manualBarcode.trim()}
              className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-500 disabled:opacity-50"
            >
              Lookup
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
