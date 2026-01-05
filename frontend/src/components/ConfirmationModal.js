import React from "react";
import { AlertTriangle, X } from "lucide-react";
import "./ConfirmationModal.css";

const ConfirmationModal = ({
  isOpen,
  title = "Confirm Action",
  message,
  confirmText = "Confirm",
  cancelText = "Cancel",
  onConfirm,
  onCancel,
  confirmButtonColor = "#d32f2f", // Default red for delete actions
}) => {
  if (!isOpen) return null;

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onCancel();
    }
  };

  return (
    <div className="confirmation-modal-overlay" onClick={handleOverlayClick}>
      <div
        className="confirmation-modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="confirmation-modal-header">
          <div className="confirmation-modal-title">
            <AlertTriangle size={24} className="confirmation-icon" />
            <h2>{title}</h2>
          </div>
          <button
            className="confirmation-modal-close"
            onClick={onCancel}
            title="Close"
          >
            <X size={18} />
          </button>
        </div>

        <div className="confirmation-modal-body">
          <p className="confirmation-message">{message}</p>
        </div>

        <div className="confirmation-modal-footer">
          <button
            className="confirmation-button cancel-button"
            onClick={onCancel}
          >
            {cancelText}
          </button>
          <button
            className="confirmation-button confirm-button"
            onClick={onConfirm}
            style={{ backgroundColor: confirmButtonColor }}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationModal;

