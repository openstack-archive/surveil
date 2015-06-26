Heat AutoScaling with Surveil
-----------------------------

When used with OpenStack integration, Surveil export metrics to Ceilometer. This allows for auto scaling based on application metrics with Heat.

For example, the ``autoscaling.yaml`` template below allows for scaling when there is an average of more than four users connected to the machines in the stack (via ssh).

autoscaling.yml
***************

.. literalinclude:: ../examples/autoscaling.yaml
