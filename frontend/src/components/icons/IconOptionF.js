import React from "react";

/**
 * Option F: Monoline badge — bowl of the p doubles as a face
 * Circular badge; lowercase p with tiny eyes in the bowl for an approachable, anthropomorphic mark.
 */
const IconOptionF = ({ size = 20, className = "", ...props }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="0 0 64 64"
      role="img"
      aria-labelledby="titleF descF"
      className={className}
      {...props}
    >
      <title id="titleF">prompt.ly icon — monoline badge with face</title>
      <desc id="descF">
        Circular badge; lowercase p with tiny eyes in the bowl for an
        approachable, anthropomorphic mark.
      </desc>
      <g
        fill="none"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <circle cx="32" cy="32" r="29" />
        <line x1="22" y1="18" x2="22" y2="44" />
        <circle cx="34" cy="30" r="10" />
        <circle cx="30.5" cy="28.5" r="1.1" fill="currentColor" stroke="none" />
        <circle cx="37.5" cy="28.5" r="1.1" fill="currentColor" stroke="none" />
        <path d="M30 32c2 1.6 6 1.6 8 0" />
      </g>
    </svg>
  );
};

export default IconOptionF;
