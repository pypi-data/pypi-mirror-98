import_profile
==============

Want to know how much time and memory each of your Python imports costs?

Find out with `import_profile`!

Just do:

    python3 -m import_profile flask sqlalchemy flask_sqlalchemy pandas numpy

And you will get:

    flask sqlalchemy flask_sqlalchemy numpy pandas

                       time cpu.user cpu.system memory.uss memory.rss
    flask              0.15     0.12       0.02       9.92      13.08
    sqlalchemy         0.10     0.09       0.01       5.09       5.22
    flask_sqlalchemy   0.07     0.07       0.00       3.45       3.43
    numpy              0.12     0.12       0.09       7.52      12.31
    pandas             0.35     0.28       0.06      17.78      25.10
    *base*             0.00     0.05       0.02       5.96      11.61

    time       = seconds of real time since the import trial began
    cpu.user   = seconds of CPU time spent in this process
    cpu.system = seconds of CPU time spent waiting for the OS kernel, such
                 as waiting for file I/O to complete
    memory.uss = unique set size - memory taken up by process, minus
                 shared objects/DLLs (megabytes)
    memory.rss = resident set size (megabytes)
