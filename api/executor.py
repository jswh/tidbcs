import time
from subprocess import Popen, PIPE, STDOUT
from os import path

class Executor(object):
    log_path = ''
    scripts_path = ''
    checkout_target = ''
    lock_path = ''

    on_error = ' error and exit'
    on_success = ' success'

    current_proc = None
    test_proc_num = 4

    def __init__(self, log_path, scripts_path, checkout_target, lock_path, test_proc_num = 4):
        self.log_path = log_path
        self.scripts_path = scripts_path
        self.checkout_target = checkout_target
        self.lock_path = lock_path
        self.test_proc_num = test_proc_num

    def run_procedure(self, command):
        proc = Popen(
            command,
            stdout=PIPE,
            universal_newlines=True,
            stderr=STDOUT,
        )
        self.current_proc = proc
        for line in iter(proc.stdout.readline,''):
            yield line.rstrip()

        yield proc.wait()

    def __build_procedures(self)r:
        scripts = self.scripts_path
        return [
            [scripts + 'checkout.sh', self.checkout_target],
            [scripts + 'failpoint.sh', 'enable'],
            self.unit_test,
            [scripts + 'failpoint.sh', 'disable'],
            scripts + 'end.sh',
        ]

    def packages(self):
        pkgs = []
        for pkg in self.run_procedure(self.scripts_path + 'packages.sh'):
            if not isinstance(pkg, int):
                pkgs.append(pkg)

        return pkgs

    def unit_test(self):
        pkgs = self.packages()
        test_procs = []
        test_state = 0
        while True:
            if len(pkgs) == 0 and len(test_procs) == 0:
                yield 'all test finished';
                break
            running_procs = []
            for test_proc in test_procs:
                if test_proc.poll() != None:
                    test_state = test_state + test_proc.poll()
                    for line in iter(test_proc.stdout.readline,''):
                        yield line.rstrip()
                else:
                    running_procs.append(test_proc)
            new_procs_num = min(len(pkgs), self.test_proc_num - len(running_procs))
            for i in range(0, new_procs_num):
                pkg = pkgs.pop()
                yield "start test " + pkg + '\n'
                proc = Popen(
                    [self.scripts_path + 'test.sh', pkg],
                    stdout=PIPE,
                    bufsize=20,
                    universal_newlines=True,
                )
                running_procs.append(proc)
            test_procs = running_procs

        yield test_state

    def is_locked(lock):
        return path.exists(lock)

    def lock(self):
        for line in self.run_procedure(['touch', self.lock_path]):
            print(line)

    def free_lock(self):
        for line in self.run_procedure(['rm', '-f', self.lock_path]):
            print(line)

    def run(self):
        if Executor.is_locked(self.lock_path):
            yield 'another process running'
            return
        self.lock()
        def run_command(command):
            if isinstance(command, str) or isinstance(command, list):
                return self.run_procedure(command)
            else:
                return command()
        with open(self.log_path, 'w') as log_file:
            last_save = time.time()
            for command in self.__build_procedures():
                for line in run_command(command):
                    if isinstance(line, int):
                        if line == 0:
                            success = str(command) + self.on_success
                            log_file.writelines(success + '\n')
                            yield success + '<br/>\n'
                        else:
                            error = str(command) + self.on_error
                            log_file.writelines(error + '\n')
                            self.free_lock()
                            yield error + '<br/>\n'
                            return
                    else:
                        log_file.writelines(line + '\n')
                        yield line + '<br/>\n'
                        if (time.time() - last_save > 1):
                            log_file.flush()
                            last_save = time.time()
            yield 'finish<br/>'
        self.free_lock()
