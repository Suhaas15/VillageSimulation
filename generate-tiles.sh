#!/bin/bash

# Generate all 5 tile types using Freepik API and apply to grid
# This takes about 60 seconds total (12 seconds per tile)

echo ""
echo "============================================================"
echo "🎨 GENERATING ALL TILES"
echo "============================================================"
echo ""

# Array of tile types
tiles=("grass" "dirt" "stone" "forest" "water")
total=${#tiles[@]}
count=0

for tile in "${tiles[@]}"; do
    count=$((count + 1))
    
    echo ""
    echo "============================================================"
    echo "🎨 TILE $count/$total: Generating $tile..."
    echo "============================================================"
    echo ""
    
    # Generate the tile
    response=$(curl -s -X POST http://localhost:5001/api/assets/generate/tile \
        -H "Content-Type: application/json" \
        -d "{\"tile_type\": \"$tile\"}")
    
    # Check if successful
    if echo "$response" | grep -q '"success":true'; then
        tiles_updated=$(echo "$response" | grep -o '"tiles_updated":[0-9]*' | cut -d: -f2)
        echo "✅ $tile tile generated and applied to $tiles_updated grid tiles!"
    else
        echo "❌ Failed to generate $tile tile"
        echo "Response: $response"
    fi
    
    # Wait 10 seconds between tiles (except after the last one)
    if [ $count -lt $total ]; then
        echo ""
        echo "⏳ Waiting 10 seconds before next tile..."
        sleep 10
    fi
done

echo ""
echo "============================================================"
echo "✅ ALL TILES GENERATED!"
echo "============================================================"
echo ""
echo "🎮 NEXT STEPS:"
echo "   1. Refresh your browser (Ctrl+R or Cmd+R)"
echo "   2. You should see the new tile textures!"
echo "   3. Pan around the map to see different tile types"
echo ""
echo "============================================================"
echo ""

