---
title: Folder Game
description: Version History
---

The game is [here](/folder)

# Version History

## 1. Initial Implementation (v0.1)

**Features:**

- Office-themed hidden object game
- Static folders with:
  - Department labels (HR, Finance, Engineering)
  - Document types (CONFIDENTIAL, Q4 REPORT)
- Rectangular click detection
- Life system (3 lives)

## 2. Draggable Folders (v0.2)

**Changes:**

- Added drag-and-drop functionality
- Folders scramble on new rounds
- Drop verification zone (bottom-right)
- Removed click penalties (only drop-zone checks)
- Issues:
  - `preventDefault` console warnings
  - Inconsistent drop detection

## 3. Circular Drop Detection (v0.3)

**Fixes/Improvements:**

- Replaced rectangular detection with **radius-based check**:
  ```javascript
  const distance = Math.sqrt(Math.pow(xDist, 2) + Math.pow(yDist, 2));
  ```
- Visual upgrades:

  - Circular drop zone (rounded-full)

  - Drag highlight effects

- Better mobile touch support

## Passive Event Fix (v0.4)

**Technical Improvements:**

- Fixed Chrome passive event warnings:

```javascript
window.addEventListener("touchmove", handler, { passive: false });
```

- Added CSS:

````css
touch-action: none;
Unified mouse/touch event handling```
````

## Proper Drop Zone Alignment (v0.5)

**Critical Fixes:**

- Corrected bottom-right positioning:

```javascript
left: 100 - zoneWidth; // True right-edge
top: 100 - zoneHeight; // True bottom-edge
```

- Fixed coordinate math:

- Container offset compensation

- Pixel/percentage conversion

- Enhanced visual feedback
