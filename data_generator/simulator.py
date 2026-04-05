import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_sensor_data(num_machines=5, days=30, interval_seconds=300):
    """
    Generates synthetic industrial sensor data with failure patterns.
    - Temperature: Usually 60-80C. Failure ramp: Up to 120C.
    - Vibration: 0.02-0.05 mm/s. Failure ramp: Up to 0.15 mm/s.
    - Pressure: 90-110 psi. Failure ramp: Fluctuates wildly before drop.
    """
    data = []
    start_time = datetime.now() - timedelta(days=days)
    
    for machine_id in range(1, num_machines + 1):
        m_id = f"M00{machine_id}"
        
        # Current "remaining life" for the simulation
        # Every machine fails at some point in this 30-day window
        current_time = start_time
        failure_time = start_time + timedelta(days=random.randint(5, 25))
        is_failed = False
        
        while current_time < datetime.now():
            if is_failed:
                # Machine goes back online after 24h repair
                current_time += timedelta(hours=24)
                failure_time = current_time + timedelta(days=random.randint(5, 15))
                is_failed = False
                continue
            
            # Time until next failure in hours
            hrs_to_failure = (failure_time - current_time).total_seconds() / 3600
            
            # Normal values
            temp = random.uniform(65, 75)
            vibration = random.uniform(0.02, 0.04)
            pressure = random.uniform(95, 105)
            
            # Failure ramp patterns (if within 24 hours of failure)
            if hrs_to_failure < 24:
                # Exponential rise in temp
                temp += (24 - hrs_to_failure) ** 1.5
                # Linear rise in vibration 
                vibration += (24 - hrs_to_failure) * 0.005
                # Destabilized pressure
                pressure += random.uniform(-10, 10) * (24 - hrs_to_failure) / 24

            # Mark as failed if we hit the failure time
            if current_time >= failure_time:
                is_failed = True
            
            data.append({
                "machine_id": m_id,
                "timestamp": current_time.isoformat(),
                "temperature": round(temp, 2),
                "vibration": round(vibration, 4),
                "pressure": round(pressure, 2),
                "rul_hours": round(max(0, hrs_to_failure), 2)
            })
            
            current_time += timedelta(seconds=interval_seconds)
            
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generating synthetic factory data...")
    df = generate_sensor_data()
    df.to_csv("sensor_data.csv", index=False)
    print(f"Dataset saved with {len(df)} records.")
