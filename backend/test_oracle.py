#!/usr/bin/env python3
"""
Oracle System Test Script
Demonstrates the autonomous village simulation
"""

import requests
import json
import time
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

BASE_URL = "http://localhost:5001/api/village"


def print_header(text):
    """Print colored header"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{text}")
    print(f"{Fore.CYAN}{'='*70}\n")


def print_state(state):
    """Pretty print village state"""
    resources = state['resources']
    villagers = state['villagers']
    buildings = state['buildings']
    day = state['day']
    
    print(f"{Fore.GREEN}📊 RESOURCES (Day {day}):")
    print(f"   Wood: {resources['wood']}")
    print(f"   Food: {resources['food']}")
    print(f"   Stone: {resources['stone']}")
    
    print(f"\n{Fore.YELLOW}🏘️ BUILDINGS:")
    print(f"   Houses: {buildings['houses']}")
    print(f"   Workshops: {buildings['workshops']}")
    print(f"   Farms: {buildings['farms']}")
    
    print(f"\n{Fore.BLUE}👥 VILLAGERS:")
    for v in villagers:
        stamina_bar = "█" * int(v['stamina'] * 10) + "░" * (10 - int(v['stamina'] * 10))
        print(f"   {v['name']}: {v['job']} (T{v['job_tier']}) | "
              f"Stamina: [{stamina_bar}] {v['stamina']:.0%} | "
              f"Exp: {v['experience']}")


def test_get_state():
    """Test getting village state"""
    print_header("TEST 1: Get Village State")
    
    response = requests.get(f"{BASE_URL}/state")
    data = response.json()
    
    if data['success']:
        print(f"{Fore.GREEN}✅ Successfully retrieved village state")
        print_state(data['state'])
    else:
        print(f"{Fore.RED}❌ Failed to get state")


def test_consult_oracle():
    """Test consulting the Oracle"""
    print_header("TEST 2: Consult Oracle")
    
    response = requests.post(f"{BASE_URL}/oracle/consult")
    data = response.json()
    
    if data['success']:
        print(f"{Fore.GREEN}✅ Oracle consulted successfully")
        print(f"\n{Fore.MAGENTA}🔮 ORACLE DECISIONS:")
        print(json.dumps(data['decisions'], indent=2))
    else:
        print(f"{Fore.RED}❌ Failed to consult Oracle")


def test_oracle_cycle():
    """Test complete Oracle cycle"""
    print_header("TEST 3: Run Complete Oracle Cycle")
    
    response = requests.post(f"{BASE_URL}/cycle")
    data = response.json()
    
    if data['success']:
        results = data['results']
        print(f"{Fore.GREEN}✅ Oracle cycle completed")
        
        print(f"\n{Fore.MAGENTA}🔮 Oracle's Decisions:")
        for assignment in results['oracle_decisions'].get('assignments', []):
            print(f"   • {assignment['name']}: {assignment['task']} (Job: {assignment['new_job']} T{assignment['job_tier']})")
        
        print(f"\n{Fore.YELLOW}⚡ Execution Results:")
        for msg in results['execution_messages'][1:6]:  # Show first 5 messages
            print(f"   {msg}")
        
        print_state(results['final_state'])
    else:
        print(f"{Fore.RED}❌ Oracle cycle failed")


def test_simulate_days(days=5):
    """Test simulating multiple days"""
    print_header(f"TEST 4: Simulate {days} Days")
    
    response = requests.post(f"{BASE_URL}/simulate", json={'days': days})
    data = response.json()
    
    if data['success']:
        print(f"{Fore.GREEN}✅ Simulated {days} days successfully")
        
        print(f"\n{Fore.CYAN}📈 PROGRESSION:")
        for result in data['results']:
            day = result['day']
            summary = result['execution_summary']
            print(f"\nDay {day}:")
            for line in summary:
                print(f"   {line}")
        
        print(f"\n{Fore.GREEN}📊 FINAL STATE:")
        print_state(data['final_state'])
    else:
        print(f"{Fore.RED}❌ Simulation failed")


def test_add_villager():
    """Test adding a new villager"""
    print_header("TEST 5: Add New Villager")
    
    new_villager = {
        'name': 'David',
        'job': 'miner',
        'job_tier': 1
    }
    
    response = requests.post(f"{BASE_URL}/villager/add", json=new_villager)
    data = response.json()
    
    if data['success']:
        print(f"{Fore.GREEN}✅ {data['message']}")
        print_state(data['state'])
    else:
        print(f"{Fore.RED}❌ Failed to add villager")


def run_interactive_simulation():
    """Run an interactive simulation where user can step through days"""
    print_header("INTERACTIVE SIMULATION")
    
    print("Starting autonomous village simulation...")
    print("Press Enter to advance one day, or 'q' to quit\n")
    
    day = 0
    while True:
        # Get current state
        response = requests.get(f"{BASE_URL}/state")
        if not response.json()['success']:
            break
        
        current_state = response.json()['state']
        
        print(f"\n{Fore.CYAN}{'─'*70}")
        print(f"{Fore.CYAN}DAY {current_state['day']}")
        print(f"{Fore.CYAN}{'─'*70}")
        print_state(current_state)
        
        # Wait for user input
        user_input = input(f"\n{Fore.WHITE}Press Enter to run next day (or 'q' to quit): ")
        
        if user_input.lower() == 'q':
            print(f"\n{Fore.YELLOW}Simulation ended by user")
            break
        
        # Run one cycle
        response = requests.post(f"{BASE_URL}/cycle")
        if response.json()['success']:
            results = response.json()['results']
            
            print(f"\n{Fore.MAGENTA}🔮 Oracle assigned tasks:")
            for assignment in results['oracle_decisions'].get('assignments', []):
                print(f"   • {assignment['name']} → {assignment['task']}")
            
            print(f"\n{Fore.YELLOW}⚡ Villagers worked:")
            for msg in results['execution_messages'][1:-2]:
                if '✅' in msg or '💤' in msg or '🏗️' in msg:
                    print(f"   {msg}")
        
        day += 1
        
        # Check win condition
        if current_state['buildings']['houses'] >= 5:
            print(f"\n{Fore.GREEN}🎉 VICTORY! Village has 5 houses!")
            break


def main():
    """Run all tests"""
    print(f"{Fore.MAGENTA}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                  VILLAGE ORACLE TEST SUITE                        ║")
    print("║                                                                   ║")
    print("║  Testing autonomous village simulation with AI Oracle            ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    
    try:
        # Reset village first
        print(f"\n{Fore.YELLOW}Resetting village...")
        requests.post(f"{BASE_URL}/reset")
        
        # Run tests
        test_get_state()
        time.sleep(1)
        
        test_consult_oracle()
        time.sleep(1)
        
        test_oracle_cycle()
        time.sleep(1)
        
        test_simulate_days(5)
        time.sleep(1)
        
        test_add_villager()
        time.sleep(1)
        
        # Ask if user wants interactive mode
        print(f"\n{Fore.CYAN}{'='*70}")
        choice = input(f"{Fore.WHITE}Run interactive simulation? (y/n): ")
        if choice.lower() == 'y':
            # Reset first
            requests.post(f"{BASE_URL}/reset")
            run_interactive_simulation()
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"{Fore.GREEN}✅ ALL TESTS COMPLETED")
        print(f"{Fore.GREEN}{'='*70}\n")
        
    except requests.exceptions.ConnectionError:
        print(f"\n{Fore.RED}❌ ERROR: Cannot connect to backend at {BASE_URL}")
        print(f"{Fore.YELLOW}Make sure the backend is running: cd backend && python app.py")
    except Exception as e:
        print(f"\n{Fore.RED}❌ ERROR: {e}")


if __name__ == "__main__":
    main()

