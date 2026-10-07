import requests
import json
import os
import sys

# MOCK: This represents a local win32crypt or pyKCS11 interaction with a physical USB token
def sign_payload_locally(payload: dict) -> dict:
    """
    Simulates signing the bid payload using a local USB DSC.
    Crucial Security Constraint: Private key never leaves the hardware token.
    """
    print("Detecting local USB Digital Signature Certificate (DSC)...")
    print("Found token: 'ePass2003Auto'")
    
    # In reality, we'd hash the payload and pass the hash to the smart card for RSA signing.
    signed_hash = "mock_signed_hash_12345abcdef"
    
    payload["dsc_signature"] = signed_hash
    payload["signer_cert_serial"] = "00-11-22-33-AA-BB"
    
    print("Payload successfully signed locally.")
    return payload

def submit_signed_bid(api_url: str, bid_id: str, token: str):
    print(f"Fetching bid payload for bid_id: {bid_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Fetch unsigned payload from SaaS
    # resp = requests.get(f"{api_url}/api/v1/bids/{bid_id}/payload", headers=headers)
    # payload = resp.json()
    
    # Mocking response
    payload = {
        "tender_id": "TENDER-123",
        "documents": ["tech_proposal.pdf", "emd_receipt.pdf"],
        "bid_amount": 150000.00
    }
    
    # 2. Sign locally
    signed_payload = sign_payload_locally(payload)
    
    # 3. Submit directly to Portal (or back to SaaS for relay)
    print("Transmitting signed packet...")
    print("Success: Bid submitted securely.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python signer.py <bid_id> <auth_token>")
        sys.exit(1)
    
    bid_id = sys.argv[1]
    auth_token = sys.argv[2]
    api_url = os.getenv("SAAS_API_URL", "http://localhost:8000")
    
    submit_signed_bid(api_url, bid_id, auth_token)
