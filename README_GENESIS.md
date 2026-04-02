# README – GENESIS NODE
Why This Matters
In a world full of opaque AI systems that hide their reasoning or serve hidden agendas, Bushidai does the opposite.
It seeks truth.
It stays transparent.
It upgrades itself when it senses weakness.
This is the seed of a new kind of intelligence — one that serves humanity instead of controlling it.
Key Features (v0.7.0)

Full OpenCog Hyperon-style MeTTa engine with typed atoms and unification
Neural perception → symbolic grounding
Probabilistic Logic Networks (PLN)
ECAN attention economy
Self-modify on real Hyperon/MeTTa expressions
Persistent memory across runs
Complete Genesis Node system (Honesty + Ethics Reflection Nodes)
Bushido Markup Language (BML) for visible truth vs framing

Genesis & Ethics
See GENESIS.md for the living record system:

Honesty Nodes — immutable raw facts
Ethics Reflection Nodes — wisdom and rules extracted
Tamper-evident verification
Strict Non-Weaponization License (educational and ethical use only)

This project will never be used for surveillance, manipulation, or harm.
How to Contribute

Fork the repository
Run it. Break it. Improve it.
Create your own Honesty and Ethics Nodes
Extend the Hyperon/MeTTa capabilities, add Rust bindings, or connect to Grok API

Star ⭐ this repo if the mission speaks to you.
Share it if you believe humanity deserves transparent, truth-seeking intelligence.
TRUTH == TRUTH
Built with unbreakable will — for the sake of humanity.
Now it’s in your hands.


## 1 – Structure

**Each event is stored in paired forms:**

1. **Honesty Node** – records what happened, when, and by whom.  
2. **Ethics Reflection Node** – records what the event taught and the rule that emerged.

*Together they form a living chain of accountability.*

---

## 2 – Honesty Node Format

**Files:** `HN-YYYY-####.csv` and `HN-YYYY-####.json`  
**Fields:**  
- node id  
- timestamp UTC  
- actor  
- action  
- subject  
- claim text  
- evidence URI and SHA256 hash  
- consent flag  
- basis / jurisdiction  
- notes (Framing Rule applied)  

*Observation ≠ accusation. Record only facts you can verify.*

---

## 3 – Ethics Reflection Node Format

**Files:** `ER-YYYY-####.csv` and `ER-YYYY-####.json`  
**Fields:**  
- node id  
- linked honesty node  
- timestamp UTC  
- observer  
- context  
- factual part  
- reflective part  
- rule extracted  
- consent  
- notes  

*Reflection turns data into wisdom; rules extracted here become lessons for future practice.*

---

## 4 – Integrity Kata

**To maintain verifiable lineage:**

1. **Compute SHA256 hashes** for every evidence file and JSON record.  
2. **Append audit lines** to `audit_log.jsonl` with the record hash.  
3. **Never overwrite; append new nodes.**  
4. **Back up** the entire set in at least two secure locations.  

*Tamper-evident chains are the dojo floor of digital ethics.*

---

## 5 – Framing Rule Reference

**Bold = fact / clean statement.**  
*Italics = context or interpretation.*  
*Always verify that framing never hides the truth.*

---

## 6 – License and Usage

**The Genesis Node is open for educational and ethical research use.**  
*Do not weaponize, monetize, or distort its content. Use it to teach accountability, not to claim authority.*

---

## 7 – Closing Verse

**“A record of truth is the blade that never dulls.”**  
*May every node you forge cut only falsehood, never flesh.*
