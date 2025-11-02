import React from "react";

/**
 * Enhanced markdown parser for chat messages
 * Supports: **bold**, *bold*, bullet lists (- or *), and numbered lists
 * @param {string} text - Text that may contain markdown
 * @returns {JSX.Element|string} - React element with markdown rendered
 */
export const renderMarkdown = (text) => {
  if (!text || typeof text !== "string") return text;

  // Split text into lines to handle lists
  const lines = text.split("\n");
  const processedLines = [];

  for (let line of lines) {
    // Check if line is a bullet point (starts with - or * followed by space)
    const bulletMatch = line.match(/^(\s*)([-*])\s+(.+)$/);
    if (bulletMatch) {
      const [, indent, bullet, content] = bulletMatch;
      const indentLevel = Math.floor(indent.length / 2); // Assume 2 spaces per indent level
      processedLines.push({
        type: "bullet",
        content: content,
        indentLevel: indentLevel,
        bullet: bullet === "-" ? "•" : "•", // Use bullet character
      });
      continue;
    }

    // Check if line is a numbered list item (starts with number. followed by space)
    const numberedMatch = line.match(/^(\s*)(\d+)\.\s+(.+)$/);
    if (numberedMatch) {
      const [, indent, number, content] = numberedMatch;
      const indentLevel = Math.floor(indent.length / 2);
      processedLines.push({
        type: "numbered",
        content: content,
        indentLevel: indentLevel,
        number: number,
      });
      continue;
    }

    // Regular text line (might contain bold formatting)
    processedLines.push({
      type: "text",
      content: line,
    });
  }

  // Render the processed lines
  const elements = [];
  let listItems = [];
  let listType = null;
  let listIndent = 0;

  processedLines.forEach((line, index) => {
    if (line.type === "bullet" || line.type === "numbered") {
      // If we're starting a new list or continuing the same type
      if (listType !== line.type || listIndent !== line.indentLevel) {
        // Close previous list if exists
        if (listItems.length > 0) {
          const ListTag = listType === "bullet" ? "ul" : "ol";
          elements.push(
            <ListTag key={`list-${elements.length}`} className="markdown-list">
              {listItems}
            </ListTag>
          );
          listItems = [];
        }
        listType = line.type;
        listIndent = line.indentLevel;
      }

      // Process content for bold text within list item
      const processedContent = processInlineFormatting(line.content);
      listItems.push(
        <li
          key={`item-${index}`}
          style={{ marginLeft: `${line.indentLevel * 20}px` }}
        >
          {processedContent}
        </li>
      );
    } else {
      // Close any open list
      if (listItems.length > 0) {
        const ListTag = listType === "bullet" ? "ul" : "ol";
        elements.push(
          <ListTag key={`list-${elements.length}`} className="markdown-list">
            {listItems}
          </ListTag>
        );
        listItems = [];
        listType = null;
        listIndent = 0;
      }

      // Process regular text line
      if (line.content.trim() || index === 0) {
        const processedContent = processInlineFormatting(line.content);
        if (line.content.trim()) {
          elements.push(
            <p key={`para-${index}`} style={{ margin: "0.5em 0" }}>
              {processedContent}
            </p>
          );
        } else {
          // Empty line for spacing
          elements.push(<br key={`br-${index}`} />);
        }
      }
    }
  });

  // Close any remaining open list
  if (listItems.length > 0) {
    const ListTag = listType === "bullet" ? "ul" : "ol";
    elements.push(
      <ListTag key={`list-${elements.length}`} className="markdown-list">
        {listItems}
      </ListTag>
    );
  }

  // If no markdown was processed, return original text
  if (elements.length === 0) {
    return text;
  }

  return <>{elements}</>;
};

/**
 * Process inline formatting (bold text) within a line
 * Supports **text** for bold (double asterisk)
 */
function processInlineFormatting(text) {
  if (!text) return text;

  // Use regex to find all **text** patterns
  const boldRegex = /\*\*(.+?)\*\*/g;
  const parts = [];
  let lastIndex = 0;
  let match;
  let hasFormatting = false;

  while ((match = boldRegex.exec(text)) !== null) {
    // Add text before the bold section
    if (match.index > lastIndex) {
      const beforeText = text.substring(lastIndex, match.index);
      if (beforeText) {
        parts.push({ text: beforeText, bold: false });
      }
    }

    // Add the bold section (without the ** markers)
    parts.push({ text: match[1], bold: true });
    hasFormatting = true;
    lastIndex = match.index + match[0].length;
  }

  // Add remaining text
  if (lastIndex < text.length) {
    const remaining = text.substring(lastIndex);
    if (remaining) {
      parts.push({ text: remaining, bold: false });
    }
  }

  // If no formatting found, return as plain text
  if (!hasFormatting || parts.length === 0) {
    return text;
  }

  // Render with React elements
  return parts.map((part, index) => {
    if (part.bold) {
      return <strong key={index}>{part.text}</strong>;
    }
    return <span key={index}>{part.text}</span>;
  });
}
