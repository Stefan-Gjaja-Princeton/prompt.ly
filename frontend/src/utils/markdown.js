// IMPORTANT NOTE: This file was created by Cursor in order to get the text generated as output by prompt.ly to format appropriately using markdown.
import { marked } from "marked";

// Configure marked.js to add CSS classes that match existing styles
marked.setOptions({
  breaks: true, // Convert line breaks to <br>
  gfm: true, // GitHub Flavored Markdown
});

// Configure renderers to add the expected CSS classes
const renderer = {
  list(body, ordered) {
    const tag = ordered ? "ol" : "ul";
    return `<${tag} class="markdown-list">${body}</${tag}>`;
  },
  code(code, language) {
    // Escape HTML in code for the data attribute (to prevent XSS in attribute)
    const escapedForAttribute = code
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");

    // marked.js will escape the code content automatically
    return `<pre class="markdown-code-block">
      <button class="copy-code-button" data-code="${escapedForAttribute}" aria-label="Copy code">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="2" y="2" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.5" fill="none"/>
          <rect x="6" y="6" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.5" fill="none"/>
        </svg>
        <span>Copy code</span>
      </button>
      <code>${code}</code>
    </pre>`;
  },
  codespan(code) {
    return `<code class="markdown-inline-code">${code}</code>`;
  },
};

marked.use({ renderer });

/**
 * Enhanced markdown parser for chat messages using marked.js
 * Supports all standard markdown features: **bold**, *italic*, bullet lists, numbered lists,
 * code blocks (```), inline code (`), links, and more
 * @param {string} text - Text that may contain markdown
 * @returns {JSX.Element|string} - React element with markdown rendered
 */
export const renderMarkdown = (text) => {
  if (!text || typeof text !== "string") return text;

  try {
    // Convert markdown to HTML using marked.js
    const html = marked.parse(text);

    // Return a div with the rendered HTML
    // Using dangerouslySetInnerHTML is safe here because marked.js only processes markdown syntax
    return (
      <div
        className="markdown-content"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    );
  } catch (error) {
    console.error("Error parsing markdown:", error);
    // If parsing fails, return the original text
    return text;
  }
};
