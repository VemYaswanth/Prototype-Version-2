#!/bin/bash
echo "🔍 Checking if database 'securitydb' exists..."
if psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='securitydb'" | grep -q 1; then
  echo "✅ Database 'securitydb' already exists."
else
  echo "⚠️ Database 'securitydb' not found. Creating now..."
  createdb -U postgres securitydb
  echo "✅ Database 'securitydb' created successfully."
fi
