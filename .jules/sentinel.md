## 2025-06-13 - [DOM-based XSS in template literals]
**Vulnerability:** Frontend JavaScript constructed dynamic HTML using `.innerHTML` with template literals containing unescaped object properties (e.g. `node.label`, search results).
**Learning:** Even static-seeming data loaded from backend APIs or internal objects can be manipulated to trigger Cross-Site Scripting (XSS) if directly inserted into the DOM. This specific pattern was prevalent in `assets/scripts.js` and `assets/test_scripts_assets.js` when rendering UI components.
**Prevention:** Always wrap dynamic string values with an `escapeHTML()` sanitization function before interpolating them into strings meant for `.innerHTML`, or prefer using `.textContent` where HTML parsing is not required.

## 2025-06-13 - [DOM-based XSS in template literals]
**Vulnerability:** Frontend JavaScript constructed dynamic HTML using `.innerHTML` with template literals containing unescaped object properties (e.g. `node.label`, search results).
**Learning:** Even static-seeming data loaded from backend APIs or internal objects can be manipulated to trigger Cross-Site Scripting (XSS) if directly inserted into the DOM. This specific pattern was prevalent in `assets/scripts.js` and `assets/test_scripts_assets.js` when rendering UI components.
**Prevention:** Always wrap dynamic string values with an `escapeHTML()` sanitization function before interpolating them into strings meant for `.innerHTML`, or prefer using `.textContent` where HTML parsing is not required.
