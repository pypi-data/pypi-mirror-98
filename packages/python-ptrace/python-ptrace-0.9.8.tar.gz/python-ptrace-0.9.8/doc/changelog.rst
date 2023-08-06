.. _changelog:

Changelog
=========

python-ptrace 0.9.8
-------------------

* Added Arm 64bit (AArch64) support.
* Implemented ``PTRACE_GETREGSET`` and ``PTRACE_SETREGSET`` required on AArch64
  and available on Linux.
* Issue #66: Fix ``SIGTRAP|0x80`` or ``SIGTRAP`` wait in syscall_state.exit
  (``PTRACE_O_TRACESYSGOOD``).
* The development branch ``master`` was renamed to ``main``.
  See https://sfconservancy.org/news/2020/jun/23/gitbranchname/ for the
  rationale.

python-ptrace 0.9.7 (2020-08-10)
--------------------------------

* Add missing module to install directives
* Update README.rst
* Project back in beta and maintenance

python-ptrace 0.9.6 (2020-08-10)
--------------------------------

* Remove RUNNING_WINDOWS constant: python-ptrace doesn't not support Windows.
* Drop Python 2.7 support. six dependency is no longer needed.
* Add close_fds and pass_fds to createChild() function.
  Patch by Jean-Baptiste Skutnik.
* Enhance strace.py output for open flags and open optional parameters.
  Patch by Jean-Baptiste Skutnik.
* Add support for PowerPC 64-bit (ppc64).
  Patch by Jean-Baptiste Skutnik.

python-ptrace 0.9.5 (2020-04-13)
--------------------------------

* Fix readProcessMappings() for device id on 3 digits. Patch by Cat Stevens.
* Drop Python 2 support.

python-ptrace 0.9.4 (2019-07-30)
--------------------------------

* Issue #36: Fix detaching from process object created without is_attached=True
* The project now requires the six module.
* Project moved to: https://github.com/vstinner/python-ptrace

python-ptrace 0.9.3 (2017-09-19)
--------------------------------

* Issue #42: Fix test_strace.py: tolerate the openat() syscall.

python-ptrace 0.9.2 (2017-02-12)
--------------------------------

* Issue #35: Fix strace.py when tracing multiple processes: use the correct
  process. Fix suggested by Daniel Trnka.

python-ptrace 0.9.1 (2016-10-12)
--------------------------------

* Added tracing of processes created with the clone syscall (commonly known as
  threads).
* gdb.py: add ``gcore`` command, dump the process memory.
* Allow command names without absolute path.
* Fix ptrace binding: clear errno before calling ptrace().
* Fix PtraceSyscall.exit() for unknown error code
* Project moved to GitHub: https://github.com/haypo/python-ptrace
* Remove the ``ptrace.ctypes_errno`` module: use directly
  the ``ctypes.get_errno()`` function
* Remove the ``ptrace.ctypes_errno`` module: use directly
  ``ctypes.c_int8``, ``ctypes.c_uint32``, ... types

python-ptrace 0.9 (2016-04-23)
------------------------------

* Add all Linux syscall prototypes
* Add error symbols (e.g. ENOENT), in addition to error text, for strace
* Fix open mode so O_RDONLY shows if it's the only file access mode
* Python 3: fix formatting of string syscall arguments (ex: filenames), decode
  bytes from the locale encoding
* Issue #17: syscall parser now supports O_CLOEXEC and SOCK_CLOEXEC, fix unit
  tests on Python 3.4 and newer

python-ptrace 0.8.1 (2014-10-30)
--------------------------------

* Update MANIFEST.in to include all files
* Fix to support Python 3.5

python-ptrace 0.8 (2014-10-05)
------------------------------

* Issue #9: Rewrite waitProcessEvent() and waitSignals() methods of
  PtraceProcess to not call waitpid() with pid=-1. There is a race condition
  with waitpid(-1) and fork, the status of the child process may be returned
  before the debugger is noticed of the creation of the new child process.
* Issue #10: Fix PtraceProcess.readBytes() for processes not created by the
  debugger (ex: fork) if the kernel blocks access to private mappings of
  /proc/pid/mem. Fallback to PTRACE_PEEKTEXT which is slower but a debugger
  tracing the process is always allowed to use it.

python-ptrace 0.7 (2013-03-05)
------------------------------

* Experimental support of Python 3.3 in the same code base
* Drop support of Python 2.5
* Remove the ptrace.compatibility module
* Fix Process.readStruct() and Process.readArray() on x86_64
* Experimental support of ARM architecture (Linux EAPI),
  strace.py has been tested on Raspberry Pi (armv6l)

python-ptrace 0.6.6 (2013-12-16)
--------------------------------

* Fix os_tools.RUNNING_LINUX for Python 2.x compiled on Linux kernel 3.x
* Support FreeBSD on x86_64
* Add missing prototype of the unlinkat() system call. Patch written by
  Matthew Fernandez.

python-ptrace 0.6.5 (2013-06-06)
--------------------------------

* syscall: fix parsing socketcall on Linux x86
* syscall: fix prototype of socket()

python-ptrace 0.6.4 (2012-02-26)
--------------------------------

* Convert all classes to new-style classes, patch written by teythoon
* Fix compilation on Apple, patch written by Anthony Gelibert
* Support GNU/kFreeBSD, patch written by Jakub Wilk
* Support sockaddr_in6 (IPv6 address)

python-ptrace 0.6.3 (2011-02-16)
--------------------------------

* Support distrom3
* Support Python 3
* Rename strace.py option --socketcall to --socket, and fix this option for
  FreeBSD and Linux/64 bits
* Add MANIFEST.in: include all files in source distribution (tests, cptrace
  module, ...)

python-ptrace 0.6.2 (2009-11-09)
--------------------------------

* Fix 64 bits sub registers (set mask for eax, ebx, ecx, edx)

python-ptrace 0.6.1 (2009-11-07)
--------------------------------

* Create follow, showfollow, resetfollow, xray commands in gdb.py. Patch
  written by Dimitris Glynos
* Project website moved to: ``http://bitbucket.org/haypo/python-ptrace/``
* Replace types (u)intXX_t by c_(u)intXX
* Create MemoryMapping.search() method and MemoryMapping now keeps a weak
  reference to the process

python-ptrace 0.6 (2009-02-13)
------------------------------

User visible changes:

* python-ptrace now depends on Python 2.5
* Invalid memory access: add fault address in the name
* Update Python 3.0 conversion patch
* Create -i (--show-ip) option to strace.py: show instruction pointer
* Add a new example (itrace.py) written by Mark Seaborn and based
  on strace.py

API changes:

* PtraceSyscall: store the instruction pointer at syscall enter (if the
  option instr_pointer=True, disabled by default)
* Remove PROC_DIRNAME and procFilename() from ptrace.linux_proc

Bugfixes:

* Fix locateProgram() for relative path
* Fix interpretation of memory fault on MOSVW instruction (source is ESI and
  destination is EDI, and not the inverse!)

python-ptrace 0.5 (2008-09-13)
------------------------------

Visible changes:

* Write an example (the most simple debugger) and begin to document the code
* gdb.py: create "dbginfo" command
* Parse socket syscalls on FreeBSD
* On invalid memory access (SIGSEGV), eval the dereference expression to get
  the fault address on OS without siginfo (e.g. FreeBSD)
* Fixes to get minimal Windows support: fix imports, fix locateProgram()

Other changes:

* Break the API:
  - Rename PtraceDebugger.traceSysgood() to PtraceDebugger.enableSysgood()
  - Rename PtraceDebugger.trace_sysgood to PtraceDebugger.use_sysgood
  - Remove PtraceProcess.readCode()
* Create createChild() function which close all files except stdin,
  stdout and stderr
* On FreeBSD, on process exit recalls waitpid(pid) to avoid zombi process


python-ptrace 0.4.2 (2008-08-28)
--------------------------------

* BUGFIX: Fix typo in gdb.py (commands => command_str), it wasn't possible to
  write more than one command...
* BUGFIX: Fix typo in SignalInfo class (remove "self."). When a process
  received a signal SIGCHLD (because of a fork), the debugger exited because
  of this bug.
* BUGFIX: Debugger._wait() return abnormal process exit as a normal event,
  the event is not raised as an exception
* PtraceSignal: don't clear preformatted arguments (e.g. arguments of execve)

python-ptrace 0.4.1 (2008-08-23)
--------------------------------

* The project has a new dedicated website: http://python-ptrace.hachoir.org/
* Create cptrace: optional Python binding of ptrace written in C (faster
  than ptrace, the Python binding written in Python with ctypes)
* Add name attribute to SignalInfo classes
* Fixes to help Python 3.0 compatibility: don't use sys.exc_clear()
  (was useless) in writeBacktrace()
* ProcessState: create utime, stime, starttime attributes

python-ptrace 0.4.0 (2008-08-19)
--------------------------------

Visible changes:

* Rename the project to "python-ptrace" (old name was "Ptrace)
* strace.py: create --ignore-regex option
* PtraceSignal: support SIGBUS, display the related registers and
  the instruction
* Support execve() syscall tracing

Developer changes:

* New API is incompatible with 0.3.2
* PtraceProcess.waitProcessEvent() accepts optional blocking=False argument
* PtraceProcess.getreg()/setreg() are able to read/write i386 and x86-64
  "sub-registers" like al or bx
* Remove iterProc() function, replaced by openProc() with explicit
  call to .close() to make sure that files are closed
* Create searchProcessesByName()
* Replace CPU_PPC constant by CPU_POWERPC and create CPU_PPC32 and CPU_PPC64
* Create MemoryMapping object, used by readMappings() and findStack() methods
  of PtraceProcess
* Always define all PtraceProcess methods but raise an error if the function
  is not implemented
