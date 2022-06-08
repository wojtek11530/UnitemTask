# Unitem programming task

Repository with a solution of a programming task given during an application for a job in UnitemSoftware.

The project demands Python version higher or equal 3.8. The dependencies are managed by Poetry, 
they are listed in `pyproject.toml` and can be installed with 
```
poetry install
```
For legacy reasons `requirements.txt` is kept.

The program is an example of Producer-Consumer architecture. It runs threads of the producer and the
consumer. The producer utilizes the data source, which generates random images, and pass them to 
the consumer which process them. After that images are passed to additional task (run on separate 
thread) which saves them to as PNG files to `processed` directory.

To run the main app:
```
python -m unitem_task.main
```
