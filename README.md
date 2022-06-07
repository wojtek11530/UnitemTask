# Unitem programming task

Repository with a solution of a programming task given during an application for a job in UnitemSoftware.

The program is an example of Producer-Consumer architecture. It runs threads of the producer and the
consumer. The producer utilizes the data source, which generates random images, and pass them to 
the consumer which process them. After that images are passed to additional task (run on separate 
thread) which saves them to as PNG files to `processed` directory.

To run the main app:
```
python -m unitem_task.main
```
