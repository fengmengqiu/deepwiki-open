#!/bin/bash
# Fix file permissions for DeepWiki development environment
# This script fixes common permission issues when switching between Docker and local development

set -e

echo "DeepWiki Permission Fix Script"
echo "==============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get current user
CURRENT_USER=$(whoami)

echo "Current user: $CURRENT_USER"
echo ""

# Fix ~/.adalflow directory permissions
if [ -d "$HOME/.adalflow" ]; then
    echo -e "${YELLOW}Fixing permissions for ~/.adalflow/${NC}"
    sudo chown -R "$CURRENT_USER":"$CURRENT_USER" "$HOME/.adalflow"
    echo -e "${GREEN}✓ Fixed ~/.adalflow permissions${NC}"
else
    echo -e "${YELLOW}~/.adalflow directory does not exist, skipping...${NC}"
fi

# Fix api/logs directory permissions
if [ -d "api/logs" ]; then
    echo -e "${YELLOW}Fixing permissions for api/logs/${NC}"
    sudo chown -R "$CURRENT_USER":"$CURRENT_USER" api/logs
    echo -e "${GREEN}✓ Fixed api/logs permissions${NC}"
else
    echo -e "${YELLOW}api/logs directory does not exist, skipping...${NC}"
fi

echo ""
echo -e "${GREEN}✓ All permissions fixed!${NC}"
echo ""
echo "You can now run the development server without permission errors."
echo "To start development:"
echo "  - Use F5 in VSCode"
echo "  - Or select '🚀 DeepWiki 全栈开发（前端+后端）' from the launch configurations"
