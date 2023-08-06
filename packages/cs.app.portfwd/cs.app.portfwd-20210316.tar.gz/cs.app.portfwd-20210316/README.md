Manage persistent ssh tunnels and port forwards.

*Latest release 20210316*:
* Portfwds: accept any iterable for target_list.
* Portability fix.

Portfwd runs a collection of ssh tunnel commands persistently,
each in its own `cs.app.svcd <https://pypi.org/project/cs.app.svcd>`_ instance
with all the visibility and process control that SvcD brings.

It reads tunnel preconditions from special comments within the ssh config file.
It uses the configuration options from the config file
as the SvcD signature function
thus restarting particular ssh tunnels when their specific configuration changes.
It has an "automatic" mode (the -A option)
which monitors the desired list of tunnels
from statuses expressed via `cs.app.flag <https://pypi.org/project/cs.app.flag>`_
which allows live addition or removal of tunnels as needed.

## Function `Condition(portfwd, op, invert, *args)`

Factory to construct a condition from a specification.

## Class `FlagCondition(_PortfwdCondition)`

A flag based condition.

### Method `FlagCondition.test(self, trace=False)`

Core test, before inversion.

## Function `main(argv=None, environ=None)`

Command line main programme.

## Class `PingCondition(_PortfwdCondition)`

A ping based condition.

### Method `PingCondition.test(self, trace=False)`

Ping the target as a test.

## Class `Portfwd(cs.app.flag.FlaggedMixin)`

An ssh tunnel built on a SvcD.

### Method `Portfwd.__init__(self, target, ssh_config=None, conditions=(), test_shcmd=None, trace=False, verbose=False, flags=None)`

Initialise the Portfwd.

Parameters:
* `target`: the tunnel name, and also the name of the ssh configuration used
* `ssh_config`: ssh configuration file if not the default
* `conditions`: an iterable of `Condition`s
  which must hold before the tunnel is set up;
  the tunnel also aborts if these cease to hold
* `test_shcmd`: a shell command which must succeed
  before the tunnel is set up;
  the tunnel also aborts if this command subsequently fails
* `trace`: issue tracing messages; default `False`
* `verbose`: be verbose; default `False`
* `flags`: optional preexisting `Flags` instance

### Method `Portfwd.on_reap(self)`

Actions to perform after the ssh tunnel exits.

### Method `Portfwd.on_spawn(self)`

Actions to perform before commencing the ssh tunnel.

Initially remove local socket paths.

### Method `Portfwd.ssh_argv(self, bare=False)`

An ssh command line argument list.

`bare`: just to command and options, no trailing "--".

### Method `Portfwd.ssh_options(self)`

Return a defaultdict(list) of `{option: values}`
representing the ssh configuration.

### Method `Portfwd.start(self)`

Call the service start method.

### Method `Portfwd.stop(self)`

Call the service stop method.

### Method `Portfwd.test_func(self)`

Servuice test function: probe all the conditions.

### Method `Portfwd.wait(self)`

Call the service wait method.

## Class `Portfwds`

A collection of `Portfwd` instances and associated control methods.

### Method `Portfwds.__init__(self, ssh_config=None, environ=None, target_list=None, auto_mode=None, trace=False, verbose=False, flags=None)`

Initialise the `Portfwds` instance.

Parameters:
* `ssh_config`: the ssh configuration file if not the default
* `environ`: the environment mapping to use;
  default: `os.environ`
* `target_list`: an iterable of `Portfwd` target names
* `auto_mode`: also derive target names
  from the set of true `PORTFWD_`*name*`_AUTO` flags
* `trace`: trace mode, default `False`
* `verbose`: verbose mode, default `False`
* `flags`: the `cs.app.flags.Flags` instance to use,
  default is to construct a new one

### Method `Portfwds.forward(self, target)`

Obtain the named Portfwd, creating it if necessary.

### Property `Portfwds.forwards`

A list of the existing Portfwd instances.

### Method `Portfwds.resolve_target_spec(self, spec)`

Accept a target spec and expand it if it is a group.
Return a set of targets.

### Method `Portfwds.start(self)`

Start all nonrunning targets, stop all running nonrequired targets.

### Method `Portfwds.stop(self)`

Stop all running targets.

### Method `Portfwds.targets_required(self)`

The concrete list of targets.

Computed from the target spec and, if in auto mode, the
PORTFWD_*_AUTO flags.

### Method `Portfwds.wait(self)`

Wait for all running targets to stop.

# Release Log



*Release 20210316*:
* Portfwds: accept any iterable for target_list.
* Portability fix.

*Release 20190602*:
* Support alert groups.
* ssh_argv no longer a property in order to support `bare` param.
* New method `ssh_options` to wrap ssh_argv.
* Drop sig_func, use ssh_options instead.
* Remove local UNIX domain socket forward endpoints before starting ssh tunnel.
* Improve option parse.

*Release 20170906*:
Initial PyPI release.
