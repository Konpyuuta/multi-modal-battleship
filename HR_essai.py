#!/usr/bin/env python3
'''
script for EmotiBitProcessor.py
This script initializes the processor and monitors heart rate values in real-time.
'''

import time
import signal
import sys
from EmotiBitProcessor import EmotiBitProcessor


def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully exit the script."""
    print("\nStopping EmotiBit processor...")
    processor.stop()
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    print("Starting EmotiBit processor test script...")
    print("Press Ctrl+C to exit")

    # Initialize the processor
    processor = EmotiBitProcessor.get_instance()

    # Configure OSC settings if needed
    # By default, it listens on 0.0.0.0:12345
    # Uncomment and modify these lines if you need different settings
    # processor.ip = "127.0.0.1"  # Only listen on localhost
    # processor.port = 12345      # Change port if needed

    # Start the processor
    processor.start()

    print(f"Listening for EmotiBit data on {processor.ip}:{processor.port}")
    print("Waiting for heart rate data...")

    # Monitor and display heart rate
    try:
        last_hr = 0
        while True:
            # Get current heart rate
            current_hr = processor.get_current_heart_rate()

            # Only print when heart rate changes
            if current_hr != last_hr:
                if current_hr > 0:
                    print(f"Current heart rate: {current_hr:.1f} BPM")
                last_hr = current_hr

            # Check if we're receiving data
            if len(processor.ppg_green_buffer) > 0 and last_hr == 0:
                print(
                    f"Receiving PPG data (buffer size: {len(processor.ppg_green_buffer)}), waiting for heart rate calculation...")

            # Sleep to avoid high CPU usage
            time.sleep(0.5)
    except KeyboardInterrupt:
        # This should be caught by the signal handler above
        pass
    finally:
        # Ensure processor is stopped on exit
        processor.stop()