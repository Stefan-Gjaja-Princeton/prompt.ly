/**
 * Unit tests for ConfirmationModal component
 */
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import ConfirmationModal from "../../components/ConfirmationModal";

describe("ConfirmationModal", () => {
  const defaultProps = {
    isOpen: true,
    title: "Confirm Action",
    message: "Are you sure?",
    onConfirm: jest.fn(),
    onCancel: jest.fn(),
  };

  it("should not render when isOpen is false", () => {
    render(<ConfirmationModal {...defaultProps} isOpen={false} />);
    expect(screen.queryByText("Confirm Action")).not.toBeInTheDocument();
  });

  it("should render when isOpen is true", () => {
    render(<ConfirmationModal {...defaultProps} />);
    expect(screen.getByText("Confirm Action")).toBeInTheDocument();
    expect(screen.getByText("Are you sure?")).toBeInTheDocument();
  });

  it("should call onConfirm when confirm button is clicked", () => {
    const onConfirm = jest.fn();
    render(<ConfirmationModal {...defaultProps} onConfirm={onConfirm} />);

    const confirmButton = screen.getByText("Confirm");
    fireEvent.click(confirmButton);

    expect(onConfirm).toHaveBeenCalledTimes(1);
  });

  it("should call onCancel when cancel button is clicked", () => {
    const onCancel = jest.fn();
    render(<ConfirmationModal {...defaultProps} onCancel={onCancel} />);

    const cancelButton = screen.getByText("Cancel");
    fireEvent.click(cancelButton);

    expect(onCancel).toHaveBeenCalledTimes(1);
  });

  it("should call onCancel when close button is clicked", () => {
    const onCancel = jest.fn();
    render(<ConfirmationModal {...defaultProps} onCancel={onCancel} />);

    const closeButton = screen.getByTitle("Close");
    fireEvent.click(closeButton);

    expect(onCancel).toHaveBeenCalledTimes(1);
  });

  it("should call onCancel when overlay is clicked", () => {
    const onCancel = jest.fn();
    render(<ConfirmationModal {...defaultProps} onCancel={onCancel} />);

    const overlay = screen.getByTestId("confirmation-modal-overlay");
    fireEvent.click(overlay);

    expect(onCancel).toHaveBeenCalledTimes(1);
  });

  it("should not call onCancel when modal content is clicked", () => {
    const onCancel = jest.fn();
    render(<ConfirmationModal {...defaultProps} onCancel={onCancel} />);

    const modalContent = screen.getByTestId("confirmation-modal-content");
    fireEvent.click(modalContent);

    expect(onCancel).not.toHaveBeenCalled();
  });

  it("should use custom confirm and cancel text", () => {
    render(
      <ConfirmationModal
        {...defaultProps}
        confirmText="Delete"
        cancelText="Keep"
      />
    );

    expect(screen.getByText("Delete")).toBeInTheDocument();
    expect(screen.getByText("Keep")).toBeInTheDocument();
  });

  it("should use custom title and message", () => {
    render(
      <ConfirmationModal
        {...defaultProps}
        title="Delete Conversation"
        message="This action cannot be undone."
      />
    );

    expect(screen.getByText("Delete Conversation")).toBeInTheDocument();
    expect(
      screen.getByText("This action cannot be undone.")
    ).toBeInTheDocument();
  });

  it("should use custom confirm button color", () => {
    render(
      <ConfirmationModal {...defaultProps} confirmButtonColor="#ff0000" />
    );

    const confirmButton = screen.getByText("Confirm");
    expect(confirmButton).toHaveStyle({ backgroundColor: "#ff0000" });
  });
});
