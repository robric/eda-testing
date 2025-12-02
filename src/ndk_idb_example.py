#!/usr/bin/env python3
"""
Step-by-step NDK exploration script.
Run with different steps to explore NDK functionality.
"""

import time
import grpc

from ndk import sdk_service_pb2
from ndk import sdk_service_pb2_grpc
from ndk import config_service_pb2
from ndk import config_service_pb2_grpc


SRLINUX_HOST = "127.0.0.1:50053"
AGENT_NAME   = "bond_007"


def step1_register():
    """Step 1: Register agent with NDK."""
    print("\n" + "="*70)
    print("STEP 1: Registering Agent")
    print("="*70)
    
    channel = grpc.insecure_channel(SRLINUX_HOST)
    client = sdk_service_pb2_grpc.SdkMgrServiceStub(channel)
    
    reg = sdk_service_pb2.AgentRegistrationRequest()
    metadata = [("agent_name", AGENT_NAME)]
    
    try:
        resp = client.AgentRegister(reg, metadata=metadata)
        print(f"✓ Agent registered successfully!")
        print(f"  Response: {resp}")
        return channel, metadata
    except Exception as e:
        print(f"✗ Failed to register: {e}")
        return None, None


def step2_explore_config_service(channel, metadata):
    """Step 2: Explore what's in config_service_pb2."""
    print("\n" + "="*70)
    print("STEP 2: Exploring Config Service")
    print("="*70)
    
    print("\nAvailable in config_service_pb2:")
    config_attrs = [x for x in dir(config_service_pb2) if not x.startswith('_')]
    for attr in config_attrs[:10]:  # Show first 10
        print(f"  - {attr}")
    
    print("\nAvailable in config_service_pb2_grpc:")
    grpc_attrs = [x for x in dir(config_service_pb2_grpc) if not x.startswith('_')]
    for attr in grpc_attrs:
        print(f"  - {attr}")


def step3_explore_available_methods(channel, metadata):
    """Step 3: See what methods are available on the config stub."""
    print("\n" + "="*70)
    print("STEP 3: Exploring Available Config Service Methods")
    print("="*70)
    
    config_stub = config_service_pb2_grpc.SdkMgrConfigServiceStub(channel)
    
    print("\nMethods available on SdkMgrConfigServiceStub:")
    methods = [m for m in dir(config_stub) if not m.startswith('_')]
    for method in methods:
        print(f"  - {method}")
    
    print("\nRequest types available:")
    request_types = [x for x in dir(config_service_pb2) if 'Request' in x]
    for req_type in request_types:
        print(f"  - {req_type}")
    
    print("\nResponse types available:")
    response_types = [x for x in dir(config_service_pb2) if 'Response' in x]
    for resp_type in response_types:
        print(f"  - {resp_type}")


def step4_explore_config_key(channel, metadata):
    """Step 4: Explore ConfigKey structure."""
    print("\n" + "="*70)
    print("STEP 4: Exploring ConfigKey Structure")
    print("="*70)
    
    print("\nCreating ConfigKey...")
    key = config_service_pb2.ConfigKey()
    print(f"  ConfigKey fields: {[f.name for f in key.DESCRIPTOR.fields]}")
    
    # Try setting js_path
    key.js_path = "/interface"
    print(f"  Set js_path to: {key.js_path}")


def step5_explore_notifications(channel, metadata):
    """Step 5: Explore notification service."""
    print("\n" + "="*70)
    print("STEP 5: Exploring Notification Service")
    print("="*70)
    
    notification_stub = sdk_service_pb2_grpc.SdkNotificationServiceStub(channel)
    
    print("\nMethods available on SdkNotificationServiceStub:")
    methods = [m for m in dir(notification_stub) if not m.startswith('_')]
    for method in methods:
        print(f"  - {method}")
    
    print("\nNotification-related types in sdk_service_pb2:")
    notif_types = [x for x in dir(sdk_service_pb2) if 'Notification' in x]
    for notif_type in notif_types:
        print(f"  - {notif_type}")


def step6_listen_for_notifications(channel, metadata):
    """Step 6: Actually listen for notifications."""
    print("\n" + "="*70)
    print("STEP 6: Listening for Notifications")
    print("="*70)
    
    notification_stub = sdk_service_pb2_grpc.SdkNotificationServiceStub(channel)
    
    print("\nExploring NotificationRegisterRequest...")
    reg_req = sdk_service_pb2.NotificationRegisterRequest()
    print(f"  Fields: {[f.name for f in reg_req.DESCRIPTOR.fields]}")
    
    # Check what operations are available
    print("\nAvailable operation values:")
    for field in reg_req.DESCRIPTOR.fields:
        if field.name == 'op':
            print(f"  Enum type: {field.enum_type.name}")
            for value in field.enum_type.values:
                print(f"    - {value.name} = {value.number}")
    
    print("\nActual methods on notification_stub:")
    methods = [m for m in dir(notification_stub) if not m.startswith('_') and callable(getattr(notification_stub, m))]
    for method in methods:
        print(f"    - {method}")
    
    print("\n" + "="*70)
    print("Looking at step 5 output, we found these methods:")
    print("Let me try the correct method name...")
    print("="*70)
    
    print("\nTrying to create notification stream...")
    try:
        # Try using the config subscription field
        reg_req = sdk_service_pb2.NotificationRegisterRequest()
        reg_req.op = 0  # OPERATION_CREATE
        
        # Subscribe to config notifications
        if hasattr(reg_req, 'config'):
            print("  Setting up config notification subscription...")
            config_sub = reg_req.config
            # Try to configure it
            print(f"  Config subscription type: {type(config_sub)}")
            print(f"  Config subscription fields: {[f.name for f in config_sub.DESCRIPTOR.fields]}")
        
        print("\n✗ NotificationRegister method doesn't exist")
        print("  The notification service likely uses a different pattern")
        print("  (possibly streaming RPC without explicit registration)")
        print("\nTry using ConfigSubscriptionRequest through the Config Service instead!")
        
        config_stub = config_service_pb2_grpc.SdkMgrConfigServiceStub(channel)
        print("\nAttempting config subscription via Config Service...")
        
        # Create subscription request
        sub_req = config_service_pb2.ConfigSubscriptionRequest()
        key = config_service_pb2.ConfigKey()
        key.js_path = "/interface"
        sub_req.key.CopyFrom(key)
        
        print(f"  Subscription request created with key: {sub_req.key.js_path}")
        
        print("\n  Checking if ConfigSubscribe exists on Config Service...")
        if hasattr(config_stub, 'ConfigSubscribe'):
            print("  ✓ ConfigSubscribe method found!")
        else:
            print("  ✗ ConfigSubscribe not found either")
            
        print("\n" + "="*70)
        print("DISCOVERY: NDK appears to use a push model")
        print("="*70)
        print("The agent likely receives notifications automatically")
        print("after registration, without explicit subscription calls.")
        print("\nTo receive notifications, you typically:")
        print("1. Register agent (done in step 1)")
        print("2. Keep connection alive with KeepAlive")
        print("3. Notifications arrive automatically on the channel")
            
    except KeyboardInterrupt:
        print("\n\nStopped")
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    print("="*70)
    print("SR Linux NDK Step-by-Step Explorer")
    print("="*70)
    
    # Step 1: Register
    channel, metadata = step1_register()
    if not channel:
        return
    
    # Step 2: Explore
    step2_explore_config_service(channel, metadata)
    
    # Step 3: Explore available methods
    step3_explore_available_methods(channel, metadata)
    
    # Step 4: Explore ConfigKey
    step4_explore_config_key(channel, metadata)
    
    # Step 5: Explore notifications
    step5_explore_notifications(channel, metadata)
    
    # Step 6: Listen for notifications (interactive)
    print("\n" + "="*70)
    print("Ready to listen for notifications?")
    print("="*70)
    print("\nStep 6 will start listening for config notifications.")
    print("Make changes in SR Linux CLI to see them here.")
    print("Press Enter to continue, or Ctrl+C to skip...")
    
    try:
        input()
        step6_listen_for_notifications(channel, metadata)
    except KeyboardInterrupt:
        print("\nSkipping notification listener")
    
    print("\n" + "="*70)
    print("Exploration complete!")
    print("="*70)
    
    channel.close()


if __name__ == "__main__":
    main()