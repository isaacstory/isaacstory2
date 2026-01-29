#!/bin/bash
# Deploy script for Isaac Story site

set -e

cd "$(dirname "$0")"

echo "📦 Building site for Nginx..."
VITE_BASE=/isaacstory/ npm run build

echo "🔗 Creating symlink in /var/www/html..."
sudo ln -sfn "$(pwd)/dist" /var/www/html/isaacstory

echo "✅ Done! Site available at:"
echo "   http://localhost/isaacstory/"
echo "   http://$(hostname -I | awk '{print $1}')/isaacstory/"
