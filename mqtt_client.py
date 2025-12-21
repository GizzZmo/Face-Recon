"""
MQTT client for IoT integration.

This module connects to an MQTT broker to publish and receive
messages for smart home and IoT device control.
"""

import paho.mqtt.client as mqtt


def create_mqtt_client(
    broker: str = "mqtt.example.com", port: int = 1883, keepalive: int = 60
) -> mqtt.Client:
    """
    Create and connect an MQTT client.

    Args:
        broker: MQTT broker address
        port: MQTT broker port (default: 1883)
        keepalive: Keep-alive interval in seconds

    Returns:
        Connected MQTT client
    """
    client = mqtt.Client()
    client.connect(broker, port, keepalive)
    return client


def publish_access_command(command: str, broker: str = "mqtt.example.com") -> None:
    """
    Publish an access control command via MQTT.

    Args:
        command: Command to publish (e.g., "OpenDoor", "CloseDoor")
        broker: MQTT broker address
    """
    client = create_mqtt_client(broker)
    client.publish("access_control", command)
    print(f"Published command: {command}")
    client.disconnect()


# Example usage
if __name__ == "__main__":
    publish_access_command("OpenDoor")
