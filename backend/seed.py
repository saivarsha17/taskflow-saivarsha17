#!/usr/bin/env python
"""
Seed script to populate the database with test data.
Usage: python seed.py
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from auth.models import User
from tasks.models import Project, Task


def clear_data():
    """Clear existing data"""
    print("Clearing existing data...")
    Task.objects.all().delete()
    Project.objects.all().delete()
    User.objects.all().delete()
    print("✓ Data cleared")


def seed_data():
    """Seed database with test data"""
    print("Seeding database...")
    
    # Create test user
    user1 = User.objects.create_user(
        email='test@example.com',
        name='Test User',
        password='password123'
    )
    print(f"✓ Created user: {user1.email}")
    
    # Create additional users for assignment
    user2 = User.objects.create_user(
        email='alice@example.com',
        name='Alice Smith',
        password='password123'
    )
    print(f"✓ Created user: {user2.email}")
    
    user3 = User.objects.create_user(
        email='bob@example.com',
        name='Bob Johnson',
        password='password123'
    )
    print(f"✓ Created user: {user3.email}")
    
    # Create project
    project = Project.objects.create(
        name='Website Redesign',
        description='Q2 website redesign project',
        owner=user1
    )
    print(f"✓ Created project: {project.name}")
    
    # Create tasks with different statuses
    task1 = Task.objects.create(
        title='Design homepage',
        description='Create mockups and design system for homepage',
        status='todo',
        priority='high',
        project=project,
        assignee=user2,
        due_date=datetime.now().date() + timedelta(days=7)
    )
    print(f"✓ Created task: {task1.title} (status: {task1.status})")
    
    task2 = Task.objects.create(
        title='Implement authentication',
        description='Setup JWT authentication endpoints',
        status='in_progress',
        priority='high',
        project=project,
        assignee=user1,
        due_date=datetime.now().date() + timedelta(days=5)
    )
    print(f"✓ Created task: {task2.title} (status: {task2.status})")
    
    task3 = Task.objects.create(
        title='Setup database',
        description='Create PostgreSQL schema and migrations',
        status='done',
        priority='high',
        project=project,
        assignee=user3,
        due_date=datetime.now().date() - timedelta(days=2)
    )
    print(f"✓ Created task: {task3.title} (status: {task3.status})")
    
    task4 = Task.objects.create(
        title='Write API documentation',
        description='Document all API endpoints with examples',
        status='todo',
        priority='medium',
        project=project,
        assignee=None,
        due_date=datetime.now().date() + timedelta(days=10)
    )
    print(f"✓ Created task: {task4.title} (unassigned)")
    
    print("\n" + "=" * 50)
    print("Seeding complete!")
    print("=" * 50)
    print("\nTest credentials:")
    print("  Email:    test@example.com")
    print("  Password: password123")
    print("\nOther test users:")
    print("  Email:    alice@example.com")
    print("  Email:    bob@example.com")
    print("  Password: password123 (for all)")


if __name__ == '__main__':
    try:
       
        seed_data()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
