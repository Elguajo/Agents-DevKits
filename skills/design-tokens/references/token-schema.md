# Token-layer contract

Use three layers where the project benefits from them:

- **Primitive:** raw, reusable values such as palette steps, spacing scale, or durations. Application components do not consume these directly.
- **Semantic:** intent-based roles such as primary action, page surface, primary text, focus ring, or danger feedback. Theme modes usually override this layer.
- **Component:** narrowly scoped aliases that document how a reusable component consumes semantic roles.

Prefer a documented schema such as DTCG when the project needs portable tooling. Preserve alias resolution, descriptions, and stable identifiers. Treat removed or renamed public tokens as compatibility changes.
