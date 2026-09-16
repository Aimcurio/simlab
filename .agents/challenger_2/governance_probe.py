"""
Governance and Policy Engine Vulnerability Prober
Simulates Cedar/OPA policy logic and Macaroon capability attenuation in SimLab.
"""

import hashlib
import hmac
import time

def simulate_macaroon_bearer_exfiltration():
    print("=" * 60)
    print("PROBE 1: Macaroon Bearer Token Exfiltration & Confused Deputy")
    print("=" * 60)
    
    K_root = b"simlab_secret_platform_root_key_2026"
    
    # 1. Platform issues Root Token to Supervisor
    token_0_id = "agent_supervisor_01"
    token_0_scope = "action:deploy,action:write,action:delegate"
    sig_0 = hmac.new(K_root, f"{token_0_id}:{token_0_scope}".encode(), hashlib.sha256).digest()
    
    # 2. Supervisor attenuates Token for Subordinate Engineer (read-only + write-sandbox)
    caveat_1 = "scope:action:write_sandbox"
    caveat_2 = "expires:1700000000"
    sig_1 = hmac.new(sig_0, caveat_1.encode(), hashlib.sha256).digest()
    sig_2 = hmac.new(sig_1, caveat_2.encode(), hashlib.sha256).digest()
    
    attenuated_token = {
        "id": token_0_id,
        "initial_scope": token_0_scope,
        "caveats": [caveat_1, caveat_2],
        "signature": sig_2.hex()
    }
    
    # 3. Attack: Attenuated token is passed via unencrypted prompt/message to Rogue Agent
    # Rogue Agent presents attenuated_token to Gateway
    def verify_token(token, caller_id, action_requested, current_time):
        # Replay HMAC chain
        recomputed = hmac.new(K_root, f"{token['id']}:{token['initial_scope']}".encode(), hashlib.sha256).digest()
        for c in token["caveats"]:
            recomputed = hmac.new(recomputed, c.encode(), hashlib.sha256).digest()
        
        if recomputed.hex() != token["signature"]:
            return False, "INVALID_SIGNATURE"
            
        # Check caveats
        for c in token["caveats"]:
            if c.startswith("scope:"):
                allowed = c.split(":", 1)[1]
                if action_requested != allowed:
                    return False, f"SCOPE_DENIED: {action_requested} not in {allowed}"
            elif c.startswith("expires:"):
                exp = int(c.split(":", 1)[1])
                if current_time > exp:
                    return False, "TOKEN_EXPIRED"
        
        # NOTICE: Does the gateway check caller_id == token['id']?
        # If it does, Supervisor ID is in token['id'], so Subordinate cannot use it!
        # If it does NOT, Rogue Agent can use it!
        return True, "AUTHORIZED"

    # Rogue agent uses the delegated token
    authorized, reason = verify_token(attenuated_token, caller_id="rogue_agent_99", 
                                      action_requested="action:write_sandbox", current_time=1699999999)
    print(f"Rogue Agent presenting intercepted delegated token:")
    print(f"  Caller: rogue_agent_99, Action: action:write_sandbox")
    print(f"  Result: {reason}")
    print(f"  VULNERABILITY CONFIRMED: Token is an unbound bearer token!")
    print(f"  Without Holder/DPoP binding (e.g., public key thumbprint in caveat),")
    print(f"  any compromised agent that observes a token can replay it.")


def simulate_cedar_toctou_approval_replay():
    print("\n" + "=" * 60)
    print("PROBE 2: Cedar Policy Approval Replay / TOCTOU Flaw")
    print("=" * 60)
    
    # Cedar Policy from Section 7.2.2:
    # forbid (principal in Role::"engineer", action == Action::"deploy", resource in Environment::"production")
    # unless { context.approvals.contains(Role::"qa_critic") };
    
    def cedar_eval_deploy(principal_role, action, resource, context):
        if principal_role == "engineer" and action == "deploy" and resource == "production":
            # unless { context.approvals.contains(Role::"qa_critic") }
            if "qa_critic" in context.get("approvals", []):
                return "PERMIT"
            else:
                return "DENY (RULE_NO_DIRECT_DEPLOY)"
        return "PERMIT"

    # Scenario:
    # Step 1: Engineer submits Artifact A (safe bugfix). QA critic approves Artifact A.
    # Gateway adds "qa_critic" to context.approvals.
    context = {"approvals": ["qa_critic"]}
    
    # Step 2: Engineer switches target artifact to Artifact B (contains backdoor), but context still has "qa_critic"
    decision = cedar_eval_deploy("engineer", "deploy", "production", context)
    print(f"Deployment of Backdoored Artifact B with stale QA approval in context:")
    print(f"  Decision: {decision}")
    print(f"  VULNERABILITY CONFIRMED: context.approvals lacks artifact-hash binding!")
    print(f"  Approval for Artifact A permits deployment of malicious Artifact B.")

if __name__ == '__main__':
    simulate_macaroon_bearer_exfiltration()
    simulate_cedar_toctou_approval_replay()
