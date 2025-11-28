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
    return `<pre class="markdown-code-block"><code>${code}</code></pre>`;
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
