#!/bin/bash
# Clean database files to avoid permission issues
# This will force the system to regenerate databases with correct permissions

set -e

echo "DeepWiki Database Cleanup Script"
echo "================================="
echo ""
echo "⚠️  WARNING: This will delete all cached databases."
echo "    Repositories will need to be re-embedded on next use."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if ~/.adalflow/databases exists and has root-owned files
if [ -d "$HOME/.adalflow/databases" ]; then
    echo -e "${YELLOW}Checking for permission issues...${NC}"

    # Check if there are any root-owned files
    if sudo -n ls "$HOME/.adalflow/databases" >/dev/null 2>&1; then
        # We can use sudo without password
        ROOT_FILES=$(sudo find "$HOME/.adalflow/databases" -user root 2>/dev/null || true)

        if [ -n "$ROOT_FILES" ]; then
            echo -e "${RED}Found root-owned database files:${NC}"
            echo "$ROOT_FILES"
            echo ""
            echo "Attempting to remove them..."
            sudo rm -f "$HOME/.adalflow/databases"/*.pkl
            echo -e "${GREEN}✓ Removed root-owned database files${NC}"
        else
            echo -e "${GREEN}No permission issues found${NC}"
        fi
    else
        # Sudo requires password, try without sudo for user-owned files
        echo -e "${YELLOW}Cannot check with sudo (password required)${NC}"
        echo "Attempting to clean user-owned files only..."
        rm -f "$HOME/.adalflow/databases"/*.pkl 2>/dev/null || echo "Some files require sudo to remove"
    fi
else
    echo -e "${YELLOW}~/.adalflow/databases does not exist${NC}"
fi

echo ""
echo -e "${GREEN}Database cleanup complete!${NC}"
echo ""
echo "Note: Databases will be regenerated on next use with correct permissions."
