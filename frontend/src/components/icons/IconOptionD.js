// IMPORTANT NOTE: This icon option was made by Cursor when I asked for specific mascots for my product.
import React from "react";

/**
 * Option D: Friendly mascot — the "p" is the head
 * Minimal anthropomorphic mascot: lowercase p as head with simple face; tiny body hints at a helpful assistant.
 */
const IconOptionD = ({ size = 20, className = "", ...props }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="16 10 32 36"
      role="img"
      aria-labelledby="titleD descD"
      className={className}
      {...props}
    >
      <title id="titleD">prompt.ly icon — friendly mascot p</title>
      <desc id="descD">
        Minimal anthropomorphic mascot: lowercase p as head with simple face;
        tiny body hints at a helpful assistant.
      </desc>
      <g
        fill="none"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        {/* Head as "p" bowl */}
        <line x1="24" y1="14" x2="24" y2="34" />
        <circle cx="34" cy="24" r="10" />
        {/* Face (subtle) */}
        <circle cx="30.5" cy="22" r="1.2" fill="currentColor" stroke="none" />
        <circle cx="37.5" cy="22" r="1.2" fill="currentColor" stroke="none" />
        <path d="M30 26c2 2 6 2 8 0" />
        {/* Tiny body/arms */}
        <path d="M24 34c0 6 4 10 10 10s10-4 10-10" />
        <path d="M26 40l-4 4M42 40l4 4" />
      </g>
    </svg>
  );
};

export default IconOptionD;
