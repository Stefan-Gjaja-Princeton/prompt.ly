/**
 * Mascot Icon Selector
 *
 * To switch between icon options, uncomment the import and assignment for the icon you want:
 * - Option D: Friendly mascot (p as head with body)
 * - Option E: Chat-bubble character (chat bubble with p face inside)
 * - Option F: Monoline badge (circular badge with p face)
 *
 * Make sure only ONE icon is imported and assigned to PromptlyMascot at a time.
 */

// Option D: Friendly mascot — the "p" is the head
import IconOptionD from "./IconOptionD";

// Option E: Chat-bubble character with eyes in the "p" bowl
// import IconOptionE from "./IconOptionE";

// Option F: Monoline badge — bowl of the p doubles as a face
// import IconOptionF from "./IconOptionF";

// The active icon (change which one is assigned here):
const PromptlyMascot = IconOptionD;
// const PromptlyMascot = IconOptionE;
// const PromptlyMascot = IconOptionF;

export default PromptlyMascot;
