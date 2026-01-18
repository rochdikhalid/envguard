from typing import Dict


def diff_envs(env_a: Dict[str, str], env_b: Dict[str, str]) -> str:
    """
    Compare two environment dictionaries.
    Returns a human-readable diff.
    
    Symbols:
      + Added in B
      - Removed from B
      ~ Changed value
    """

    lines = []

    keys_a = set(env_a.keys())
    keys_b = set(env_b.keys())

    # Added in B
    for key in sorted(keys_b - keys_a):
        lines.append(f"+ {key} (missing in A)")

    # Removed from B
    for key in sorted(keys_a - keys_b):
        lines.append(f"- {key} (missing in B)")

    # Changed values
    for key in sorted(keys_a & keys_b):
        val_a = env_a[key]
        val_b = env_b[key]

        if val_a != val_b:
            # Mask values for security
            lines.append(f"~ {key}: value differs (masked)")

    if not lines:
        return "✅ Environments are identical!"

    return "\n".join(lines)
