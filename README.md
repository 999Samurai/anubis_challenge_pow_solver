# anubis_challenge_pow_solver
Python script that solves anubis_challenge [Proof of Work](https://en.wikipedia.org/wiki/Proof_of_work) from Anexia without a web browser.

# Example
```python
"""
<script id="anubis_challenge" type="application/json">
  {
    "rules": {
      "algorithm": "fast",
      "difficulty": 3,
      "report_as": 3
    },
    "challenge": "d800d1d339ded260"
  }
</script>
 """

challenge = "d800d1d339ded260"
difficulty = 3
# ------------------------------------------------------------------

real_res = solve(challenge, difficulty, max_workers=mp.cpu_count(), timeout=30)
print("Result:", real_res)

# Output: 
{
  'nonce': 7264, 
  'hash': '0004ce3f6f602bbf312f47365eed4bcf512890a6f5727b9c59a314616402130f', 
  'difficulty': 3, 
  'workers': 12, 
  'elapsed_s': 0.696434497833252
}
```
