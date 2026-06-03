Heartbeat and Startup
======================

Heartbeat wakes the Agent periodically to do background tasks.
``jiuwenclaw-start`` starts everything with one command.

Heartbeat
---------

Enable in ``.jiuwenclaw/config/config.yaml``:

.. code-block:: yaml

   heartbeat:
     enabled: true
     every: 60
     task: "Check inbox and summarize new messages."

The Gateway sends the task to Agent at the configured interval. Useful for:

- Daily summaries
- Monitoring alerts
- Scheduled reports

One-Command Startup
-------------------

.. code-block:: bash

   jiuwenclaw-start

This starts:

.. code-block:: text

   AgentServer (port 18092) + WebChannel (port 19000)

Press Ctrl+C to stop both gracefully.
