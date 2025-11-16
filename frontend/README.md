# Village Frontend

React-based frontend for The Village Project.

## Setup

```bash
npm install
npm run dev
```

## Features

- Dynamic 40x40 grid rendering
- Viewport optimization (only renders visible tiles)
- Tree click-to-cut interaction
- Resource tracking UI
- Pan/drag navigation

## Components

- **VillageGrid**: Main grid renderer with pan controls
- **Tile**: Individual tile component with background
- **Tree**: Interactive tree overlay with hover effects
- **ResourcePanel**: Top resource counter display

## Adding Custom Tree Asset

Place `tree.png` in `public/` folder and update `Tree.jsx` to use it instead of emojis.

