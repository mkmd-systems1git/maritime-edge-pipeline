import asyncio
import json
import time
import random
import multiprocessing

class ResilientEdgeAgent:
    def __init__(self):
        self.local_buffer = []  # Emergency backup queue for satellite dropouts
        self.cloud_connected = True

    async def generate_telemetry_loop(self, queue):
        print("🚀 Marine Instrumentation Simulator Started Streaming Data...")
        while True:
            # Simulate real-time ship GPS data strings near Mombasa port
            lat = round(random.uniform(-4.0, -4.1), 4)
            lon = round(random.uniform(39.6, 39.7), 4)
            speed = round(random.uniform(12.0, 15.5), 1)
            
            data = {
                "timestamp": int(time.time()),
                "lat": lat,
                "lon": lon,
                "speed_knots": speed,
                "engine_rpm": random.randint(720, 750)
            }
            await queue.put(data)
            await asyncio.sleep(1)

    async def process_uplink_loop(self, queue):
        print("⚓ Edge Agent Initialized. Monitoring Satellite Network Links...")
        while True:
            data = await queue.get()
            
            # Chaos engineering simulator: 20% chance of random satellite dropout at sea
            self.cloud_connected = random.random() > 0.2
            
            if self.cloud_connected:
                print(f"🛰️ [UPLINK SUCCESS] Transmitted optimized payload to Cloud HQ: Lat {data['lat']}, Lon {data['lon']}")
                
                # Flush emergency backup queue if satellite link is restored
                if self.local_buffer:
                    print(f"🔄 Sat-Link Restored! Flushing {len(self.local_buffer)} buffered records to shore...")
                    while self.local_buffer and self.cloud_connected:
                        buffered_data = self.local_buffer.pop(0)
                        print(f"📤 Sent buffered data: Timestamp {buffered_data['timestamp']}")
            else:
                # SATELLITE DROPOUT RULE: Save to edge storage buffer instead of throwing it away
                print(f"⚠️ Sat-Link Down. Saving data to local edge storage: Time {data['timestamp']}")
                self.local_buffer.append(data)
                
            queue.task_done()

async def main():
    shared_queue = asyncio.Queue()
    agent = ResilientEdgeAgent()
    
    # Run data generator and uplink processing concurrently in the async loop
    await asyncio.gather(
        agent.generate_telemetry_loop(shared_queue),
        agent.process_uplink_loop(shared_queue)
    )

if __name__ == "__main__":
    print("🚀 Starting Production-Grade Maritime Edge Control Ecosystem...")
    asyncio.run(main())
