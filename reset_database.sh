#!/bin/bash

# Reset the database and clear locks
echo "Resetting database..."

cd backend

# Remove existing database files
rm -f promptly.db
rm -f promptly.db-wal
rm -f promptly.db-shm

echo "Database reset complete. You can now restart the backend server."
