import React from "react";
import "./MobileWarning.css";
import logo from "../assets/promptly_logo.png";

const MobileWarning = () => {
  return (
    <div className="mobile-warning-container">
      <div className="mobile-warning-card">
        <div className="mobile-warning-header">
          <img src={logo} alt="Prompt.ly" className="mobile-warning-logo" />
          <h1>prompt.ly</h1>
        </div>
        <div className="mobile-warning-content">
          <p>prompt.ly is best displayed on a computer with a wide window.</p>
        </div>
      </div>
    </div>
  );
};

export default MobileWarning;

