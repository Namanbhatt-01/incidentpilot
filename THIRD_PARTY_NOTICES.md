# Third-Party Notices & Attribution

This project, **IncidentPilot**, incorporates, adapts, or references components from the following open-source projects in strict compliance with their respective licenses:

---

## 1. Incident Suite
- **Repository**: [https://github.com/dbDez/incident-suite](https://github.com/dbDez/incident-suite)
- **License**: MIT License
- **Copyright**: (c) 2025 dbDez
- **Components Incorporated / Adapted**:
  - Runbook Markdown definitions (`switch/runbooks/`)
  - Log parsing concepts (`packages/infrastructure/knowledge/chunker.py`)
  - Structured SRE schema contracts (`packages/domain/entities.py`)
  - Adversarial Critic Agent design (`packages/application/handlers/critic.py`)

### Full MIT License Text:
```text
MIT License

Copyright (c) 2025 dbDez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 2. Akmatori
- **Repository**: [https://github.com/akmatori/akmatori](https://github.com/akmatori/akmatori)
- **License**: Apache License, Version 2.0
- **Copyright**: (c) 2025 Akmatori Authors
- **Components Incorporated / Adapted**:
  - Human-in-the-loop approval gate concepts and permission boundaries (`packages/application/handlers/approval.py`)

### Full Apache 2.0 License Notice:
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at `http://www.apache.org/licenses/LICENSE-2.0`.

---

## 3. Switch Infrastructure
- **Repository**: [https://github.com/sandbox-quantum/switch](https://github.com/sandbox-quantum/switch)
- **Official Documentation**: [https://docs.switchagents.ai](https://docs.switchagents.ai)
- **Usage**:
  - Switch Agent Protocol (SSE streaming and HTTP operations) wire contract.
  - Switch Room Template schema (`switch/templates/incident-pilot.template.yaml`).

