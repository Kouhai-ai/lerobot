#!/usr/bin/env python3
"""
Simple SO101 Connection Test
============================

This script tests basic connection to the SO101 robot without trying to
configure all motors. Use this to debug connection issues.
"""

import sys
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import scservo_sdk as scs
    logger.info("✓ scservo_sdk imported successfully")
except ImportError as e:
    logger.error(f"✗ Failed to import scservo_sdk: {e}")
    sys.exit(1)

def test_connection(port: str, baudrate: int = 1000000):
    """Test basic connection to SO101 robot"""

    logger.info(f"Testing connection to {port} at {baudrate} baud")

    # Create handlers
    port_handler = scs.PortHandler(port)
    packet_handler = scs.PacketHandler(0)  # Protocol version 0

    try:
        # Open port
        logger.info("Opening port...")
        if not port_handler.openPort():
            logger.error(f"Failed to open port {port}")
            return False

        # Set baudrate
        logger.info("Setting baudrate...")
        if not port_handler.setBaudRate(baudrate):
            logger.error(f"Failed to set baudrate to {baudrate}")
            port_handler.closePort()
            return False

        # Try to ping motor ID 1 (shoulder_pan)
        logger.info("Pinging motor ID 1...")
        model_number, result, error = packet_handler.ping(port_handler, 1)

        if result == scs.COMM_SUCCESS:
            logger.info(f"✓ Motor ID 1 responded! Model: {model_number}")
        else:
            logger.warning(f"Motor ID 1 did not respond: {packet_handler.getTxRxResult(result)}")

        # Try a few more motor IDs
        for motor_id in [2, 3, 4, 5, 6]:
            logger.info(f"Pinging motor ID {motor_id}...")
            model_number, result, error = packet_handler.ping(port_handler, motor_id)

            if result == scs.COMM_SUCCESS:
                logger.info(f"✓ Motor ID {motor_id} responded! Model: {model_number}")
            else:
                logger.warning(f"Motor ID {motor_id} did not respond: {packet_handler.getTxRxResult(result)}")

        # Close port
        port_handler.closePort()
        logger.info("Connection test completed")
        return True

    except Exception as e:
        logger.error(f"Exception during connection test: {e}")
        try:
            port_handler.closePort()
        except:
            pass
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_connection.py <port>")
        print("Example: python test_connection.py /dev/tty.usbmodem58FA0962001")
        sys.exit(1)

    port = sys.argv[1]

    # Test different baud rates
    baud_rates = [1000000, 115200, 57600, 9600]

    for baudrate in baud_rates:
        logger.info(f"\n=== Testing baudrate {baudrate} ===")
        if test_connection(port, baudrate):
            logger.info(f"✓ Connection successful at {baudrate} baud")
            break
        else:
            logger.warning(f"✗ Connection failed at {baudrate} baud")
    else:
        logger.error("Failed to connect at any baud rate")
        sys.exit(1)