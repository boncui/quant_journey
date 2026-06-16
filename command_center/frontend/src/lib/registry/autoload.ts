/** The "add a folder, done" mechanism: eagerly import every panel index so each calls
 *  registerPanel() as a side effect. Importing this once (in main.tsx) populates the registry. */
const modules = import.meta.glob("../../panels/**/index.ts", { eager: true });

export const PANEL_COUNT = Object.keys(modules).length;
