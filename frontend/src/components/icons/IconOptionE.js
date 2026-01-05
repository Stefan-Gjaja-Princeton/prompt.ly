// IMPORTANT NOTE: This icon option was made by Cursor when I asked for specific mascots for my product.
import React from "react";

/**
 * Option E: Chat-bubble character with eyes in the "p" bowl
 * Chat bubble as body; interior lowercase p forms a face. Simple eyes + hint of a smile keep it minimalist.
 */
const IconOptionE = ({ size = 20, className = "", ...props }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="0 0 64 64"
      role="img"
      aria-labelledby="titleE descE"
      className={className}
      {...props}
    >
      <title id="titleE">prompt.ly icon — chat-bubble character</title>
      <desc id="descE">
        Chat bubble as body; interior lowercase p forms a face. Simple eyes +
        hint of a smile keep it minimalist.
      </desc>
      <g
        fill="none"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        {/* Bubble body */}
        <path d="M12 22a12 12 0 0 1 12-12h16a12 12 0 0 1 12 12v8a12 12 0 0 1-12 12H28l-8 8v-8h-4a12 12 0 0 1-12-12v-8z" />
        {/* p inside */}
        <line x1="26" y1="18" x2="26" y2="36" />
        <circle cx="36" cy="26" r="8" />
        {/* face in bowl */}
        <circle cx="33.5" cy="24.5" r="1.1" fill="currentColor" stroke="none" />
        <circle cx="38.5" cy="24.5" r="1.1" fill="currentColor" stroke="none" />
        <path d="M33 28c1.8 1.4 4.2 1.4 6 0" />
      </g>
    </svg>
  );
};

export default IconOptionE;
