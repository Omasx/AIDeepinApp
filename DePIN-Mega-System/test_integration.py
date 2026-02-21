import asyncio
import sys
import os
sys.path.append(os.getcwd())

from projects.aoi_system.main_aoi import AOISystem

async def test_init():
    print("Testing AOISystem initialization with Phantom Grid...")
    try:
        aoi = AOISystem()
        # We won't call initialize() because it starts background loops
        print("AOISystem instantiated successfully.")
        
        # Test Phantom bridge presence
        if hasattr(aoi, 'phantom'):
            print("PhantomBridge detected in AOISystem.")
        else:
            print("Error: PhantomBridge NOT detected.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_init())
