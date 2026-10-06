"use strict";

/**
 * Local ESLint rule template.
 * Copy into the project's existing ESLint config. Does not install ESLint.
 *
 * Replace BANNED_NAME with the identifier the constraint forbids.
 */

module.exports = {
  meta: {
    type: "problem",
    docs: { description: "Disallow a banned identifier. See CONSTRAINTS.md." },
    schema: [],
  },
  create(context) {
    return {
      Identifier(node) {
        if (node.name === "BANNED_NAME") {
          context.report({
            node,
            message: "BANNED_NAME is constrained. See CONSTRAINTS.md.",
          });
        }
      },
    };
  },
};
